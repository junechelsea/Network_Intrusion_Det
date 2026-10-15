
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate

# Load the cleaned dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

X = df.drop(columns=["label"])
y = df["label"]

# Use the same five folds for both experiments
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scoring = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1"
}

# Experiment A: Keep port features
X_with_ports = X.copy()

# Experiment B: Remove port features
X_without_ports = X.drop(columns=[
    "endpoint_a_port",
    "endpoint_b_port"
])

experiments = {
    "WITH PORTS": X_with_ports,
    "WITHOUT PORTS": X_without_ports
}

for name, features in experiments.items():
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    results = cross_validate(
        model,
        features,
        y,
        cv=cv,
        scoring=scoring
    )

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    for metric in scoring:
        scores = results[f"test_{metric}"]

        print(
            f"{metric.capitalize():12}: "
            f"{scores.mean():.4f} "
            f"(standard deviation: {scores.std():.4f})"
        )

print("\nPORT FEATURE CROSS-VALIDATION COMPLETE")
