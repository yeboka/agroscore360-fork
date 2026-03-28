/**
 * AgroScore 360 — i18n Translation Dictionary
 * Supports: English (en), Kazakh (kk), Russian (ru)
 */
export const translations = {
  en: {
    // Header
    appName:        'AgroScore 360',
    appSubtitle:    'Livestock Subsidy Scoring System',
    ministry:       'Ministry of Agriculture of the Republic of Kazakhstan',
    langLabel:      'Language',

    // KPI Cards
    totalApplicants:  'Total Applicants',
    avgScore:         'Average Score',
    totalRequested:   'Total Requested',
    highScoreCount:   'High Score (≥70)',

    // Budget Allocation
    budgetTitle:      'Smart Budget Allocation',
    budgetLabel:      'Available Budget (KZT)',
    budgetHint:       'Drag the slider to simulate budget scenarios',
    allocated:        'Allocated',
    remaining:        'Remaining',
    approvedCount:    'Approved',
    reserveCount:     'Reserve',
    rejectedCount:    'Rejected',

    // Table
    rank:             '#',
    appNumber:        'App. No.',
    region:           'Region',
    direction:        'Direction',
    headCount:        'Heads',
    amount:           'Requested (KZT)',
    score:            'Score',
    statusCol:        'Status',
    approved:         'Approved',
    reserve:          'Reserve',
    rejected:         'Rejected',
    searchPlaceholder:'Search by region, direction…',
    filterAll:        'All',
    filterApproved:   'Approved',
    filterReserve:    'Reserve',
    filterRejected:   'Rejected',

    // XAI Modal
    xaiTitle:         'Explainability Report',
    xaiSubtitle:      'SHAP feature contributions to the Efficiency Score',
    featureImpact:    'Feature Impact',
    positiveImpact:   'Positive',
    negativeImpact:   'Negative',
    close:            'Close',
    farmerDetails:    'Applicant Details',
    infraIndex:       'Infrastructure Index',
    survivalRate:     'Herd Survival Rate',
    obligations:      'Obligations Met',
    climateRisk:      'Climate Risk Factor',
    efficiencyScore:  'Efficiency Score',
    shapExplain:      'SHAP values show how each feature pushed the score above or below the average baseline.',

    // Feature labels (short)
    feat_infrastructure_index:        'Infrastructure Index',
    feat_herd_survival_rate:          'Herd Survival Rate',
    feat_historical_obligations_met:  'Obligations Fulfilled',
    feat_climate_risk_factor:         'Climate Risk',
    feat_head_count_log:              'Herd Scale (log)',

    // Footer
    footerNote: 'AgroScore 360 — GovTech Hackathon MVP. All data is anonymized.',
  },

  kk: {
    appName:        'AgroScore 360',
    appSubtitle:    'Мал шаруашылығы субсидиясын бағалау жүйесі',
    ministry:       'Қазақстан Республикасы Ауыл шаруашылығы министрлігі',
    langLabel:      'Тіл',

    totalApplicants:  'Барлық өтініш берушілер',
    avgScore:         'Орташа балл',
    totalRequested:   'Жиынтық сұралған',
    highScoreCount:   'Жоғары балл (≥70)',

    budgetTitle:      'Ақылды бюджетті бөлу',
    budgetLabel:      'Қолжетімді бюджет (KZT)',
    budgetHint:       'Бюджет сценарийлерін модельдеу үшін жүгірткіні сүйреңіз',
    allocated:        'Бөлінген',
    remaining:        'Қалған',
    approvedCount:    'Мақұлданған',
    reserveCount:     'Резерв',
    rejectedCount:    'Қабылданбаған',

    rank:             '#',
    appNumber:        'Өтін. №',
    region:           'Облыс',
    direction:        'Бағыт',
    headCount:        'Бас',
    amount:           'Сұралған (KZT)',
    score:            'Балл',
    statusCol:        'Мәртебе',
    approved:         'Мақұлданған',
    reserve:          'Резерв',
    rejected:         'Қабылданбаған',
    searchPlaceholder:'Облыс, бағыт бойынша іздеу…',
    filterAll:        'Барлығы',
    filterApproved:   'Мақұлданған',
    filterReserve:    'Резерв',
    filterRejected:   'Қабылданбаған',

    xaiTitle:         'Түсіндіру есебі',
    xaiSubtitle:      'Тиімділік балына SHAP ерекшелік үлестері',
    featureImpact:    'Ерекшелік әсері',
    positiveImpact:   'Оң',
    negativeImpact:   'Теріс',
    close:            'Жабу',
    farmerDetails:    'Өтініш беруші деректері',
    infraIndex:       'Инфрақұрылым индексі',
    survivalRate:     'Мал сақталуы',
    obligations:      'Міндеттемелер орындалды',
    climateRisk:      'Климаттық тәуекел',
    efficiencyScore:  'Тиімділік балы',
    shapExplain:      'SHAP мәндері әрбір ерекшеліктің орташа базалық деңгейден жоғары немесе төмен балға қалай әсер еткенін көрсетеді.',

    feat_infrastructure_index:        'Инфрақұрылым индексі',
    feat_herd_survival_rate:          'Мал сақталу деңгейі',
    feat_historical_obligations_met:  'Орындалған міндеттемелер',
    feat_climate_risk_factor:         'Климаттық тәуекел',
    feat_head_count_log:              'Табын ауқымы (лог)',

    footerNote: 'AgroScore 360 — GovTech хакатон MVP. Барлық деректер жасырынды.',
  },

  ru: {
    appName:        'AgroScore 360',
    appSubtitle:    'Система оценки субсидий в животноводстве',
    ministry:       'Министерство сельского хозяйства Республики Казахстан',
    langLabel:      'Язык',

    totalApplicants:  'Всего заявок',
    avgScore:         'Средний балл',
    totalRequested:   'Итого запрошено',
    highScoreCount:   'Высокий балл (≥70)',

    budgetTitle:      'Умное распределение бюджета',
    budgetLabel:      'Доступный бюджет (KZT)',
    budgetHint:       'Переместите ползунок для моделирования сценариев',
    allocated:        'Выделено',
    remaining:        'Остаток',
    approvedCount:    'Одобрено',
    reserveCount:     'Резерв',
    rejectedCount:    'Отклонено',

    rank:             '#',
    appNumber:        '№ заявки',
    region:           'Область',
    direction:        'Направление',
    headCount:        'Голов',
    amount:           'Запрошено (KZT)',
    score:            'Балл',
    statusCol:        'Статус',
    approved:         'Одобрено',
    reserve:          'Резерв',
    rejected:         'Отклонено',
    searchPlaceholder:'Поиск по области, направлению…',
    filterAll:        'Все',
    filterApproved:   'Одобрено',
    filterReserve:    'Резерв',
    filterRejected:   'Отклонено',

    xaiTitle:         'Отчёт о прозрачности',
    xaiSubtitle:      'Вклад признаков SHAP в Балл эффективности',
    featureImpact:    'Влияние признака',
    positiveImpact:   'Положительное',
    negativeImpact:   'Отрицательное',
    close:            'Закрыть',
    farmerDetails:    'Данные заявителя',
    infraIndex:       'Индекс инфраструктуры',
    survivalRate:     'Сохранность поголовья',
    obligations:      'Выполнение обязательств',
    climateRisk:      'Климатический риск',
    efficiencyScore:  'Балл эффективности',
    shapExplain:      'Значения SHAP показывают, как каждый признак сдвигает балл выше или ниже среднего базового значения.',

    feat_infrastructure_index:        'Индекс инфраструктуры',
    feat_herd_survival_rate:          'Сохранность поголовья (%)',
    feat_historical_obligations_met:  'Исполнение обязательств',
    feat_climate_risk_factor:         'Климатический риск',
    feat_head_count_log:              'Масштаб стада (лог)',

    footerNote: 'AgroScore 360 — GovTech Хакатон MVP. Все данные анонимизированы.',
  },
}

export const useTranslation = (lang) => (key) => translations[lang]?.[key] ?? translations['en'][key] ?? key
