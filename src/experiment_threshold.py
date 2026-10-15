
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# 1. Load the dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

X = df.drop(columns=["label"])
y = df["label"]

# 2. Create the cross-validation strategy
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# 3. Generate out-of-fold scan probabilities
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

probabilities = cross_val_predict(
    model,
    X,
    y,
    cv=cv,
    method="predict_proba"
)

# Find the column representing label 1 (SCAN)
scan_probabilities = probabilities[:, 1]

# 4. Compare several decision thresholds
thresholds = [0.20, 0.30, 0.40, 0.50, 0.60]

print("=" * 60)
print("RANDOM FOREST THRESHOLD EXPERIMENT")
print("=" * 60)

for threshold in thresholds:
    predictions = (scan_probabilities >= threshold).astype(int)

    print(f"\nThreshold: {threshold:.2f}")
    print(f"Accuracy : {accuracy_score(y, predictions):.4f}")
    print(f"Precision: {precision_score(y, predictions, zero_division=0):.4f}")
    print(f"Recall   : {recall_score(y, predictions, zero_division=0):.4f}")
    print(f"F1-score : {f1_score(y, predictions, zero_division=0):.4f}")
    print("Confusion matrix:")
    print(confusion_matrix(y, predictions))

print("\nTHRESHOLD EXPERIMENT COMPLETE")
