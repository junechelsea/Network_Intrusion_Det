import pandas as pd

# Load the ML-ready dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

print("=" * 50)
print("ML-READY DATASET CHECK")
print("=" * 50)

print("\n1. DATASET SHAPE")
print(df.shape)

print("\n2. COLUMN NAMES")
for column in df.columns:
    print(column)

print("\n3. DATA TYPES")
print(df.dtypes)

print("\n4. MISSING VALUES")
print(df.isnull().sum())

print("\n5. LABEL DISTRIBUTION")
print(df["label"].value_counts())

print("\n6. FIRST FIVE ROWS")
print(df.head())

print("\n" + "=" * 50)
print("CHECK COMPLETE")
print("=" * 50)