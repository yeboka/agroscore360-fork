"""
AgroScore 360 — Custom CSS for a modern GovTech SaaS look.
"""

CUSTOM_CSS = """
<style>
/* ── Import Google Font ─────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global overrides ───────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Main container ─────────────────────────────────────── */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1200px;
}

/* ── Sidebar styling ────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1b2d 0%, #1a2940 100%);
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: #94a3b8 !important;
    font-weight: 500;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
}

/* ── Metric cards ───────────────────────────────────────── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
[data-testid="stMetric"] label {
    color: #64748b !important;
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 700;
    font-size: 1.6rem;
}

/* ── Tabs ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: #f1f5f9;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.5rem 1.25rem;
    font-weight: 500;
    font-size: 0.9rem;
    color: #475569;
    background: transparent;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #0f172a !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    font-weight: 600;
}

/* ── Buttons ────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.02em;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
    transform: translateY(-1px);
}

/* ── DataFrames / Tables ────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

/* ── Headers ────────────────────────────────────────────── */
h1 {
    color: #0f172a;
    font-weight: 700;
    font-size: 1.8rem !important;
    letter-spacing: -0.02em;
}
h2 {
    color: #1e293b;
    font-weight: 600;
    font-size: 1.35rem !important;
    margin-top: 1.5rem;
}
h3 {
    color: #334155;
    font-weight: 600;
    font-size: 1.1rem !important;
}

/* ── Status badges (used in budget allocation) ──────────── */
.badge-approved {
    background: #dcfce7;
    color: #166534;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.8rem;
}
.badge-reserve {
    background: #fef9c3;
    color: #854d0e;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.8rem;
}
.badge-rejected {
    background: #fee2e2;
    color: #991b1b;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.8rem;
}

/* ── Hero banner ────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f766e 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
}
.hero-banner h1 {
    color: white !important;
    margin: 0 0 0.3rem 0;
    font-size: 1.6rem !important;
}
.hero-banner p {
    color: #94a3b8;
    margin: 0;
    font-size: 0.95rem;
}

/* ── Plotly chart container ─────────────────────────────── */
[data-testid="stPlotlyChart"] {
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    padding: 0.5rem;
    background: white;
}

/* ── Expander ───────────────────────────────────────────── */
.streamlit-expanderHeader {
    font-weight: 600;
    color: #1e293b;
}

/* ── Slider ─────────────────────────────────────────────── */
.stSlider > div > div > div > div {
    background: #2563eb !important;
}
</style>
"""
