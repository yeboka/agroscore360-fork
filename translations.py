"""
AgroScore 360 — Multi-language support (EN / KZ / RU)
All UI strings are stored here for easy scaling.
"""

TRANSLATIONS = {
    # ── App chrome ──────────────────────────────────────────────
    "app_title": {
        "EN": "AgroScore 360 — Livestock Subsidy DSS",
        "KZ": "AgroScore 360 — Мал шаруашылығы субсидиясы DSS",
        "RU": "AgroScore 360 — Субсидирование животноводства DSS",
    },
    "sidebar_title": {
        "EN": "Control Panel",
        "KZ": "Басқару тақтасы",
        "RU": "Панель управления",
    },
    "language_label": {
        "EN": "Language / Тіл / Язык",
        "KZ": "Language / Тіл / Язык",
        "RU": "Language / Тіл / Язык",
    },
    # ── Tab names ───────────────────────────────────────────────
    "tab_dashboard": {
        "EN": "Dashboard",
        "KZ": "Басты бет",
        "RU": "Дашборд",
    },
    "tab_scoring": {
        "EN": "ML Scoring",
        "KZ": "ML Скоринг",
        "RU": "ML Скоринг",
    },
    "tab_explainer": {
        "EN": "XAI Explainer",
        "KZ": "XAI Түсіндіру",
        "RU": "XAI Объяснение",
    },
    "tab_budget": {
        "EN": "Budget Allocation",
        "KZ": "Бюджет бөлу",
        "RU": "Распределение бюджета",
    },
    # ── Dashboard metrics ───────────────────────────────────────
    "total_applications": {
        "EN": "Total Applications",
        "KZ": "Жалпы өтінімдер",
        "RU": "Всего заявок",
    },
    "total_amount": {
        "EN": "Total Subsidies (KZT)",
        "KZ": "Жалпы субсидиялар (₸)",
        "RU": "Общая сумма субсидий (₸)",
    },
    "regions_count": {
        "EN": "Regions",
        "KZ": "Облыстар",
        "RU": "Регионы",
    },
    "avg_score": {
        "EN": "Avg Efficiency Score",
        "KZ": "Орташа тиімділік ұпайы",
        "RU": "Средний балл эффективности",
    },
    "score_distribution": {
        "EN": "Efficiency Score Distribution",
        "KZ": "Тиімділік ұпайларының таралуы",
        "RU": "Распределение баллов эффективности",
    },
    "top_regions": {
        "EN": "Average Score by Region",
        "KZ": "Облыс бойынша орташа ұпай",
        "RU": "Средний балл по регионам",
    },
    "by_direction": {
        "EN": "Applications by Livestock Direction",
        "KZ": "Мал шаруашылығы бағыты бойынша өтінімдер",
        "RU": "Заявки по направлениям животноводства",
    },
    # ── Scoring tab ─────────────────────────────────────────────
    "score_table_title": {
        "EN": "Farmer Efficiency Scores (Top 500)",
        "KZ": "Фермерлердің тиімділік ұпайлары (Топ 500)",
        "RU": "Баллы эффективности фермеров (Топ 500)",
    },
    "col_region": {
        "EN": "Region",
        "KZ": "Облыс",
        "RU": "Область",
    },
    "col_district": {
        "EN": "District",
        "KZ": "Аудан",
        "RU": "Район",
    },
    "col_direction": {
        "EN": "Direction",
        "KZ": "Бағыт",
        "RU": "Направление",
    },
    "col_subsidy_name": {
        "EN": "Subsidy Type",
        "KZ": "Субсидия түрі",
        "RU": "Вид субсидии",
    },
    "col_amount": {
        "EN": "Amount (KZT)",
        "KZ": "Сома (₸)",
        "RU": "Сумма (₸)",
    },
    "col_score": {
        "EN": "Efficiency Score",
        "KZ": "Тиімділік ұпайы",
        "RU": "Балл эффективности",
    },
    "col_status": {
        "EN": "Status",
        "KZ": "Мәртебесі",
        "RU": "Статус",
    },
    "col_infrastructure": {
        "EN": "Infrastructure",
        "KZ": "Инфрақұрылым",
        "RU": "Инфраструктура",
    },
    "col_survival": {
        "EN": "Survival Rate",
        "KZ": "Аман қалу деңгейі",
        "RU": "Выживаемость",
    },
    "col_obligations": {
        "EN": "Obligations Met",
        "KZ": "Міндеттемелер орындалды",
        "RU": "Обязательства выполнены",
    },
    "col_climate_risk": {
        "EN": "Climate Risk",
        "KZ": "Климаттық тәуекел",
        "RU": "Климатический риск",
    },
    "filter_region": {
        "EN": "Filter by Region",
        "KZ": "Облыс бойынша сүзу",
        "RU": "Фильтр по области",
    },
    "filter_direction": {
        "EN": "Filter by Direction",
        "KZ": "Бағыт бойынша сүзу",
        "RU": "Фильтр по направлению",
    },
    "filter_all": {
        "EN": "All",
        "KZ": "Барлығы",
        "RU": "Все",
    },
    # ── XAI Explainer ───────────────────────────────────────────
    "select_farmer": {
        "EN": "Select Application (by row index)",
        "KZ": "Өтінімді таңдаңыз (жол индексі бойынша)",
        "RU": "Выберите заявку (по индексу строки)",
    },
    "shap_title": {
        "EN": "SHAP Feature Contributions",
        "KZ": "SHAP белгілерінің үлесі",
        "RU": "Вклад признаков SHAP",
    },
    "shap_text_title": {
        "EN": "Score Breakdown",
        "KZ": "Ұпай бөлінісі",
        "RU": "Разбор балла",
    },
    "base_score": {
        "EN": "Base Score",
        "KZ": "Базалық ұпай",
        "RU": "Базовый балл",
    },
    "final_score": {
        "EN": "Final Score",
        "KZ": "Қорытынды ұпай",
        "RU": "Итоговый балл",
    },
    "farmer_profile": {
        "EN": "Farmer Profile",
        "KZ": "Фермер профилі",
        "RU": "Профиль фермера",
    },
    # ── Budget Allocation ───────────────────────────────────────
    "budget_input": {
        "EN": "Total Available Budget (KZT)",
        "KZ": "Қолжетімді жалпы бюджет (₸)",
        "RU": "Общий доступный бюджет (₸)",
    },
    "min_score_threshold": {
        "EN": "Minimum Score Threshold",
        "KZ": "Ең аз ұпай шегі",
        "RU": "Минимальный порог балла",
    },
    "status_approved": {
        "EN": "Approved",
        "KZ": "Мақұлданды",
        "RU": "Одобрена",
    },
    "status_reserve": {
        "EN": "Reserve",
        "KZ": "Резерв",
        "RU": "Резерв",
    },
    "status_rejected": {
        "EN": "Rejected",
        "KZ": "Қабылданбады",
        "RU": "Отклонена",
    },
    "budget_summary": {
        "EN": "Budget Allocation Summary",
        "KZ": "Бюджет бөлу қорытындысы",
        "RU": "Итоги распределения бюджета",
    },
    "approved_count": {
        "EN": "Approved Applications",
        "KZ": "Мақұлданған өтінімдер",
        "RU": "Одобренные заявки",
    },
    "reserve_count": {
        "EN": "Reserve Applications",
        "KZ": "Резервтегі өтінімдер",
        "RU": "Заявки в резерве",
    },
    "rejected_count": {
        "EN": "Rejected Applications",
        "KZ": "Қабылданбаған өтінімдер",
        "RU": "Отклонённые заявки",
    },
    "budget_used": {
        "EN": "Budget Used (KZT)",
        "KZ": "Пайдаланылған бюджет (₸)",
        "RU": "Использованный бюджет (₸)",
    },
    "budget_remaining": {
        "EN": "Budget Remaining (KZT)",
        "KZ": "Қалған бюджет (₸)",
        "RU": "Остаток бюджета (₸)",
    },
    "allocation_table": {
        "EN": "Allocation Results",
        "KZ": "Бөлу нәтижелері",
        "RU": "Результаты распределения",
    },
    "run_allocation": {
        "EN": "Run Budget Allocation",
        "KZ": "Бюджет бөлуді іске қосу",
        "RU": "Запустить распределение бюджета",
    },
    # ── Feature names (for SHAP display) ────────────────────────
    "feat_infrastructure_index": {
        "EN": "Infrastructure Index",
        "KZ": "Инфрақұрылым индексі",
        "RU": "Индекс инфраструктуры",
    },
    "feat_herd_survival_rate": {
        "EN": "Herd Survival Rate",
        "KZ": "Мал аман қалу деңгейі",
        "RU": "Выживаемость стада",
    },
    "feat_historical_obligations_met": {
        "EN": "Historical Obligations Met",
        "KZ": "Тарихи міндеттемелер орындалды",
        "RU": "Исторические обязательства выполнены",
    },
    "feat_climate_risk_factor": {
        "EN": "Climate Risk Factor",
        "KZ": "Климаттық тәуекел факторы",
        "RU": "Фактор климатического риска",
    },
    "feat_normatif_per_head": {
        "EN": "Subsidy Rate per Head",
        "KZ": "Бас басына субсидия мөлшерлемесі",
        "RU": "Норматив субсидии на голову",
    },
    "feat_amount_requested": {
        "EN": "Amount Requested",
        "KZ": "Сұралған сома",
        "RU": "Запрашиваемая сумма",
    },
    "feat_direction_encoded": {
        "EN": "Livestock Direction",
        "KZ": "Мал шаруашылығы бағыты",
        "RU": "Направление животноводства",
    },
    "feat_region_encoded": {
        "EN": "Region",
        "KZ": "Облыс",
        "RU": "Область",
    },
    "model_training": {
        "EN": "Training ML model...",
        "KZ": "ML моделі оқытылуда...",
        "RU": "Обучение ML модели...",
    },
    "data_loading": {
        "EN": "Loading and processing data...",
        "KZ": "Деректерді жүктеу және өңдеу...",
        "RU": "Загрузка и обработка данных...",
    },
}


def t(key: str, lang: str = "EN") -> str:
    """Get translated string. Falls back to EN if key/lang missing."""
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get("EN", key))
