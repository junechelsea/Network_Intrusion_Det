
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# 1. Load the ML-ready dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

# 2. Separate features and labels
X = df.drop(columns=["label"])
y = df["label"]

# 3. Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 4. Create a balanced Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced",
    random_state=42
)

# 5. Train the model
model.fit(X_train, y_train)

# 6. Predict the test labels
y_pred = model.predict(X_test)

# 7. Evaluate the results
print("=" * 50)
print("BALANCED RANDOM FOREST EXPERIMENT")
print("=" * 50)

print("\nAccuracy:")
print(f"{accuracy_score(y_test, y_pred):.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["NORMAL", "SCAN"],
    zero_division=0
))

print("=" * 50)
print("EXPERIMENT COMPLETE")
print("=" * 50)
