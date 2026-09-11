import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load the ML-ready dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

# Remove port features for this experiment
df = df.drop(columns=[
    "endpoint_a_port",
    "endpoint_b_port"
])

# Separate features from the target
X = df.drop(columns=["label"])
y = df["label"]

# Use the same train/test split as our baseline model
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Create the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the unseen test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Generate confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Generate classification report
report = classification_report(
    y_test,
    y_pred,
    target_names=["NORMAL", "SCAN"]
)

print("=" * 50)
print("NO-PORTS EXPERIMENT")
print("=" * 50)

print("\nFeatures used:")
for feature in X.columns:
    print("-", feature)

print("\nNumber of features:", X.shape[1])

print("\nAccuracy:")
print(f"{accuracy:.4f}")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(report)

print("=" * 50)
print("NO-PORTS EXPERIMENT COMPLETE")
print("=" * 50)