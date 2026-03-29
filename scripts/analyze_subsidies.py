"""
AgroScore 360 — Полный анализ датасета субсидий 2025 года
=========================================================
Скрипт загружает выгрузку из subsidy.plem.kz и выводит:
  1. Классификацию всех полей
  2. Базовую статистику
  3. Распределения по регионам, направлениям, статусам
  4. Временной анализ
  5. Аномалии и выбросы
  6. Корреляции и паттерны
"""

from __future__ import annotations

import os
import sys
import warnings
from collections import Counter
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

warnings.filterwarnings("ignore")

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "Выгрузка по выданным субсидиям 2025 год (обезлич).xlsx"

FIELD_SCHEMA = {
    0:  ("id",                "№ п/п",                     "int",         "ID",
         "Порядковый номер заявки в системе subsidy.plem.kz. "
         "Используется как уникальный идентификатор записи."),
    1:  ("date",              "Дата поступления",           "datetime",    "Temporal",
         "Дата и время подачи заявки (ДД.ММ.ГГГГ ЧЧ:ММ:СС). "
         "Позволяет строить временные ряды, определять сезонность подачи заявок, "
         "рассчитывать скорость обработки."),
    4:  ("region",            "Область",                    "categorical", "Geography",
         "Область Казахстана, в которую подана заявка (18 регионов). "
         "Используется для географической агрегации, расчёта климатических рисков, "
         "сравнения регионов по объёму субсидий."),
    5:  ("akimat",            "Акимат",                     "categorical", "Geography",
         "Управление сельского хозяйства при акимате области — орган, "
         "принимающий и рассматривающий заявку. Связан с регионом."),
    6:  ("app_number",        "Номер заявки",               "string",      "ID",
         "Уникальный 14-значный номер заявки в системе ИСС. "
         "Формат кодирует тип субсидии и хронологию."),
    7:  ("subsidy_direction", "Направление",                "categorical", "Category",
         "Направление животноводства (9 категорий: скотоводство, птицеводство, "
         "овцеводство, коневодство, верблюдоводство, свиноводство, козоводство, "
         "пчеловодство, искусственное осеменение). "
         "Определяет нормативные ставки и требования к заявителю."),
    8:  ("subsidy_name",      "Наименование субсидирования","categorical", "Category",
         "Полное наименование вида субсидии (~35 уникальных видов). "
         "Детализирует тип поддержки: селекционная работа, приобретение племенного "
         "поголовья, удешевление кормов, удешевление производства мяса/молока и т.д. "
         "Ключевое поле для классификации типов господдержки."),
    9:  ("status",            "Статус заявки",              "categorical", "Target/Label",
         "Текущий статус обработки заявки (6 значений: Исполнена, Одобрена, "
         "Отклонена, Сформировано поручение, Отозвано, Получена). "
         "КЛЮЧЕВОЕ ПОЛЕ: используется как целевая переменная / метка для ML, "
         "отражает историю обязательств заявителя (Art. 14-1)."),
    10: ("normative",         "Норматив",                   "numeric",     "Financial",
         "Нормативная ставка субсидии на единицу (тенге за голову скота, "
         "за кг продукции и т.д.). 41 уникальное значение — от 20 до 700,000 тг. "
         "Определяется Приказом МСХ №108 для каждого вида субсидии."),
    11: ("amount",            "Причитающая сумма",          "numeric",     "Financial/Target",
         "Расчётная сумма субсидии к выплате (тенге). "
         "Диапазон: 0 — 1,229,004,660 тг. Среднее: 3,801,413 тг. "
         "Формула: норматив × количество единиц. "
         "КЛЮЧЕВОЕ ПОЛЕ: основная числовая метрика для анализа и scoring."),
    12: ("district",          "Район хозяйства",           "categorical", "Geography",
         "Район, в котором расположено хозяйство заявителя (192 уникальных). "
         "1.1% пропусков. Используется для детальной геоаналитики."),
}


