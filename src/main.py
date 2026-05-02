from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict
import pandas as pd
import numpy as np

from supabase import create_client, Client

# -------- INIT --------
app = FastAPI(title="NetPaySense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- SAFE GLOBALS --------
karnataka = None
models_loaded = True  # disable heavy ML

# -------- PATHS --------
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "Frontend"

# -------- GEO (SAFE) --------
def load_geo_data():
    global karnataka
    try:
        import geopandas as gpd
        from shapely.geometry import Point

        print("Loading geo data...")
        gdf = gpd.read_file(DATA_PATH / "IndiaStatesBoundaryShapes/India_State_Boundary.shp")
        gdf = gdf.to_crs(epsg=4326)
        karnataka = gdf[gdf["STATE"] == "KARNATAKA"]
        print("Geo loaded")

    except Exception as e:
        print("Geo failed:", e)
        karnataka = None

# -------- STARTUP --------
@app.on_event("startup")
async def startup_event():
    print("🔥 APP STARTED")
    threading.Thread(target=load_geo_data, daemon=True).start()

# -------- HEALTH --------
@app.get("/")
def home():
    return {"status": "running"}

# -------- GEO CHECK --------
def isInKarnataka(lat, lon):
    if karnataka is None:
        return True
    try:
        from shapely.geometry import Point
        return karnataka.geometry.contains(Point(lon, lat)).any()
    except:
        return True

# -------- SCHEMA --------
class PredictionRequest(BaseModel):
    lat: float
    lon: float
    bank_name: Optional[str] = None

class BankPredictionRequest(BaseModel):
    bank: str
    lat: float
    lon: float
    network_score: float = 90.0

class FeedbackRequest(BaseModel):
    lat: float
    lon: float
    outcome: str
    metrics: dict

# -------- PREDICT (SAFE MODE) --------
@app.post("/predict")
async def predict(req: PredictionRequest):

    if not isInKarnataka(req.lat, req.lon):
        return JSONResponse(status_code=403, content={
            "status": "out_of_range",
            "message": "Only Karnataka supported"
        })

    # simple dummy safe response
    upi_score = np.random.uniform(60, 95)

    return {
        "lat": req.lat,
        "lon": req.lon,
        "tier": "good" if upi_score > 75 else "mid",
        "upi": f"{upi_score:.1f}%",
        "badge": "SAFE MODE",
        "recommendation": "Models disabled (free plan safe mode)",
        "confidence": "70%",
        "server_version": "safe-mode"
    }

# -------- SPEED TEST --------
@app.get("/pulse-test")
async def pulse_test():
    return {"status": "disabled in free plan"}

# -------- SUPABASE --------
_supabase_url = os.getenv("SUPABASE_URL", "")
_supabase_key = os.getenv("SUPABASE_KEY", "")

try:
    if _supabase_url and _supabase_key:
        supabase: Client = create_client(_supabase_url, _supabase_key)
        print("Supabase connected")
    else:
        supabase = None
except:
    supabase = None

# -------- BANK STATUS --------
@app.get("/bank-status")
async def bank_status():
    if not supabase:
        return {"banks": []}

    try:
        response = supabase.table("bank_health").select("*").limit(20).execute()
        return {"banks": response.data}
    except Exception as e:
        return {"error": str(e)}

# -------- FEEDBACK --------
@app.post("/feedback")
async def submit_feedback(req: FeedbackRequest):
    if not supabase:
        return {"status": "disabled"}

    try:
        supabase.table("feedback").insert({
            "lat": req.lat,
            "lon": req.lon,
            "outcome": req.outcome,
            "metrics": req.metrics,
            "timestamp": datetime.now().isoformat()
        }).execute()

        return {"status": "recorded"}

    except Exception as e:
        return {"error": str(e)}

# -------- FRONTEND --------
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
