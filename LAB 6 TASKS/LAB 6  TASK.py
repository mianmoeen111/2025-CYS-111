from pathlib import Path
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix

# Find emails.csv in the same folder as TaskA.py
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "emails.csv"

if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"emails.csv not found at: {CSV_PATH}\n"
        "Place emails.csv in the same folder as TaskA.py."
    )

# Load and clean the dataset
df = pd.read_csv(CSV_PATH, on_bad_lines="skip")
df = df.dropna()

print("Dataset shape:", df.shape)
print("\nFirst five rows:")
print(df.head())

# Separate features and target
X = df.drop(columns=["Email No.", "Prediction"])
y = df["Prediction"].astype(int)

# Split into 80% training and 20% testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Train the Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

print("\n--- Task A Results ---")
print(f"Training rows: {len(X_train)}")
print(f"Testing rows: {len(X_test)}")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nConfusion Matrix (rows=actual, columns=predicted)")
print("Labels: 0 = Not Spam, 1 = Spam")
print(cm)

tn, fp, fn, tp = cm.ravel()
print("\nTrue Negatives:", tn)
print("False Positives:", fp)
print("False Negatives:", fn)
print("True Positives:", tp)

print("\nFirst five actual and predicted labels:")
print(pd.DataFrame({
    "Actual": y_test.iloc[:5].values,
    "Predicted": y_pred[:5]
}))

print("\nClass Priors:")
for label, probability in zip(model.classes_, model.class_log_prior_):
    print(f"Class {label}: {probability:.4f}")

# Compare different test-data sizes
print("\n--- Test Size Comparison ---")
for test_size in [0.10, 0.20, 0.30, 0.40]:
    Xtr, Xte, ytr, yte = train_test_split(
        X, y,
        test_size=test_size,
        random_state=42
    )

    temp_model = MultinomialNB()
    temp_model.fit(Xtr, ytr)
    predictions = temp_model.predict(Xte)

    print(
        f"Test size: {test_size:.0%} | "
        f"Accuracy: {accuracy_score(yte, predictions) * 100:.2f}%"
    )

# Show words most associated with each class
print("\n--- Top 10 Words for Each Class ---")
for class_index, class_label in enumerate(model.classes_):
    top_indices = model.feature_log_prob_[class_index].argsort()[-10:][::-1]
    top_words = X.columns[top_indices]

    class_name = "Spam" if class_label == 1 else "Not Spam"
    print(f"\n{class_name}:")
    print(", ".join(top_words))

# Save the trained model and its feature order for Task B
with open(BASE_DIR / "spam_model.pkl", "wb") as file:
    pickle.dump(model, file)

with open(BASE_DIR / "spam_features.pkl", "wb") as file:
    pickle.dump(list(X.columns), file)

print("\nModel saved successfully for Task B.")