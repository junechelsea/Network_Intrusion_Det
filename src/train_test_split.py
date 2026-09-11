import pandas as pd
from sklearn.model_selection import train_test_split

# Load the ML-ready dataset
df = pd.read_csv("data/ml_ready_dataset.csv")

# Separate features from the target
X = df.drop(columns=["label"])
y = df["label"]

# Split the dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("=" * 50)
print("TRAIN / TEST SPLIT")
print("=" * 50)

print("\nOriginal dataset:")
print(f"Features: {X.shape}")
print(f"Labels: {y.shape}")

print("\nTraining data:")
print(f"X_train: {X_train.shape}")
print(f"y_train: {y_train.shape}")

print("\nTesting data:")
print(f"X_test: {X_test.shape}")
print(f"y_test: {y_test.shape}")

print("\nTraining label distribution:")
print(y_train.value_counts())

print("\nTesting label distribution:")
print(y_test.value_counts())

print("\nTraining percentages:")
print((y_train.value_counts(normalize=True) * 100).round(2))

print("\nTesting percentages:")
print((y_test.value_counts(normalize=True) * 100).round(2))

print("\n" + "=" * 50)
print("SPLIT COMPLETE")
print("=" * 50)