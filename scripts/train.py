import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Step 1: Load data
df = pd.read_csv('/home/rksha/Documents/Projects/log-anamoly-detector/data/logs.csv') 
print(f"✅ Loaded {len(df)} log entries")

# Step 2: Extract features & labels
texts = df['Content'].astype(str)  # log message text
labels = df['Label']               # 1 = normal, -1 = anomaly

# Step 3: Convert text to TF-IDF features
vectorizer = TfidfVectorizer(max_features=1000)  # you can tune max_features
X = vectorizer.fit_transform(texts)

# Step 4: Split into train/test to check model quality
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42, stratify=labels
)

# Step 5: Train RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 6: Evaluate
y_pred = model.predict(X_test)
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))
print("📌 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Step 7: Save the model & vectorizer for later use
joblib.dump(model, '/home/rksha/Documents/Projects/log-anamoly-detector/models/rf_model.pkl')
joblib.dump(vectorizer, '/home/rksha/Documents/Projects/log-anamoly-detector/models/tfidf_vectorizer.pkl')
print("✅ Model & vectorizer saved to 'models/' folder")
