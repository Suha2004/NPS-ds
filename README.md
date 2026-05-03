<<<<<<< HEAD
---
title: NetPaySense API
emoji: 🛰️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# 🛰️ NetPaySense: AI-Powered UPI Reliability Checker (v5.2 Edge Edition)

**NetPaySense** is a real-time diagnostic platform designed to predict the success probability of UPI payments with localized intelligence. It combines **Dual-Model Machine Learning (Neural Networks + KDTree)**, **Live Bank Pulse Monitoring**, and a **Cloudflare Global Edge Speed Test** to provide a premium, accessible payment safety dashboard.

---

## 🚀 Key Features (v5.2)

- **⚡ Global Edge Speed Test (New in v5.2)**: Completely bypasses slow cloud server bottlenecks by utilizing Cloudflare's massive Anycast edge network (`speed.cloudflare.com`). Delivers Fast.com-level accuracy (100+ Mbps) and pure local network latency (~30ms) directly from the mobile browser.
- **🌍 Multilingual Intelligence**: Full native support for **Kannada, Hindi, Tamil, and Telugu**, including localized analytics and dynamic UI recommendations.
- **🎯 Precision Risk Meter**: A state-of-the-art canvas-based gauge providing real-time risk visualization (Low/Medium/High) based on real-world network physics.
- **🗺️ Smart Network Map**: AI-suggested "Better Network Zones" visualized on a live map, recommending the absolute best signal spot within 50 meters.
- **🏦 Real-time Bank Pulse**: Live 15-minute background health monitoring of major Indian banks (SBI, HDFC, ICICI, etc.) synced seamlessly via Supabase.
- **🚨 Community Failure Alerts**: Crowd-sourced regional failure detection that warns users if nearby payments are failing in real-time.
- **🗼 Dynamic Tower Intelligence**: Real-time nearest cell tower detection via OpenCellID API, mapping MNC/MCC codes to major Indian operators (Airtel, Jio, BSNL, Vi) for hyper-local network switching recommendations.
- **✨ Premium Glassmorphism UI**: A high-end, native-app-like mobile-first design system with optimized Dark/Light modes.
=======
# 🛰️ NetPaySense: AI-Powered UPI Reliability Checker (v4.3 Pro)

**NetPaySense** is a real-time diagnostic platform designed to predict the success probability of UPI payments with localized intelligence. It combines **Dual-Model Machine Learning (Neural Networks + KDTree)** with **Live Bank Pulse Monitoring** and **Multilingual v4.2 Localization** to provide a premium, accessible payment safety dashboard.

---

## 🚀 Key Features (v4.2 Pro)
- **🌍 Multilingual Intelligence**: Full native support for **Kannada, Hindi, Tamil, and Telugu**, including localized analytics and recommendations.
- **🎯 Precision Risk Meter**: A state-of-the-art canvas-based gauge providing real-time risk visualization (Low/Medium/High) based on network physics.
- **🗺️ Smart Network Map**: AI-suggested "Better Network Zones" visualized on a live map, recommending the absolute best signal spot within 50 meters.
- **🏦 Real-time Bank Pulse**: Live 120-second health monitoring of major Indian banks (SBI, HDFC, ICICI, etc.) synced via Supabase.
- **🚨 Community Failure Alerts**: Crowd-sourced regional failure detection that warns users if nearby payments are failing in real-time.
- **🗼 Tower Intelligence**: Real-time nearest cell tower detection via OpenCellID API, mapping MNC/MCC codes to major Indian operators (Airtel, Jio, BSNL, Vi) for hyper-local network recommendations.
- **✨ Premium Glassmorphism UI**: A high-end, mobile-first design system with optimized Dark/Light modes and v4.3 performance parallelization.
>>>>>>> fixed-ui

---

