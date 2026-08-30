"""
Command-line version of the NER Landslide Early Warning Prototype.

Run:
    python one.py
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def create_training_data(n_samples=2000):
    np.random.seed(42)

    rainfall_24h = np.random.uniform(10, 300, n_samples)
    slope_angle = np.random.uniform(5, 60, n_samples)
    elevation = np.random.uniform(200, 2500, n_samples)
    soil_factor = np.random.choice(
        [1, 2, 3],
        size=n_samples,
        p=[0.30, 0.50, 0.20]
    )

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
        ["Low", "Medium", "High"],
        default="Critical"
    )

    return pd.DataFrame({
        "rainfall_24h": rainfall_24h,
        "slope_angle": slope_angle,
        "elevation": elevation,
        "soil_factor": soil_factor,
        "risk_level": labels
    })


def main():
    df = create_training_data()

    features = [
        "rainfall_24h",
        "slope_angle",
        "elevation",
        "soil_factor"
    ]

    X = df[features]
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

    y_pred = model.predict(X_test)

    print("\n=== MODEL EVALUATION ===")
    print(classification_report(y_test, y_pred, zero_division=0))

    live_zones = pd.DataFrame([
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

    live_zones["predicted_risk"] = model.predict(
        live_zones[features]
    )

    icons = {
        "Low": "GREEN",
        "Medium": "YELLOW",
        "High": "ORANGE",
        "Critical": "RED"
    }

    print("\n=== LIVE DASHBOARD ===")

    for _, row in live_zones.iterrows():
        risk = row["predicted_risk"]

        print(
            f"\n[{row['zone_id']}] {row['zone_name']}"
            f" | {icons[risk]} | {risk}"
        )
        print(
            f"Rainfall: {row['rainfall_24h']} mm/24h"
            f" | Slope: {row['slope_angle']}°"
            f" | Elevation: {row['elevation']} m"
        )

        if risk in ["High", "Critical"]:
            print(
                "ALERT SIMULATED -> District Authority / registered locals"
            )

    print("\nPrototype completed successfully.")


if __name__ == "__main__":
    main()
