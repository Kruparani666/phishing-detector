import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load dataset
data = pd.read_csv("phishing_email.csv")

X = data["text"]
y = data["label"]

# Better vectorizer
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2),   # use bigrams
    max_features=5000
)

X = vectorizer.fit_transform(X)

# Stratified split (important!)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Better model with balancing
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
os.makedirs("model", exist_ok=True)
pickle.dump(model, open("model/phishing_model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

print("Improved model trained and saved successfully!")
