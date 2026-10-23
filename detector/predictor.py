
import json
from pathlib import Path

import joblib
import pandas as pd


# Locate project files independently of the terminal's current directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_nids.joblib"
METADATA_PATH = PROJECT_ROOT / "models" / "model_metadata.json"

# Load the existing trained model and its metadata
with open(METADATA_PATH, "r", encoding="utf-8") as file:
    metadata = json.load(file)

model = joblib.load(MODEL_PATH)

FEATURES = metadata["features"]
THRESHOLD = metadata.get("threshold", 0.5)


def prepare_features(flow):
    """Prepare a flow using the exact feature names and order."""

    values = dict(flow)

    # Convert a raw protocol name into the indicators used during training.
    if "protocol" in values:
        protocol = str(values["protocol"]).upper()

        if not any(
            name in values
            for name in ("protocol_1", "protocol_TCP", "protocol_UDP")
        ):
            values["protocol_1"] = int(protocol == "1")
            values["protocol_TCP"] = int(protocol == "TCP")
            values["protocol_UDP"] = int(protocol == "UDP")

    missing = [name for name in FEATURES if name not in values]

    if missing:
        raise ValueError(
            f"Missing required model features: {missing}"
        )

    # Select only the model's expected features, in training order.
    row = {name: values[name] for name in FEATURES}

    return pd.DataFrame([row], columns=FEATURES)


def predict_flow(flow):
    """Predict NORMAL or SCAN and return the confidence values."""

    features = prepare_features(flow)

    probabilities = model.predict_proba(features)[0]

    classes = list(model.classes_)
    scan_index = classes.index(1)
    scan_probability = float(probabilities[scan_index])

    prediction = (
        "SCAN"
        if scan_probability >= THRESHOLD
        else "NORMAL"
    )

    predicted_index = classes.index(
        1 if prediction == "SCAN" else 0
    )

    return {
        "prediction": prediction,
        "confidence": float(probabilities[predicted_index]),
        "scan_probability": scan_probability,
    }


if __name__ == "__main__":
    print("NIDS prediction module loaded successfully.")
    print("Model:", MODEL_PATH.name)
    print("Expected features:", len(FEATURES))
    print("SCAN threshold:", THRESHOLD)
