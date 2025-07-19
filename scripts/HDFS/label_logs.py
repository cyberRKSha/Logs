# import pandas as pd

# # Load CSV
# df = pd.read_csv('/home/rksha/Documents/Projects/log-anamoly-detector/data/logs.csv')  # <-- update path if needed

# # Preview to see column names
# print("Columns found:", df.columns)

# # Replace 'message' below with actual column name containing the log text
# log_column = 'Content'  # Example: change if actual column is different

# # Define keywords that likely indicate anomaly
# anomaly_keywords = [
#     'reverse mapping checking getaddrinfo', 'POSSIBLE BREAK-IN ATTEMPT',
#     'Invalid user', 'authentication failure', 'Failed password',
#     'Too many authentication failures', 'PAM', 'disconnect',
#     'Did not receive identification string', 'input_userauth_request',
#     'pam_unix(sshd:auth): authentication failure', 'message repeated', 'Disconnecting: Too many authentication failures',
#     'fatal', 'error', 'Failed'
# ]

# # Function to detect anomalies
# def label_log(text):
#     text_lower = str(text).lower()
#     if any(keyword.lower() in text_lower for keyword in anomaly_keywords):
#         return -1
#     else:
#         return 1

# # Apply labeling
# df['label'] = df[log_column].apply(label_log)

# # Save labeled CSV
# df.to_csv('logs_labeled.csv', index=False)
# print("✅ Labeled logs saved to logs_labeled.csv")





import pandas as pd

df = pd.read_csv('/home/rksha/Documents/Projects/log-anamoly-detector/data/logs.csv')

print("Columns found:", df.columns)

# Use actual column name:
log_column = 'Date:Day:Time:Component:Pid:Content'

# Define keywords
anomaly_keywords = [
    'reverse mapping checking getaddrinfo',
    'Invalid user', 'authentication failure', 'Failed password',
    'Too many authentication failures', 'input_userauth_request', 'message repeated', 
    'Disconnecting: Too many authentication failures', 'fatal', 'error', 'Failed'
]

def label_log(text):
    text_lower = str(text).lower()
    if any(keyword.lower() in text_lower for keyword in anomaly_keywords):
        return -1
    else:
        return 1

df['label'] = df[log_column].apply(label_log)

df.to_csv('logs_labeled.csv', index=False)
print("✅ Labeled logs saved to logs_labeled.csv")
