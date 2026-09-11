import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the ML-ready dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

# Separate features from the target
X = df.drop(columns=["label"])
y = df["label"]

# Split the dataset
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

print("=" * 50)
print("MODEL TRAINING COMPLETE")
print("=" * 50)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nNumber of trees:", model.n_estimators)

print("\nModel successfully learned from the training data.")