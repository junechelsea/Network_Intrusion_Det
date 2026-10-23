
import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# Project paths
DATA_PATH = Path("data/ml_ready_dataset.csv")
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "random_forest_nids.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.json"

# Load the ML-ready dataset
df = pd.read_csv(DATA_PATH)

# Separate features from the target
X = df.drop(columns=["label"])
y = df["label"]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# Create the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
)

# Train the model
model.fit(X_train, y_train)

# Evaluate on the held-out test set
y_pred = model.predict(X_test)

print("=" * 50)
print("MODEL TRAINING AND EVALUATION")
print("=" * 50)

print("\nTotal samples:", len(df))
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Number of trees:", model.n_estimators)

print("\nClass distribution:")
print(y.value_counts().sort_index())

print("\nAccuracy:", round(accuracy_score(y_test, y_pred), 4))

print("\nClassification report:")
print(
    classification_report(
        y_test,
        y_pred,
        labels=[0, 1],
        target_names=["NORMAL", "SCAN"],
        zero_division=0,
    )
)

print("Confusion matrix (rows=actual, columns=predicted):")
print("Labels: 0=NORMAL, 1=SCAN")
print(confusion_matrix(y_test, y_pred, labels=[0, 1]))

# Create the model directory if it doesn't exist
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Save the trained model
joblib.dump(model, MODEL_PATH)

# Save the feature names and training configuration
metadata = {
    "model_type": "RandomForestClassifier",
    "n_estimators": model.n_estimators,
    "random_state": 42,
    "dataset": str(DATA_PATH),
    "features": list(X.columns),
    "classes": [int(value) for value in model.classes_],
    "threshold": 0.5,
    "training_samples": int(len(X_train)),
    "testing_samples": int(len(X_test)),
}

with open(METADATA_PATH, "w", encoding="utf-8") as file:
    json.dump(metadata, file, indent=4)

print("\nModel saved to:", MODEL_PATH)
print("Metadata saved to:", METADATA_PATH)
print("\nTraining and saving complete.")
