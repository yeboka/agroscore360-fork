"""
AgroScore 360 — FastAPI Backend
================================
Serves the scored farmer list with SHAP explanations.

Endpoints:
  GET  /              → health check
  GET  /api/farmers   → list of all scored farmers (JSON)
  GET  /api/stats     → aggregate statistics for the dashboard KPI cards
  GET  /api/farmer/{id} → single farmer detail (full SHAP breakdown)

Run with:
  uvicorn main:app --reload --port 8000
"""

import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import get_farmers

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR  = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "subsidies_2025.xlsx"

# ---------------------------------------------------------------------------
# Startup: pre-load & score the dataset once
# ---------------------------------------------------------------------------
farmers_cache: list[dict] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model and data once at startup."""
    global farmers_cache
    if not DATA_PATH.exists():
        print(f"[WARN] Dataset not found at {DATA_PATH}. API will return empty list.")
        farmers_cache = []
    else:
        farmers_cache = get_farmers(str(DATA_PATH))
    yield   # app is running
    # Cleanup (none needed)


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AgroScore 360 API",
    description="Merit-based subsidy scoring system for the Ministry of Agriculture of Kazakhstan",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the React dev server (port 5173) and any localhost origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "AgroScore 360 API",
        "farmers_loaded": len(farmers_cache),
    }


@app.get("/api/farmers", tags=["Farmers"])
def list_farmers():
    """
    Return the full scored list of subsidy applicants, sorted by
    efficiency_score descending.

    Each farmer object includes:
      - id, app_number, region, district, subsidy_direction, status
      - amount (KZT requested), efficiency_score (0–100)
      - infrastructure_index, herd_survival_rate, historical_obligations_met,
        climate_risk_factor  (engineered features from subsidy rules)
      - shap_values  (feature contribution breakdown for XAI panel)
    """
    if not farmers_cache:
        return []
    # Already sorted by score descending from model.py
    return farmers_cache


@app.get("/api/stats", tags=["Statistics"])
def get_stats():
    """
    Aggregate KPI statistics for the dashboard header cards.
    """
    if not farmers_cache:
        return {}

    scores = [f["efficiency_score"] for f in farmers_cache]
    amounts = [f["amount"] for f in farmers_cache]

    high    = sum(1 for s in scores if s >= 70)
    medium  = sum(1 for s in scores if 50 <= s < 70)
    low     = sum(1 for s in scores if s < 50)

    return {
        "total_applicants":     len(farmers_cache),
        "avg_score":            round(sum(scores) / len(scores), 1),
        "total_requested_kzt":  int(sum(amounts)),
        "high_score_count":     high,
        "medium_score_count":   medium,
        "low_score_count":      low,
        "score_distribution":   {
            "bins":   ["0–20", "20–40", "40–60", "60–80", "80–100"],
            "counts": [
                sum(1 for s in scores if s < 20),
                sum(1 for s in scores if 20 <= s < 40),
                sum(1 for s in scores if 40 <= s < 60),
                sum(1 for s in scores if 60 <= s < 80),
                sum(1 for s in scores if s >= 80),
            ],
        },
    }


@app.get("/api/farmer/{farmer_id}", tags=["Farmers"])
def get_farmer(farmer_id: int):
    """
    Return a single farmer's full detail including SHAP breakdown.
    """
    match = next((f for f in farmers_cache if f["id"] == farmer_id), None)
    if match is None:
        raise HTTPException(status_code=404, detail=f"Farmer {farmer_id} not found")
    return match
