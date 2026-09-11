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

# Separate features and labels
X = df.drop(columns=["label"])
y = df["label"]

# Split the dataset exactly as before
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

# Make predictions on unseen testing data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Generate confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Generate precision, recall and F1-score
report = classification_report(
    y_test,
    y_pred,
    target_names=["NORMAL", "SCAN"]
)

print("=" * 50)
print("MODEL EVALUATION")
print("=" * 50)

print("\nAccuracy:")
print(f"{accuracy:.4f}")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(report)

print("=" * 50)
print("EVALUATION COMPLETE")
print("=" * 50)