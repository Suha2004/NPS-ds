from fastapi import FastAPI
import torch
import joblib
import numpy as np

app = FastAPI()

# -------- MODEL (EXACT SAME AS TRAINING) --------
class OoklaNN(torch.nn.Module):
    def __init__(self, input_size):
        super(OoklaNN, self).__init__()
        self.network = torch.nn.Sequential(
            torch.nn.Linear(input_size, 64),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.15),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.1),
            torch.nn.Linear(32, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 3)
        )

    def forward(self, x):
        return self.network(x)

# -------- LOAD MODEL --------
model = OoklaNN(input_size=6)
model.load_state_dict(torch.load("ookla_nn.pth"))
model.eval()

# -------- LOAD SCALER --------
scaler = joblib.load("ookla_scaler.pkl")

# -------- HOME --------
@app.get("/")
def home():
    return {"message": "NetPaySense API is running 🚀"}

# -------- PREDICT --------
@app.post("/predict")
def predict(data: dict):
    try:
        # Input
        upload_mbps = data["upload_mbps"]
        lat = data["lat"]
        lon = data["lon"]
        latency = data["latency_ms"]

        # Feature engineering (same as training)
        upload_latency_ratio = upload_mbps / (latency + 1)

        if latency < 50:
            latency_bucket = 0
        elif latency < 100:
            latency_bucket = 1
        else:
            latency_bucket = 2

        geo_interaction = lat * lon

        # Final feature array
        features = np.array([[upload_mbps, lat, lon,
                              upload_latency_ratio,
                              latency_bucket,
                              geo_interaction]])

        # Scale
        features_scaled = scaler.transform(features)

        # Predict
        with torch.no_grad():
            output = model(torch.tensor(features_scaled, dtype=torch.float32))
            _, pred = torch.max(output, 1)

        label_map = {0: "poor", 1: "average", 2: "good"}

        return {
            "prediction": label_map[int(pred)],
            "status": "success"
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
        