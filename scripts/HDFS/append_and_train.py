# append_and_train.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import json
import pickle
import os

# Load main dataset
df = pd.read_csv('/home/rksha/Documents/Projects/log-anamoly-detector/data/all_logs.csv')
df['label'] = df['label'].astype(int)

# If new logs exist, append them
new_logs_path = '/home/rksha/Documents/Projects/log-anamoly-detector/data/new_logs.csv'

if os.path.exists(new_logs_path):
    new_df = pd.read_csv(new_logs_path)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv('/home/rksha/Documents/Projects/log-anamoly-detector/data/all_logs.csv', index=False)
    os.remove(new_logs_path)
    print("✅ New logs added to dataset.")

# Vectorize
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df['text'])
y = df['label']

# Train
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Save model & vectorizer together
with open('/home/rksha/Documents/Projects/log-anamoly-detector/models/models.pkl', 'wb') as f:
    pickle.dump({'model': model, 'vectorizer': vectorizer}, f)

print("✅ Model trained & saved as models.pkl")

# Predict on whole data to get metrics
y_pred = model.predict(X)
report = classification_report(y, y_pred, output_dict=True)

# Save report
with open('/home/rksha/Documents/Projects/log-anamoly-detector/models/classification_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print("📊 Classification report saved.")