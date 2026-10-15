
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate

# 1. Load the dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

X = df.drop(columns=["label"])
y = df["label"]

# 2. Create five stratified folds
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# 3. Choose the metrics to evaluate
scoring = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1"
}

# 4. Compare both model configurations
models = {
    "Original Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),
    "Balanced Random Forest": RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    )
}

# 5. Evaluate each model across five folds
for name, model in models.items():
    results = cross_validate(
        model,
        X,
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

print("\nCROSS-VALIDATION COMPLETE")
