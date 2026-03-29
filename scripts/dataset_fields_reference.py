"""
Справочник полей датасета субсидий 2025
======================================
- Для categorical-полей: все уникальные значения из файла (с частотой).
- Для остальных полей: описание из схемы + краткая статистика по данным.

Запуск из корня репозитория:
  python3 scripts/dataset_fields_reference.py

Рекомендуется виртуальное окружение backend (там уже есть pandas):
  source backend/.venv/bin/activate && python3 scripts/dataset_fields_reference.py

Если pandas не найден, скрипт сам перезапустится через backend/.venv/bin/python3,
если такой интерпретатор существует.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent


def _reexec_with_backend_venv_if_no_pandas() -> None:
    try:
        import pandas  # noqa: F401
    except ModuleNotFoundError:
        venv_prefix = (REPO_ROOT / "backend" / ".venv").resolve()
        in_backend_venv = Path(sys.prefix).resolve() == venv_prefix
        for name in ("python3", "python"):
            vpy = REPO_ROOT / "backend" / ".venv" / "bin" / name
            # На macOS системный python3 и venv/bin/python3 часто один бинарник;
            # отличие — sys.prefix (site-packages). Перезапускаем с venv, если не в нём.
            if vpy.is_file() and not in_backend_venv:
                os.execv(str(vpy), [str(vpy), str(Path(__file__).resolve()), *sys.argv[1:]])
        print(
            "Не установлен pandas. Варианты:\n"
            "  1) Активируйте venv:  source backend/.venv/bin/activate\n"
            "  2) Установите зависимости:  pip install -r backend/requirements.txt\n"
            "  3) Запустите явно:  backend/.venv/bin/python3 scripts/dataset_fields_reference.py",
            file=sys.stderr,
        )
        sys.exit(1)


_reexec_with_backend_venv_if_no_pandas()

import pandas as pd  # noqa: E402
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analyze_subsidies as asmod  # noqa: E402


def print_rule(char: str = "=", width: int = 76) -> None:
    print(char * width)


def describe_non_categorical(df: pd.DataFrame, col: str, name_ru: str, desc: str, dtype: str) -> None:
    print_rule("-")
    print(f"  {col}  —  {name_ru}")
    print(f"  Тип: {dtype}")
    print()
    print(f"  {desc}")
    print()

    s = df[col]
    if col == "id":
        print(f"  Диапазон ID: {int(s.min())} … {int(s.max())}  (записей: {len(s):,d})")
    elif col == "date":
        parsed = pd.to_datetime(s, format="%d.%m.%Y %H:%M:%S", errors="coerce")
        ok = parsed.notna()
        print(f"  Формат: ДД.ММ.ГГГГ ЧЧ:ММ:СС")
        if ok.any():
            print(f"  Минимум:  {parsed[ok].min()}")
            print(f"  Максимум: {parsed[ok].max()}")
        print(f"  Примеры: {s.iloc[0]}, {s.iloc[len(s) // 2]}, {s.iloc[-1]}")
    elif col == "app_number":
        u = s.astype(str).nunique()
        print(f"  Уникальных номеров заявок: {u:,d} (почти всегда = числу строк)")
        sample = s.drop_duplicates().head(5).tolist()
        print(f"  Примеры: {', '.join(sample)}")
    elif col == "normative":
        num = pd.to_numeric(s, errors="coerce")
        nu = num.dropna()
        uniq = sorted(nu.unique())
        print(f"  Уникальных нормативов в данных: {len(uniq)}")
        print(f"  Минимум: {nu.min():,.0f} тг, максимум: {nu.max():,.0f} тг")
        print(f"  Все значения норматива (тг), по возрастанию:")
        for v in uniq:
            c = int((nu == v).sum())
            print(f"    {v:>15,.0f}  —  {c:,d} заявок")
    elif col == "amount":
        num = pd.to_numeric(s, errors="coerce")
        nu = num.dropna()
        print(f"  Минимум: {nu.min():,.0f} тг")
        print(f"  Максимум: {nu.max():,.0f} тг")
        print(f"  Среднее: {nu.mean():,.0f} тг, медиана: {nu.median():,.0f} тг")
        z = int((nu == 0).sum())
        if z:
            print(f"  Нулевых сумм: {z}")
    print()


def print_categorical_values(df: pd.DataFrame, col: str, name_ru: str, desc: str) -> None:
    print_rule("-")
    print(f"  {col}  —  {name_ru}")
    print(f"  Тип: categorical")
    print()
    print(f"  {desc}")
    print()

    vc = df[col].astype(str).str.strip().value_counts()
    vc = vc.sort_index(key=lambda idx: idx.str.lower())
    n = len(vc)
    total = int(vc.sum())
    print(f"  Всего уникальных значений: {n:,d}  (всего строк с данными: {total:,d})")
    print()
    w = len(str(n))
    for i, (val, cnt) in enumerate(vc.items(), start=1):
        pct = 100.0 * cnt / total if total else 0
        line = val.replace("\n", " ")
        if len(line) > 200:
            line = line[:197] + "..."
        print(f"  {i:>{w}}. [{cnt:>6,d} | {pct:5.1f}%]  {line}")
    print()


def main() -> None:
    schema = asmod.FIELD_SCHEMA
    df = asmod.load_data()

    print_rule()
    print("  СПРАВОЧНИК ПОЛЕЙ — categorical: все значения; остальные: описание + статистика")
    print_rule()
    print(f"  Файл: {asmod.DATA_FILE.name}")
    print(f"  Строк в выборке: {len(df):,d}")
    print()

    # Порядок столбцов как в FIELD_SCHEMA (по индексу Excel)
    for col_idx in sorted(schema.keys()):
        code, name_ru, dtype, _category, desc = schema[col_idx]
        if dtype == "categorical":
            print_categorical_values(df, code, name_ru, desc)
        else:
            describe_non_categorical(df, code, name_ru, desc, dtype)

    print_rule()
    print("  Готово.")
    print_rule()


if __name__ == "__main__":
    main()
