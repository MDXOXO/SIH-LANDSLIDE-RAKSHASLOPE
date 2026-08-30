# NER Landslide Early Warning System — Prototype

An academic/SIH prototype for a **North-East India landslide early warning system** using:

- Synthetic terrain and rainfall data
- Random Forest classification
- Simulated live telemetry
- Risk levels: Low / Medium / High / Critical
- Multilingual alert templates
- Interactive Streamlit dashboard

## Important limitation

This prototype **does not use real-time IMD/GSI/Bhuvan data** and does not send real SMS.

The training labels are generated using an artificial rule so that the machine-learning pipeline can be demonstrated. The reported model accuracy therefore does **not** represent real-world landslide prediction accuracy.

## Project files

- `app.py` — interactive Streamlit dashboard
- `one.py` — command-line version
- `requirements.txt` — required Python packages
- `README.md` — project documentation

## Run locally

Python 3.11+ is recommended.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install packages:

```powershell
python -m pip install -r requirements.txt
```

Run the command-line prototype:

```powershell
python one.py
```

Run the dashboard:

```powershell
streamlit run app.py
```

## Suggested future upgrades

1. Replace synthetic rainfall with real weather/rain-gauge/API data.
2. Add DEM-derived slope/elevation data.
3. Add soil/geology and historical landslide records.
4. Train and validate against real GSI/state disaster-management datasets.
5. Add GIS map layers.
6. Add time-series rainfall accumulation: 1h, 6h, 24h, 72h.
7. Add rainfall intensity thresholds and antecedent rainfall.
8. Connect the alert service to a real SMS gateway.
9. Add user registration and district-authority dashboards.
10. Calibrate the model and evaluate precision, recall, F1 and false-alert rate on unseen real data.

## Prototype architecture

Data Sources
    ↓
Feature Extraction
    ↓
Risk Model
    ↓
Risk Classification
    ↓
Dashboard + Local-Language Alert
    ↓
District Authority / Registered Users

## License

For academic and prototype use.
