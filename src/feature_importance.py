import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the ML-ready dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

# Separate features and labels
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

# Get the importance of every feature
importance = model.feature_importances_

# Create a table containing feature names and their importance
feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": importance
})

# Sort from most important to least important
feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)

print("=" * 50)
print("FEATURE IMPORTANCE")
print("=" * 50)

print("\nFeatures ranked from most important to least important:\n")

for index, row in feature_importance.iterrows():
    print(f"{row['feature']:25} {row['importance']:.4f}")

print("\n" + "=" * 50)
print("FEATURE IMPORTANCE ANALYSIS COMPLETE")
print("=" * 50)