## 🛠️ Technology Stack
<<<<<<< HEAD

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+) with Uvicorn
- **Database**: [Supabase](https://supabase.com/) (Real-time PostgreSQL)
- **AI/ML Engine**: [scikit-learn](https://scikit-learn.org/) (Neural Feature Scaling) + [KDTree](https://scipy.org/) (Spatial Optimization)
- **GIS Logic**: [GeoPandas](https://geopandas.org/), [Shapely](https://shapely.readthedocs.io/)
- **Frontend**: Vanilla ES6+ JavaScript, Modern CSS3 (Glassmorphism), [Leaflet.js](https://leafletjs.com/) for mapping.
- **Diagnostics**: Cloudflare Edge Network (`1.1.1.1` trace & `speed.cloudflare.com` payloads)
=======
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Database**: [Supabase](https://supabase.com/) (Real-time PostgreSQL)
- **AI/ML Engine**: [PyTorch](https://pytorch.org/) (Neural Feature Mapping) + [KDTree](https://scipy.org/) (Spatial Optimization)
- **GIS Logic**: [GeoPandas](https://geopandas.org/), [Shapely](https://shapely.readthedocs.io/)
- **Frontend**: ES6+ JavaScript, Modern CSS3 (Glassmorphism), [Leaflet.js](https://leafletjs.com/)
>>>>>>> fixed-ui

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/gvs-manashwi-roy/NetPaySense.git
cd NetPaySense
```

<<<<<<< HEAD
### 2. Set Up Environment Variables
Create a `.env` file in the root directory with your required credentials:
```bash
# Required for database connections
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Required for dynamic mobile operator tower tracking
=======
### 2. Set Up Environment
Create a `.env` file in the root directory with your Supabase credentials:
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
>>>>>>> fixed-ui
OPENCELL_API_KEY=your_API_KEY
```

### 3. Run the Backend
```bash
<<<<<<< HEAD
# Set up a virtual environment
=======
# Set up virtual environment
>>>>>>> fixed-ui
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

<<<<<<< HEAD
# Start the server (runs on port 7860 to match Hugging Face standard)
$env:PYTHONPATH="src"; python -m uvicorn src.main:app --host 0.0.0.0 --port 7860 --reload
=======
# Start the server
$env:PYTHONPATH="src"; python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
>>>>>>> fixed-ui
```

---

## 🔌 API Intelligence
<<<<<<< HEAD

- `POST /predict`: Neural-Spatial prediction. Calculates overall UPI success probability based on Edge Ping and Download/Upload bandwidth. Returns `better_location` for the Smart Map.
- `POST /bank-predict`: Hybrid scoring that downgrades network reliability if real-time bank server health is struggling.
- `GET /bank-status`: Returns a live JSON feed of bank health statuses scraped and persisted in Supabase.
- `GET /test-download` & `POST /test-upload`: Legacy backend speed endpoints (now superseded by client-side Cloudflare tests, kept for system health diagnostics).
- `POST /feedback`: Records local payment outcomes for Community Alerts and future Reinforcement Learning.
=======
- `POST /predict`: Neural-Spatial prediction. Returns `better_location` for the Smart Map and localized signal tiers.
- `POST /bank-predict`: Hybrid scoring that weights network latency against real-time bank server health.
- `GET /bank-status`: Returns a live JSON feed of bank health statuses persisted in Supabase.
- `GET /pulse-test`: Real-time network probe (speedtest) to verify live latency and operator stats.
- `POST /feedback`: Records local payment outcomes for Reinforcement Learning and Community Alerts.
>>>>>>> fixed-ui

---

## 🧠 Risk Assessment Logic
<<<<<<< HEAD

The **UPI Success Chance** is determined by a deterministic physics and probability model:
1. **Edge Latency Thresholds**: 
   - < 50ms: Excellent (Green)
   - 100ms - 150ms: Risky (Amber/Yellow)
   - \> 200ms: Critical Failure Risk (Red)
2. **Bandwidth Requirements**: Minimum 1.0 Mbps upload required for consistent, timeout-free payment handshakes.
3. **Smart Spatial Optimization**: KDTree identifies the best performance neighbor among the 10 nearest spatial data points to suggest physical movement for better signal.
4. **Bank Server Override**: High network quality is automatically and drastically downgraded if the selected bank's UPI server is reporting `DOWN` or `FLUCTUATING` from the background scraper.
5. **Operator Awareness**: Uses live MNC/MCC data from OpenCellID to identify the nearest operator tower, providing dynamic switching recommendations (e.g., "Switch to Airtel") instead of generic suggestions.

---

## 📄 License
This project is proprietary. All rights reserved. See the [LICENSE](LICENSE) file for details.
=======
The **UPI Success Chance** is determined by a deterministic physics model:
1. **Latency Thresholds**: 
   - < 50ms: Excellent (Green)
   - 100ms - 150ms: Risky (Amber/Yellow)
   - \> 200ms: Critical Failure Risk (Red)
2. **Bandwidth Requirements**: Minimum 1.0 Mbps upload required for consistent payment handshakes.
3. **Smart Optimization**: KDTree identifies the best performance neighbor among the 10 nearest spatial data points.
4. **Bank Override**: High network quality is automatically downgraded if the selected bank's UPI server is reporting `DOWN` or `FLUCTUATING`.
5. **Operator Awareness**: Uses live MNC/MCC data from OpenCellID to identify the nearest operator tower, providing dynamic recommendations (e.g., "Use Airtel") instead of generic suggestions.
>>>>>>> fixed-ui

---

## 🤝 Contributors
<<<<<<< HEAD
*Developed with ❤️ by the NetPaySense Team. Architecture optimizations (v4 - v5.2) designed in collaboration with Google DeepMind (Advanced Agentic Coding).*
=======
*Developed with ❤️ by the NetPaySense Team. v4.2 Localization by Google DeepMind (Advanced Agentic Coding).*
>>>>>>> fixed-ui
