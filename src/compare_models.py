
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_validate

# 1. Load the dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

X = df.drop(columns=["label"])
y = df["label"]

# 2. Use the same five folds for every model
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# 3. Define the evaluation metrics
scoring = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1"
}

# 4. Define the models
models = {
    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Logistic Regression": make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000)
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
}

# 5. Train and evaluate each model
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

print("\nMODEL COMPARISON COMPLETE")
