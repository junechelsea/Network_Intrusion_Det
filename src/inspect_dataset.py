import pandas as pd

# Load the final dataset
df = pd.read_csv("data/final_dataset.csv")

print("=" * 50)
print("DATASET INSPECTION")
print("=" * 50)

# Basic information
print("\n1. DATASET SHAPE")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# Column names
print("\n2. COLUMN NAMES")
print(df.columns.tolist())

# Data types
print("\n3. DATA TYPES")
print(df.dtypes)

# Missing values
print("\n4. MISSING VALUES")
print(df.isnull().sum())

# Duplicate rows
print("\n5. DUPLICATE ROWS")
print(f"Duplicates: {df.duplicated().sum()}")

# Class distribution
print("\n6. CLASS DISTRIBUTION")
print(df["label"].value_counts())
print("\nClass percentages:")
print((df["label"].value_counts(normalize=True) * 100).round(2))

# First five rows
print("\n7. FIRST FIVE ROWS")
print(df.head())

# Numerical summary
print("\n8. NUMERICAL FEATURE SUMMARY")
print(df.describe())

print("\n" + "=" * 50)
print("INSPECTION COMPLETE")
print("=" * 50)