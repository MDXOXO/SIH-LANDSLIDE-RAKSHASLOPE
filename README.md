# ⛰️ RakshaSlope — Prototype

### AI-Based Landslide Early Warning & Risk Monitoring System for Northeast India

RakshaSlope is an academic / Smart India Hackathon (SIH) prototype designed to demonstrate an AI-assisted landslide risk monitoring and early-warning workflow for vulnerable regions of Northeast India.

## 🚀 Live Prototype

**Streamlit App:** https://sih-landslide-rakshaslope-8b9q9nv7bbhnteconpy7yn.streamlit.app/

## 🎯 Prototype Capabilities

- Synthetic rainfall and terrain data generation
- Random Forest risk classification
- Simulated live-zone telemetry
- Four risk levels: 🟢 Low / 🟡 Medium / 🟠 High / 🔴 Critical
- Rainfall, slope, elevation and soil-susceptibility inputs
- Interactive risk simulator
- Multilingual warning-message generation
- Alert-centre simulation
- Model probability display
- Interactive Streamlit dashboard

## 🧠 AI/ML Pipeline

```text
Synthetic / Future Real Data
          ↓
Feature Engineering
          ↓
Random Forest Classifier
          ↓
Risk Classification
          ↓
Alert Engine
          ↓
Dashboard + Local-Language Warning
```

### Current model inputs

| Feature | Description |
|---|---|
| Rainfall | Rainfall accumulated over the previous 24 hours |
| Slope | Terrain slope angle in degrees |
| Elevation | Elevation above sea level in metres |
| Soil susceptibility | Prototype factor representing low/medium/high susceptibility |

## 🚨 Risk Levels

| Level | Meaning |
|---|---|
| 🟢 Low | Lower simulated landslide risk |
| 🟡 Medium | Moderate simulated risk; continued monitoring recommended |
| 🟠 High | Elevated simulated risk; alert condition triggered |
| 🔴 Critical | Very high simulated risk; priority alert condition triggered |

## 📡 Current Prototype Zones

The dashboard currently demonstrates simulated telemetry for:

- Cherrapunji North
- Kohima West
- Gangtok South
- Aizawl East

These are **demonstration zones**, not live operational monitoring locations.

## 📱 Multilingual Alerts

The prototype demonstrates localized warning generation for:

- Khasi
- Nagamese
- Mizo
- Nepali
- English fallback

No real SMS is sent by the current prototype.

## ⚠️ Important Limitation

This is a **prototype demonstration**. The current model is trained using synthetic data and an artificial rule for generating training labels. Therefore, model accuracy shown by the application **does not represent real-world landslide prediction accuracy**.

The current version does **not** use live IMD/GSI/Bhuvan data, live sensor feeds, or real emergency-alert infrastructure.

A production system would require validated historical landslide records, meteorological observations, DEM/terrain information, soil and geological data, rigorous model validation, calibration, and operational alert integration.

## 🛠️ Technology Stack

- Python
- NumPy
- Pandas
- Scikit-learn
- Random Forest
- Streamlit

## 📁 Project Structure

```text
SIH-LANDSLIDE-RAKSHASLOPE/
│
├── app.py                 # Interactive Streamlit dashboard
├── one.py                 # Command-line prototype
├── requirements.txt       # Python dependencies
├── run_windows.bat        # Windows launcher
├── README.md              # Project documentation
└── .gitignore
```

## 💻 Run Locally

Python 3.11+ is recommended.

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate it on Windows

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the dashboard

```powershell
streamlit run app.py
```

### 5. Run the command-line version

```powershell
python one.py
```

## 🔮 Future Development

1. Integrate validated real rainfall/weather data.
2. Add historical landslide datasets for supervised learning.
3. Incorporate soil, geology and terrain-derived features.
4. Add 1h, 6h, 24h and 72h rainfall accumulation features.
5. Perform proper cross-validation and model calibration.
6. Evaluate precision, recall, F1-score and false-alert rate on real unseen data.
7. Integrate operational notification infrastructure.
8. Add district-authority and citizen-facing workflows.
9. Develop an auditable alert history and incident log.

## 📌 Project Status

**Current stage:** Functional academic/SIH prototype

The priority of this version is demonstrating the complete workflow from environmental inputs → AI risk classification → monitoring → localized alert generation.

## 📄 License

For academic and prototype use.
