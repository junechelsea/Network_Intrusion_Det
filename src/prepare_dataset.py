import pandas as pd
import os


NORMAL_FILE = "data/normal_traffic.csv"
ATTACK_FILE = "data/attack_traffic.csv"
OUTPUT_FILE = "data/final_dataset.csv"


print("========================================")
print(" PREPARING FINAL DATASET")
print("========================================")


# Load the datasets
normal_df = pd.read_csv(NORMAL_FILE)
attack_df = pd.read_csv(ATTACK_FILE)


print(f"Normal flows: {len(normal_df)}")
print(f"Attack flows: {len(attack_df)}")


# Check that both datasets have the same columns
normal_columns = list(normal_df.columns)
attack_columns = list(attack_df.columns)

if normal_columns != attack_columns:
    print("\nERROR: The datasets have different columns.")
    print("Normal columns:")
    print(normal_columns)
    print("\nAttack columns:")
    print(attack_columns)
    raise SystemExit


print("\nColumn check: PASSED")


# Combine the datasets
final_df = pd.concat(
    [normal_df, attack_df],
    ignore_index=True
)


# Shuffle the dataset
final_df = final_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# Save the final dataset
final_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n========================================")
print(" FINAL DATASET CREATED")
print("========================================")

print(f"Total flows: {len(final_df)}")

print("\nClass distribution:")
print(final_df["label"].value_counts())

print(f"\nDataset saved to: {OUTPUT_FILE}")

print("\nFirst 5 rows:")
print(final_df.head())