def load_data() -> pd.DataFrame:
    """Load the Excel file and return a cleaned DataFrame."""
    if not DATA_FILE.exists():
        print(f"[ERROR] Файл не найден: {DATA_FILE}")
        sys.exit(1)

    print(f"Загрузка {DATA_FILE.name} ...")
    wb = openpyxl.load_workbook(str(DATA_FILE), read_only=True)
    ws = wb.active

    header_row = None
    rows_data = []
    for i, row in enumerate(ws.iter_rows(values_only=True), start=1):
        if i == 5:
            header_row = row
            continue
        if i >= 6 and row[0] is not None:
            rows_data.append(row)

    wb.close()

    used_cols = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    col_names = [FIELD_SCHEMA[c][0] for c in used_cols]

    data = []
    for row in rows_data:
        data.append([row[c] for c in used_cols])

    df = pd.DataFrame(data, columns=col_names)

    df = df[df["id"].notna()].copy()
    df = df[df["id"].astype(str).str.match(r"^\d+")].copy()
    df["id"] = df["id"].astype(str).astype(int)

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["normative"] = pd.to_numeric(df["normative"], errors="coerce").fillna(0)
    df["region"] = df["region"].fillna("Неизвестный").str.strip()
    df["district"] = df["district"].fillna("Неизвестный").str.strip()
    df["subsidy_direction"] = df["subsidy_direction"].fillna("Неизвестно").str.strip()
    df["status"] = df["status"].fillna("Неизвестно").str.strip()

    df["date_parsed"] = pd.to_datetime(
        df["date"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )

    df["head_count"] = (
        df["amount"] / df["normative"].replace(0, 1)
    ).round(0).clip(0, 100_000).astype(int)

    print(f"Загружено {len(df)} записей.\n")
    return df


def section(title: str):
    width = 72
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_field_classification():
    section("1. КЛАССИФИКАЦИЯ ПОЛЕЙ ДАТАСЕТА")
    print("""
Файл: Выгрузка по выданным субсидиям 2025 год (обезлич).xlsx
Источник: ИСС subsidy.plem.kz (Информационная Система Субсидирования)
Период: 21.01.2025 — 19.03.2026
Строк данных: ~36,651
Столбцов с данными: 11 (из 17 в Excel — остальные пустые/служебные)
""")

    for col_idx in sorted(FIELD_SCHEMA.keys()):
        code, name_ru, dtype, category, desc = FIELD_SCHEMA[col_idx]
        print(f"  [{col_idx:2d}] {code:22s}  |  {name_ru}")
        print(f"       Тип: {dtype:15s}  |  Категория: {category}")
        print(f"       {desc}")
        print()


def analyze_basic_stats(df: pd.DataFrame):
    section("2. БАЗОВАЯ СТАТИСТИКА")

    print(f"  Всего записей:        {len(df):>10,d}")
    print(f"  Уникальных заявок:    {df['app_number'].nunique():>10,d}")
    print(f"  Регионов (область):   {df['region'].nunique():>10,d}")
    print(f"  Районов:              {df['district'].nunique():>10,d}")
    print(f"  Направлений:          {df['subsidy_direction'].nunique():>10,d}")
    print(f"  Видов субсидий:       {df['subsidy_name'].nunique():>10,d}")
    print(f"  Статусов:             {df['status'].nunique():>10,d}")
    print(f"  Уникальных нормативов:{df['normative'].nunique():>10,d}")

    print(f"\n  --- Финансовые показатели (тенге) ---")
    print(f"  Общая сумма:          {df['amount'].sum():>20,.0f}")
    print(f"  Средняя сумма:        {df['amount'].mean():>20,.0f}")
    print(f"  Медиана:              {df['amount'].median():>20,.0f}")
    print(f"  Минимум:              {df['amount'].min():>20,.0f}")
    print(f"  Максимум:             {df['amount'].max():>20,.0f}")
    print(f"  Стд. отклонение:      {df['amount'].std():>20,.0f}")

    print(f"\n  --- Пропуски ---")
    for col in df.columns:
        n_null = df[col].isna().sum()
        if n_null > 0:
            pct = n_null / len(df) * 100
            print(f"  {col:25s}: {n_null:>6,d}  ({pct:.1f}%)")
    if df.isna().sum().sum() == 0:
        print("  Пропусков нет (после очистки)")


def analyze_status(df: pd.DataFrame):
    section("3. РАСПРЕДЕЛЕНИЕ ПО СТАТУСАМ")

    total = len(df)
    status_stats = (
        df.groupby("status")
        .agg(count=("id", "count"), total_amount=("amount", "sum"), avg_amount=("amount", "mean"))
        .sort_values("count", ascending=False)
    )

    print(f"\n  {'Статус':<30s} {'Кол-во':>8s} {'%':>7s} {'Сумма (млрд тг)':>18s} {'Средн. (тыс тг)':>18s}")
    print("  " + "-" * 85)
    for status, row in status_stats.iterrows():
        pct = row["count"] / total * 100
        print(
            f"  {status:<30s} {int(row['count']):>8,d} {pct:>6.1f}% "
            f"{row['total_amount'] / 1e9:>17.2f} {row['avg_amount'] / 1e3:>17.1f}"
        )

    approved = df[df["status"].isin(["Исполнена", "Одобрена", "Сформировано поручение"])]["amount"].sum()
    rejected = df[df["status"].isin(["Отклонена", "Отозвано"])]["amount"].sum()
    print(f"\n  Одобрено/Исполнено суммарно: {approved / 1e9:,.2f} млрд тг")
    print(f"  Отклонено/Отозвано суммарно: {rejected / 1e9:,.2f} млрд тг")
    print(f"  Процент отказов по кол-ву:   {df['status'].isin(['Отклонена', 'Отозвано']).sum() / total * 100:.1f}%")


def analyze_regions(df: pd.DataFrame):
    section("4. РАСПРЕДЕЛЕНИЕ ПО РЕГИОНАМ")

    region_stats = (
        df.groupby("region")
        .agg(
            count=("id", "count"),
            total_amount=("amount", "sum"),
            avg_amount=("amount", "mean"),
            median_amount=("amount", "median"),
        )
        .sort_values("total_amount", ascending=False)
    )

    print(f"\n  {'Область':<40s} {'Заявок':>7s} {'Сумма (млрд тг)':>17s} {'Средн. (тыс тг)':>17s}")
    print("  " + "-" * 85)
    for region, row in region_stats.iterrows():
        print(
            f"  {region:<40s} {int(row['count']):>7,d} "
            f"{row['total_amount'] / 1e9:>16.2f} {row['avg_amount'] / 1e3:>16.1f}"
        )


def analyze_directions(df: pd.DataFrame):
    section("5. РАСПРЕДЕЛЕНИЕ ПО НАПРАВЛЕНИЯМ ЖИВОТНОВОДСТВА")

    dir_stats = (
        df.groupby("subsidy_direction")
        .agg(
            count=("id", "count"),
            total_amount=("amount", "sum"),
            avg_amount=("amount", "mean"),
            avg_norm=("normative", "mean"),
        )
        .sort_values("count", ascending=False)
    )

    print(f"\n  {'Направление':<55s} {'Заявок':>7s} {'Сумма (млрд тг)':>17s}")
    print("  " + "-" * 82)
    for direction, row in dir_stats.iterrows():
        print(
            f"  {direction:<55s} {int(row['count']):>7,d} "
            f"{row['total_amount'] / 1e9:>16.2f}"
        )


def analyze_subsidy_types(df: pd.DataFrame):
    section("6. ТОП-15 ВИДОВ СУБСИДИЙ ПО СУММЕ")

    type_stats = (
        df.groupby("subsidy_name")
        .agg(count=("id", "count"), total_amount=("amount", "sum"))
        .sort_values("total_amount", ascending=False)
        .head(15)
    )

    for i, (name, row) in enumerate(type_stats.iterrows(), 1):
        short_name = name[:90] + "..." if len(name) > 90 else name
        print(f"\n  {i:2d}. {short_name}")
        print(f"      Заявок: {int(row['count']):,d}  |  Сумма: {row['total_amount'] / 1e9:.2f} млрд тг")


def analyze_temporal(df: pd.DataFrame):
    section("7. ВРЕМЕННОЙ АНАЛИЗ")

    valid_dates = df[df["date_parsed"].notna()].copy()
    if valid_dates.empty:
        print("  Не удалось распарсить даты.")
        return

    print(f"\n  Период: {valid_dates['date_parsed'].min()} — {valid_dates['date_parsed'].max()}")

    valid_dates["month"] = valid_dates["date_parsed"].dt.to_period("M")
    monthly = (
        valid_dates.groupby("month")
        .agg(count=("id", "count"), total_amount=("amount", "sum"))
        .sort_index()
    )

    print(f"\n  {'Месяц':<12s} {'Заявок':>8s} {'Сумма (млрд тг)':>17s}")
    print("  " + "-" * 40)
    for period, row in monthly.iterrows():
        bar = "█" * int(row["count"] / monthly["count"].max() * 30)
        print(
            f"  {str(period):<12s} {int(row['count']):>8,d} "
            f"{row['total_amount'] / 1e9:>16.2f}  {bar}"
        )


def analyze_normatives(df: pd.DataFrame):
    section("8. АНАЛИЗ НОРМАТИВНЫХ СТАВОК")

    norm_stats = (
        df.groupby("normative")
        .agg(count=("id", "count"), total_amount=("amount", "sum"), avg_heads=("head_count", "mean"))
        .sort_values("count", ascending=False)
    )

    print(f"\n  {'Норматив (тг)':>15s} {'Заявок':>8s} {'%':>7s} {'Сумма (млрд тг)':>17s} {'Ср. голов':>10s}")
    print("  " + "-" * 62)
    for norm, row in norm_stats.head(20).iterrows():
        pct = row["count"] / len(df) * 100
        print(
            f"  {norm:>15,.0f} {int(row['count']):>8,d} {pct:>6.1f}% "
            f"{row['total_amount'] / 1e9:>16.2f} {row['avg_heads']:>9.0f}"
        )


def analyze_outliers(df: pd.DataFrame):
    section("9. ВЫБРОСЫ И АНОМАЛИИ")

    q1 = df["amount"].quantile(0.25)
    q3 = df["amount"].quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    outliers = df[df["amount"] > upper]

    print(f"\n  IQR метод (amount):")
    print(f"    Q1:         {q1:>15,.0f} тг")
    print(f"    Q3:         {q3:>15,.0f} тг")
    print(f"    IQR:        {iqr:>15,.0f} тг")
    print(f"    Верхняя гр: {upper:>15,.0f} тг")
    print(f"    Выбросов:   {len(outliers):>10,d}  ({len(outliers) / len(df) * 100:.1f}%)")

    print(f"\n  ТОП-10 крупнейших заявок:")
    top10 = df.nlargest(10, "amount")
    for _, row in top10.iterrows():
        print(
            f"    #{int(row['id']):>6d}  {row['amount'] / 1e6:>10,.1f} млн тг  "
            f"{row['region'][:25]:<25s}  {row['status']}"
        )

    zero_amount = df[df["amount"] == 0]
    print(f"\n  Заявки с нулевой суммой: {len(zero_amount)}")

    if df["date_parsed"].notna().any():
        weekend = df[df["date_parsed"].dt.dayofweek >= 5]
        print(f"  Заявки поданные в выходные: {len(weekend)} ({len(weekend) / len(df) * 100:.1f}%)")


def analyze_cross_patterns(df: pd.DataFrame):
    section("10. ПЕРЕКРЁСТНЫЕ ПАТТЕРНЫ")

    print("\n  --- Процент отказов по регионам (топ-5) ---")
    region_reject = (
        df.groupby("region")
        .apply(lambda x: pd.Series({
            "total": len(x),
            "rejected": x["status"].isin(["Отклонена", "Отозвано"]).sum(),
            "reject_rate": x["status"].isin(["Отклонена", "Отозвано"]).mean() * 100,
        }))
        .sort_values("reject_rate", ascending=False)
    )
    for region, row in region_reject.head(5).iterrows():
        print(f"    {region:<40s} {row['reject_rate']:.1f}%  ({int(row['rejected'])} из {int(row['total'])})")

    print("\n  --- Средняя сумма по направлениям и статусам ---")
    pivot = df.pivot_table(
        values="amount", index="subsidy_direction", columns="status",
        aggfunc="mean", fill_value=0
    )
    for direction in pivot.index:
        exec_val = pivot.loc[direction].get("Исполнена", 0) / 1e3
        rej_val = pivot.loc[direction].get("Отклонена", 0) / 1e3
        short = direction[:50]
        print(f"    {short:<52s} Исп: {exec_val:>10,.0f} тыс  Откл: {rej_val:>10,.0f} тыс")

    print("\n  --- Концентрация: доля топ-5 регионов ---")
    top5_regions = df.groupby("region")["amount"].sum().nlargest(5)
    pct_top5 = top5_regions.sum() / df["amount"].sum() * 100
    print(f"    Топ-5 регионов аккумулируют {pct_top5:.1f}% от общей суммы субсидий")
    for r, v in top5_regions.items():
        print(f"      {r:<40s} {v / 1e9:.2f} млрд тг")


def print_summary_for_agroscore(df: pd.DataFrame):
    section("11. ВЫВОДЫ ДЛЯ AGROSCORE 360")
    print("""
  Рекомендации по использованию полей для ML-скоринга:

  ЦЕЛЕВЫЕ ПЕРЕМЕННЫЕ:
    - amount (Причитающая сумма)  → Regression target
    - status (Статус заявки)      → Classification target

  КЛЮЧЕВЫЕ ПРИЗНАКИ (Features):
    - region + district           → Геолокация → климатический риск
    - subsidy_direction           → Тип хозяйства → инфраструктурный вес
    - normative                   → Ставка → масштаб операции
    - head_count (derived)        → Размер хозяйства
    - status                      → Исторические обязательства (proxy)
    - date                        → Сезонность, тренды

  ПРОИЗВОДНЫЕ ПРИЗНАКИ (Feature Engineering):
    - infrastructure_index        → f(normative, head_count, direction)
    - herd_survival_rate          → f(status, climate_risk)
    - historical_obligations_met  → f(status)
    - climate_risk_factor         → f(region, district)
    - amount_per_head             → amount / head_count
    - month / quarter             → из date

  ПОЛЯ-ИДЕНТИФИКАТОРЫ (не для ML):
    - id                          → Порядковый номер
    - app_number                  → Номер заявки
    - akimat                      → Дублирует region
""")


def main():
    print_field_classification()

    df = load_data()

    analyze_basic_stats(df)
    analyze_status(df)
    analyze_regions(df)
    analyze_directions(df)
    analyze_subsidy_types(df)
    analyze_temporal(df)
    analyze_normatives(df)
    analyze_outliers(df)
    analyze_cross_patterns(df)
    print_summary_for_agroscore(df)

    print("\n" + "=" * 72)
    print("  АНАЛИЗ ЗАВЕРШЁН")
    print("=" * 72)


if __name__ == "__main__":
    main()
