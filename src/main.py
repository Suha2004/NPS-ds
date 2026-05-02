from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import threading
from datetime import datetime
from typing import Optional, Dict

import pandas as pd
import numpy as np
from pathlib import Path

# Optional imports
try:
    from .bank_monitor import fetch_bank_health, get_bank_upi_status, clean_old_data
except:
    from bank_monitor import fetch_bank_health, get_bank_upi_status, clean_old_data

# -------- PATHS --------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "Frontend"

app = FastAPI(title="NetPaySense API")

# -------- CORS --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- STARTUP --------
@app.on_event("startup")
async def startup_event():
    print("🚀 APP STARTED")

    try:
        clean_old_data()
        threading.Thread(target=fetch_bank_health, daemon=True).start()
    except Exception as e:
        print("Startup warning:", e)

# -------- LIGHT KARNATAKA CHECK --------
def isInKarnataka(lat: float, lon: float) -> bool:
    return 11.5 <= lat <= 18.5 and 74 <= lon <= 78.5

# -------- LOAD DATA --------
look_up_df = pd.read_csv(DATA_PATH / 'final_dataset.csv')

look_up_df['download_mbps'] = look_up_df['avg_d_kbps'] / 1000
look_up_df['upload_mbps'] = look_up_df['avg_u_kbps'] / 1000
look_up_df['latency_ms'] = look_up_df['avg_lat_ms']

look_up_df = look_up_df[
    (look_up_df['download_mbps'] > 0) &
    (look_up_df['latency_ms'] > 0)
]

# -------- SCHEMA --------
class PredictionRequest(BaseModel):
    lat: float
    lon: float
    bank_name: Optional[str] = None
    live_metrics: Optional[Dict] = None

# -------- UI LOGIC --------
def get_ui_data(upi_score):
    if upi_score < 45:
        return {"tier": "poor", "badge": "High Risk", "rec": "Carry cash backup"}
    elif upi_score < 75:
        return {"tier": "mid", "badge": "Medium Risk", "rec": "Proceed with caution"}
    else:
        return {"tier": "good", "badge": "Low Risk", "rec": "Safe to proceed"}

# -------- MAIN PREDICT --------
@app.post("/predict")
async def predict(req: PredictionRequest):

    if not isInKarnataka(req.lat, req.lon):
        return JSONResponse(status_code=403, content={
            "status": "out_of_range",
            "message": "Available only in Karnataka"
        })

    try:
        # -------- SIMPLE NEAREST POINT (NO SCIPY) --------
        nearest = look_up_df.iloc[
            ((look_up_df['lat'] - req.lat)**2 + (look_up_df['lon'] - req.lon)**2).idxmin()
        ]

        dn = nearest['download_mbps']
        up = nearest['upload_mbps']
        lat = nearest['latency_ms']

        # Override with live metrics
        if req.live_metrics:
            dn = req.live_metrics.get('download', dn)
            up = req.live_metrics.get('upload', up)
            lat = req.live_metrics.get('latency', lat)

        # -------- UPI SCORE --------
        BASE = 95

        lat_penalty = min(lat / 2, 70)
        up_penalty = 0 if up > 2 else (20 if up > 1 else 40)
        dn_penalty = 0 if dn > 2 else 10

        upi_score = BASE - lat_penalty - up_penalty - dn_penalty
        upi_score = max(5, min(99, upi_score))

        ui = get_ui_data(upi_score)

        # -------- BANK CHECK --------
        bank_warning = None
        if req.bank_name:
            try:
                status, _ = get_bank_upi_status(req.bank_name)
                if status == "DOWN":
                    ui["tier"] = "poor"
                    ui["badge"] = "CRITICAL"
                    ui["rec"] = "Bank server down"
                    bank_warning = f"{req.bank_name} DOWN"
            except:
                pass

        return {
            "lat": float(nearest['lat']),
            "lon": float(nearest['lon']),
            "tier": ui["tier"],
            "upi": f"{upi_score:.1f}%",
            "badge": ui["badge"],
            "recommendation": ui["rec"],
            "confidence": "80%",
            "bank_warning": bank_warning,
            "server_version": "final-safe"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------- HEALTH --------
@app.get("/health")
def health():
    return {"status": "running"}

# -------- FRONTEND --------
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
