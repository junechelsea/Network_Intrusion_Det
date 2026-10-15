
import pandas as pd

# 1. Load the ML-ready dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

print("=" * 60)
print("NORMAL VS SCAN TRAFFIC ANALYSIS")
print("=" * 60)

# 2. Separate normal traffic from scan traffic
normal = df[df["label"] == 0]
scan = df[df["label"] == 1]

print("\nNumber of normal flows:", len(normal))
print("Number of scan flows:", len(scan))

# 3. Select the features we want to investigate
features = [
    "packet_count",
    "total_bytes",
    "duration",
    "packets_per_second",
    "bytes_per_second",
    "syn_count",
    "ack_count",
    "endpoint_a_port",
    "endpoint_b_port"
]

# 4. Calculate the average values for each class
comparison = pd.DataFrame({
    "NORMAL_mean": normal[features].mean(),
    "SCAN_mean": scan[features].mean(),
    "NORMAL_median": normal[features].median(),
    "SCAN_median": scan[features].median()
})

# 5. Display the comparison
print("\nFEATURE COMPARISON")
print(comparison.round(2).to_string())

# 6. Save the results for later reference
comparison.to_csv("data/feature_comparison.csv")

print("\nResults saved to data/feature_comparison.csv")
print("\nANALYSIS COMPLETE")
