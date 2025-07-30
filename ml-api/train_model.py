import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle

# Load dataset
df = pd.read_csv("phishing_dataset.csv")

print("Columns in dataset:", list(df.columns))

# Drop all string/non-numeric columns that can't be used in training
df = df.drop(["FILENAME", "URL", "Domain", "TLD", "Title", "Robots"], axis=1)

# Ensure no missing values (optional safety step)
df = df.dropna()

# Separate features and target
X = df.drop("label", axis=1)
y = df["label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model using pickle
with open("phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved as phishing_model.pkl")
