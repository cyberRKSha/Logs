# import pandas as pd
# import random

# normal_logs = [
#     "081109 203524 147 INFO dfs.DataNode$PacketResponder: Received block blk_-9073992586687739851 of size 11977 from /10.250.7.244",
#     "081109 203530 155 INFO dfs.FSNamesystem: BLOCK* NameSystem.getAdditionalBlock: allocated new block blk_-2342342342342342342",
#     "081109 203531 156 INFO dfs.ClientProtocol: Successfully replicated block blk_-2342342342342342342 to 3 datanodes",
#     "081109 203532 157 INFO dfs.DataNode: Block blk_-2342342342342342342 replication completed",
#     "081109 203533 158 INFO dfs.FSNamesystem: BLOCK* NameSystem.completeFile: file /user/hadoop/file1 closed successfully"
# ]

# anomaly_logs = [
#     "081109 203524 149 ERROR dfs.SecurityAlert: Unauthorized block deletion attempt detected on blk_-1608999687919862906",
#     "081109 203525 150 ERROR dfs.FSNamesystem: BLOCK* NameSystem.addStoredBlock: checksum mismatch detected on blk_-1608999687919862906",
#     "081109 203526 151 CRITICAL dfs.Audit: Multiple failed login attempts detected for user root",
#     "081109 203527 152 WARNING dfs.Security: Root password changed outside maintenance window",
#     "081109 203528 153 ERROR dfs.DataNode$DataXceiver: Receiving block blk_-1608999687919862906 from blacklisted node /10.250.66.66:50010",
#     "081109 203529 154 ERROR dfs.Security: Unauthorized user hacker attempted to access secure block blk_-1608999687919862906",
#     "081109 203530 155 CRITICAL dfs.FSNamesystem: BLOCK* NameSystem.allocateBlock: unexpected block allocation failure blk_-1608999687919862906",
#     "081109 203531 156 WARNING dfs.SecurityAlert: Suspicious repeated block transfer from unknown IP /10.99.99.99:50010"
# ]

# def generate_logs(n=50):
#     logs = []
#     for _ in range(n):
#         if random.random() < 0.7:
#             text = random.choice(normal_logs)
#             label = 1
#         else:
#             text = random.choice(anomaly_logs)
#             label = -1
#         logs.append({'text': text, 'label': label})
#     return logs

# if __name__ == "__main__":
#     logs = generate_logs()
#     df = pd.DataFrame(logs)
#     df.to_csv('/home/rksha/Documents/Projects/log-anamoly-detector/data/new_logs.csv', index=False, encoding='utf-8')
#     print("✅ Generated data/new_logs.csv with", len(df), "new logs.")

import pandas as pd
from log_generator import generate_logs

# Generate 50 new logs (40 normal, 10 anomaly)
logs = generate_logs(n_normal=35, n_anomaly=15)

df = pd.DataFrame(logs, columns=['text', 'label'])
df.to_csv('/home/rksha/Documents/Projects/log-anamoly-detector/data/new_logs.csv', index=False)
print("✅ Generated new logs: data/new_logs.csv")
