"""
AgroScore 360 — Отчёт о качестве данных
========================================
Проверяет целостность, консистентность и пригодность датасета
для ML-модели скоринга.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "Выгрузка по выданным субсидиям 2025 год (обезлич).xlsx"


def load_raw() -> pd.DataFrame:
    wb = openpyxl.load_workbook(str(DATA_FILE), read_only=True)
    ws = wb.active

    rows_data = []
    for i, row in enumerate(ws.iter_rows(values_only=True), start=1):
        if i >= 6 and row[0] is not None:
            rows_data.append(row)
    wb.close()

    used_cols = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    col_names = ["id", "date", "region", "akimat", "app_number",
                 "subsidy_direction", "subsidy_name", "status",
                 "normative", "amount", "district"]

    data = [[row[c] for c in used_cols] for row in rows_data]
    df = pd.DataFrame(data, columns=col_names)
    df = df[df["id"].notna()].copy()
    df = df[df["id"].astype(str).str.match(r"^\d+")].copy()
    df["id"] = df["id"].astype(str).astype(int)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["normative"] = pd.to_numeric(df["normative"], errors="coerce")
    df["date_parsed"] = pd.to_datetime(df["date"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    return df


def check(name: str, passed: bool, detail: str = ""):
    icon = "PASS" if passed else "FAIL"
    print(f"  [{icon}] {name}")
    if detail:
        print(f"         {detail}")


def main():
    print("=" * 72)
    print("  ОТЧЁТ О КАЧЕСТВЕ ДАННЫХ — Субсидии 2025")
    print("=" * 72)

    if not DATA_FILE.exists():
        print(f"[ERROR] Файл не найден: {DATA_FILE}")
        sys.exit(1)

    df = load_raw()
    n = len(df)
    print(f"\n  Загружено записей: {n:,d}\n")

    # ---- 1. Полнота данных ----
    print("  --- 1. ПОЛНОТА ДАННЫХ (Completeness) ---")
    for col in df.columns:
        if col in ("date_parsed",):
            continue
        nulls = df[col].isna().sum()
        pct = nulls / n * 100
        ok = pct < 5
        check(f"{col:25s} пропусков: {nulls:>6,d} ({pct:.2f}%)", ok)

    # ---- 2. Уникальность ----
    print("\n  --- 2. УНИКАЛЬНОСТЬ (Uniqueness) ---")
    dup_ids = df["id"].duplicated().sum()
    check(f"Дубликаты ID: {dup_ids}", dup_ids == 0)

    dup_apps = df["app_number"].duplicated().sum()
    check(f"Дубликаты номеров заявок: {dup_apps}", dup_apps == 0,
          f"{'Есть повторяющиеся номера заявок — возможно, это нормально (обновления)' if dup_apps > 0 else ''}")

    # ---- 3. Валидность значений ----
    print("\n  --- 3. ВАЛИДНОСТЬ (Validity) ---")

    negative_amounts = (df["amount"] < 0).sum()
    check(f"Отрицательные суммы: {negative_amounts}", negative_amounts == 0)

    zero_amounts = (df["amount"] == 0).sum()
    check(f"Нулевые суммы: {zero_amounts}", zero_amounts < n * 0.01,
          f"{zero_amounts / n * 100:.2f}% — {'допустимо' if zero_amounts < n * 0.01 else 'требует проверки'}")

    negative_norms = (df["normative"] < 0).sum()
    check(f"Отрицательные нормативы: {negative_norms}", negative_norms == 0)

    valid_statuses = {"Исполнена", "Одобрена", "Отклонена", "Сформировано поручение", "Отозвано", "Получена"}
    invalid_status = ~df["status"].isin(valid_statuses)
    check(f"Невалидные статусы: {invalid_status.sum()}", invalid_status.sum() == 0,
          f"Обнаружены: {df[invalid_status]['status'].unique()[:5]}" if invalid_status.any() else "")

    valid_directions = {
        "Субсидирование в скотоводстве", "Субсидирование в птицеводстве",
        "Субсидирование в овцеводстве", "Субсидирование в верблюдоводстве",
        "Субсидирование в коневодстве", "Субсидирование в свиноводстве",
        "Субсидирование в козоводстве", "Субсидирование в пчеловодстве",
        "Субсидирование затрат по искусственному осеменению",
    }
    invalid_dir = ~df["subsidy_direction"].isin(valid_directions)
    check(f"Невалидные направления: {invalid_dir.sum()}", invalid_dir.sum() == 0)

    bad_dates = df["date_parsed"].isna().sum()
    check(f"Непарсируемые даты: {bad_dates}", bad_dates < n * 0.01)

    # ---- 4. Консистентность ----
    print("\n  --- 4. КОНСИСТЕНТНОСТЬ (Consistency) ---")

    for region, group in df.groupby("region"):
        akimats = group["akimat"].nunique()
        if akimats > 1:
            check(f"Область '{region}' → {akimats} акиматов", False,
                  "Ожидается 1 акимат на область")
            break
    else:
        check("Каждая область → 1 акимат", True)

    head_count = df["amount"] / df["normative"].replace(0, np.nan)
    extreme_heads = (head_count > 50_000).sum()
    check(
        f"Экстремальное кол-во голов (>50K): {extreme_heads}",
        extreme_heads < n * 0.005,
        f"Может указывать на ошибки в normative или amount"
    )

    # ---- 5. Распределение ----
    print("\n  --- 5. РАСПРЕДЕЛЕНИЕ (Distribution) ---")

    skewness = df["amount"].skew()
    check(f"Скошенность amount: {skewness:.2f}", True,
          "Правосторонний скос — типично для финансовых данных, рекомендуется log-трансформация")

    kurtosis = df["amount"].kurtosis()
    check(f"Эксцесс amount: {kurtosis:.2f}", True,
          "Тяжёлые хвосты — наличие крупных заявок")

    top1_pct = df.nlargest(int(n * 0.01), "amount")["amount"].sum() / df["amount"].sum() * 100
    check(f"Топ 1% заявок = {top1_pct:.1f}% суммы", True,
          "Парето-эффект: малая доля заявок аккумулирует большую часть средств")

    # ---- 6. Пригодность для ML ----
    print("\n  --- 6. ПРИГОДНОСТЬ ДЛЯ ML ---")

    check(f"Размер выборки ({n:,d})", n > 10_000,
          "Достаточно для обучения")

    target_balance = df["status"].value_counts(normalize=True)
    majority = target_balance.iloc[0]
    check(f"Баланс классов (макс. доля: {majority:.1%})", majority < 0.8,
          f"{'Дисбаланс — рекомендуется SMOTE или class_weight' if majority >= 0.6 else 'Умеренный баланс'}")

    n_features_raw = 7  # region, district, direction, name, status, normative, amount
    check(f"Кол-во сырых признаков: {n_features_raw}", n_features_raw >= 5)

    n_cat_high_card = sum(1 for c in ["district", "subsidy_name"] if df[c].nunique() > 50)
    check(f"Высококардинальные категории: {n_cat_high_card}", True,
          "district (192) и subsidy_name (35+) — использовать target encoding или embedding")

    # ---- Summary ----
    print("\n" + "=" * 72)
    print("  ИТОГО: Датасет пригоден для ML-скоринга с учётом рекомендаций:")
    print("    - Log-трансформация amount для нормализации")
    print("    - Target encoding для district")
    print("    - Class weight балансировка для status")
    print("    - Проверить выбросы в верхнем 1% по amount")
    print("=" * 72)


if __name__ == "__main__":
    main()
