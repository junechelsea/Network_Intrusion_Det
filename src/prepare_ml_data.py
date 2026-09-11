import pandas as pd

# Load the final dataset
df = pd.read_csv("data/final_dataset.csv")

print("Original dataset size:")
print(df.shape)

# Remove duplicate flows
df = df.drop_duplicates()

print("\nAfter removing duplicates:")
print(df.shape)

# Remove IP address features
df = df.drop(columns=[
    "endpoint_a_ip",
    "endpoint_b_ip"
])

# Convert protocol into numerical features
df = pd.get_dummies(
    df,
    columns=["protocol"],
    dtype=int
)

# Convert labels into numbers
df["label"] = df["label"].map({
    "NORMAL": 0,
    "SCAN": 1
})

# Save the ML-ready dataset
df.to_csv(
    "data/ml_ready_dataset.csv",
    index=False
)

print("\nML-ready dataset saved successfully.")
print("Final shape:", df.shape)

print("\nLabel distribution:")
print(df["label"].value_counts())