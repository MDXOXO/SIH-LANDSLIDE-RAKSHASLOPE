import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

st.set_page_config(
    page_title="RakshaSlope | Landslide Early Warning",
    page_icon="⛰️",
    layout="wide"
)

# ------------------------------------------------------------
# 1. Synthetic training data
# ------------------------------------------------------------
@st.cache_resource
def train_model():
    np.random.seed(42)
    n_samples = 2000

    rainfall_24h = np.random.uniform(10, 300, n_samples)
    slope_angle = np.random.uniform(5, 60, n_samples)
    elevation = np.random.uniform(200, 2500, n_samples)
    soil_factor = np.random.choice(
        [1, 2, 3],
        size=n_samples,
        p=[0.30, 0.50, 0.20]
    )

    # Prototype rule used only to create synthetic labels.
    # This is NOT a real landslide probability equation.
    risk_score = (
        rainfall_24h * 0.40
        + slope_angle * 1.20
        + (elevation - 200) * 0.006
        + soil_factor * 15
    )

    labels = np.select(
        [
            risk_score < 100,
            risk_score < 140,
            risk_score < 180
        ],
        [
            "Low",
            "Medium",
            "High"
        ],
        default="Critical"
    )

    df = pd.DataFrame({
        "rainfall_24h": rainfall_24h,
        "slope_angle": slope_angle,
        "elevation": elevation,
        "soil_factor": soil_factor,
        "risk_level": labels
    })

    X = df[["rainfall_24h", "slope_angle", "elevation", "soil_factor"]]
    y = df["risk_level"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(
        y_test,
        predictions,
        output_dict=True,
        zero_division=0
    )

    return model, accuracy, report


model, accuracy, report = train_model()

# ------------------------------------------------------------
# 2. Prototype live-zone data
# ------------------------------------------------------------
LIVE_ZONES = pd.DataFrame([
    {
        "zone_id": "NER-Z01",
        "zone_name": "Cherrapunji North",
        "rainfall_24h": 245.0,
        "slope_angle": 42.0,
        "elevation": 1430,
        "soil_factor": 3,
        "language": "Khasi"
    },
    {
        "zone_id": "NER-Z02",
        "zone_name": "Kohima West",
        "rainfall_24h": 120.0,
        "slope_angle": 25.0,
        "elevation": 1444,
        "soil_factor": 2,
        "language": "Nagamese"
    },
    {
        "zone_id": "NER-Z03",
        "zone_name": "Gangtok South",
        "rainfall_24h": 35.0,
        "slope_angle": 15.0,
        "elevation": 1650,
        "soil_factor": 1,
        "language": "Nepali"
    },
    {
        "zone_id": "NER-Z04",
        "zone_name": "Aizawl East",
        "rainfall_24h": 190.0,
        "slope_angle": 38.0,
        "elevation": 1132,
        "soil_factor": 3,
        "language": "Mizo"
    }
])

# ------------------------------------------------------------
# 3. Local alert templates
# ------------------------------------------------------------
LOCAL_SMS_TEMPLATES = {
    "Khasi": "WARNING: High landslide risk detected in {zone}. Avoid unsafe hill roads and move to a safe area if advised.",
    "Nagamese": "WARNING: {zone} te landslide risk high. Pahad rasta avoid koribo aru safe place te thakibo.",
    "Mizo": "WARNING: {zone}-ah landslide hlauhawm a awm. Tlang kawngah fimkhur rawh; an advise chuan himna hmunah kal rawh.",
    "Nepali": "चेतावनी: {zone} क्षेत्रमा पहिरोको जोखिम उच्च छ। पहाडी बाटो प्रयोग नगर्नुहोस् र आवश्यक परे सुरक्षित स्थानमा जानुहोस्।",
    "English": "WARNING: High landslide risk detected in {zone}. Avoid hill roads and move to a safe area if advised."
}

RISK_ICON = {
    "Low": "🟢",
    "Medium": "🟡",
    "High": "🟠",
    "Critical": "🔴"
}

# ------------------------------------------------------------
# 4. RakshaSlope dashboard
# ------------------------------------------------------------
st.title("⛰️ RakshaSlope")
st.subheader("AI-Based Landslide Early Warning & Risk Monitoring System")
st.caption("Northeast India • AI Risk Assessment • Live Monitoring • Multilingual Alerts")

st.warning(
    "Prototype Mode: This demonstration uses synthetic training data and simulated "
    "telemetry. It is not intended for real-world emergency decision-making. "
    "Production deployment would require validated historical landslide records and live data."
)

feature_columns = [
    "rainfall_24h",
    "slope_angle",
    "elevation",
    "soil_factor"
]

X_live = LIVE_ZONES[feature_columns]
LIVE_ZONES["predicted_risk"] = model.predict(X_live)
LIVE_ZONES["model_probability"] = model.predict_proba(X_live).max(axis=1) * 100

critical_count = int((LIVE_ZONES["predicted_risk"] == "Critical").sum())
high_count = int((LIVE_ZONES["predicted_risk"] == "High").sum())
alert_count = critical_count + high_count

c1, c2, c3, c4 = st.columns(4)
c1.metric("Monitored Zones", len(LIVE_ZONES))
c2.metric("Critical Zones", critical_count)
c3.metric("High-Risk Zones", high_count)
c4.metric("Active Alerts", alert_count)

st.divider()

st.subheader("📡 Live Zone Monitoring")

display_df = LIVE_ZONES[
    [
        "zone_id",
        "zone_name",
        "rainfall_24h",
        "slope_angle",
        "elevation",
        "predicted_risk",
        "model_probability"
    ]
].copy()

display_df.columns = [
    "Zone ID",
    "Zone",
    "Rainfall (mm/24h)",
    "Slope (°)",
    "Elevation (m)",
    "Risk Level",
    "Model Probability (%)"
]

display_df["Model Probability (%)"] = display_df["Model Probability (%)"].round(1)

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

st.divider()

st.subheader("🚨 Alert Centre")

for _, row in LIVE_ZONES.iterrows():
    risk = row["predicted_risk"]

    if risk in ["High", "Critical"]:
        message = LOCAL_SMS_TEMPLATES.get(
            row["language"],
            LOCAL_SMS_TEMPLATES["English"]
        ).format(zone=row["zone_name"])

        with st.container(border=True):
            st.markdown(
                f"### {RISK_ICON[risk]} {row['zone_name']} — {risk}"
            )
            st.write("**Simulated alert recipient:** District Authority / registered local users")
            st.write(f"**Language:** {row['language']}")
            st.code(message)
            st.info("Prototype only: no real SMS has been sent.")

st.divider()
st.subheader("🧪 Risk Simulator")
st.caption("Enter hypothetical conditions to test the prototype risk engine.")

left, right = st.columns(2)

with left:
    rainfall = st.slider("Rainfall in last 24 hours (mm)", 0.0, 400.0, 150.0)
    slope = st.slider("Slope angle (degrees)", 0.0, 70.0, 30.0)

with right:
    elevation = st.slider("Elevation (m)", 0, 4000, 1200)
    soil = st.selectbox(
        "Soil susceptibility",
        options=[1, 2, 3],
        format_func=lambda x: {
            1: "1 — Low",
            2: "2 — Medium",
            3: "3 — High"
        }[x]
    )

if st.button("Analyse Risk", type="primary"):
    test_data = pd.DataFrame([{
        "rainfall_24h": rainfall,
        "slope_angle": slope,
        "elevation": elevation,
        "soil_factor": soil
    }])

    prediction = model.predict(test_data)[0]
    probability = model.predict_proba(test_data).max() * 100

    if prediction == "Critical":
        st.error(f"{RISK_ICON[prediction]} Predicted Risk: **{prediction}**")
    elif prediction == "High":
        st.warning(f"{RISK_ICON[prediction]} Predicted Risk: **{prediction}**")
    elif prediction == "Medium":
        st.info(f"{RISK_ICON[prediction]} Predicted Risk: **{prediction}**")
    else:
        st.success(f"{RISK_ICON[prediction]} Predicted Risk: **{prediction}**")

    st.metric("Model Probability", f"{probability:.1f}%")

with st.expander("🧠 Model & Prototype Details"):
    st.write("**Algorithm:** Random Forest Classifier")
    st.write("**Synthetic training samples:** 2,000")
    st.write(f"**Hold-out test accuracy:** {accuracy * 100:.2f}%")
    st.write("**Input features:** rainfall, slope angle, elevation and soil susceptibility.")
    st.write(
        "**Important:** The labels are generated from a synthetic rule. "
        "The accuracy therefore measures how well the Random Forest learned "
        "that artificial rule, not real-world landslide prediction performance."
    )

    report_df = pd.DataFrame(report).transpose().round(3)
    st.dataframe(report_df, width="stretch")

st.divider()
st.caption("RakshaSlope • Academic / SIH Prototype • Northeast India")
