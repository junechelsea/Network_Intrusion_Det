
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the ML-ready dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

# 2. Separate normal and scan traffic
normal = df[df["label"] == 0]
scan = df[df["label"] == 1]

# 3. Choose the features to visualize
features = [
    "packet_count",
    "duration",
    "packets_per_second",
    "bytes_per_second"
]

# 4. Create one boxplot for each feature
for feature in features:
    plt.figure(figsize=(8, 5))

    plt.boxplot(
        [normal[feature], scan[feature]],
        tick_labels=["NORMAL", "SCAN"]
    )

    plt.title(f"{feature}: NORMAL vs SCAN")
    plt.ylabel(feature)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    # Save each graph in the data folder
    plt.savefig(f"data/{feature}_boxplot.png", bbox_inches="tight")

    plt.show()

print("All feature distribution graphs created successfully.")

