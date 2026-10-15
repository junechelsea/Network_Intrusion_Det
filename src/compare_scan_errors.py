
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict

# 1. Load the prepared dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

X = df.drop(columns=["label"])
y = df["label"]

# 2. Use the same cross-validation setup
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 3. Generate predictions for unseen folds
predictions = cross_val_predict(
    model,
    X,
    y,
    cv=cv
)

# 4. Separate the dataset into three groups
normal = df[y == 0].drop(columns=["label"])

detected_scans = df[(y == 1) & (predictions == 1)].drop(
    columns=["label"]
)

missed_scans = df[(y == 1) & (predictions == 0)].drop(
    columns=["label"]
)

# 5. Compare selected features
features = [
    "packet_count",
    "total_bytes",
    "duration",
    "packets_per_second",
    "bytes_per_second",
    "syn_count",
    "ack_count",
    "endpoint_a_port",
    "endpoint_b_port",
]

groups = {
    "NORMAL": normal,
    "DETECTED_SCAN": detected_scans,
    "MISSED_SCAN": missed_scans,
}

print("=" * 65)
print("COMPARISON OF NORMAL, DETECTED, AND MISSED FLOWS")
print("=" * 65)

print("\nNumber of flows in each group:")
for name, group in groups.items():
    print(f"{name}: {len(group)}")

for feature in features:
    print(f"\n{feature}")
    print("-" * 45)

    for name, group in groups.items():
        print(
            f"{name:15} "
            f"mean={group[feature].mean():12.2f} "
            f"median={group[feature].median():12.2f}"
        )

print("\nCOMPARISON COMPLETE")
