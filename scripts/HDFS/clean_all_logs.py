import pandas as pd

df = pd.read_csv('/home/rksha/Documents/Projects/log-anamoly-detector/data/all_logs.csv')
print(df.head(10))   # See the first few rows

# Remove rows where 'label' column is not numeric
df = df[pd.to_numeric(df['label'], errors='coerce').notnull()]

# Convert label to int now that bad rows are removed
df['label'] = df['label'].astype(int)

# Save cleaned CSV
df.to_csv('/home/rksha/Documents/Projects/log-anamoly-detector/data/all_logs.csv', index=False)
print("✅ Cleaned all_logs.csv and fixed labels.")
