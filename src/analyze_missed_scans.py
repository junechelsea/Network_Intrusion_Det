
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import confusion_matrix, classification_report

# 1. Load the prepared dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

X = df.drop(columns=["label"])
y = df["label"]

# 2. Use five-fold stratified cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# 3. Generate predictions for flows not used to train
# the model that predicts them
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

predictions = cross_val_predict(
    model,
    X,
    y,
    cv=cv
)

# 4. Display overall performance
print("=" * 60)
print("MISSED SCAN ANALYSIS")
print("=" * 60)

print("\nClassification report:")
print(classification_report(
    y,
    predictions,
    target_names=["NORMAL", "SCAN"],
    zero_division=0
))

print("\nConfusion matrix (rows = actual, columns = predicted):")
print(confusion_matrix(y, predictions))

# 5. Find scans incorrectly predicted as normal
missed_scans = df[(y == 1) & (predictions == 0)].copy()

print(f"\nTotal scan flows: {(y == 1).sum()}")
print(f"Missed scan flows: {len(missed_scans)}")

# 6. Examine the characteristics of missed scans
if not missed_scans.empty:
    print("\nAverage features of missed scans:")
    print(
        missed_scans.drop(columns=["label"])
        .mean()
        .round(2)
        .to_string()
    )

    print("\nFirst 10 missed scan flows:")
    print(missed_scans.head(10).to_string(index=False))

print("\nMISSED SCAN ANALYSIS COMPLETE")
