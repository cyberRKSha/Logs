# import time
# import random

# # Path to the live log file
# log_file = '/home/rksha/Documents/Projects/log-anamoly-detector/data/live_test.log'

# # Some synthetic normal logs
# normal_logs = [
#     "081109 203524 147 INFO dfs.DataNode$PacketResponder: Received block blk_-9073992586687739851 of size 11977 from /10.250.7.244",
#     "081109 203529 154 INFO dfs.FSNamesystem: BLOCK* NameSystem.allocateBlock: block allocated successfully blk_-1608999687919862906",
#     "081109 203527 152 INFO dfs.DataNode$PacketResponder: Received block blk_-9073992586687739851 of size 11977 from /10.250.7.244",
#     "081109 203531 156 INFO dfs.DataNode$PacketResponder: Received block blk_-9073992586687739851 of size 11977 from /10.250.7.244"
# ]

# # Some synthetic anomaly logs
# anomaly_logs = [
#     "081109 203525 150 ERROR dfs.FSNamesystem: BLOCK* NameSystem.addStoredBlock: checksum mismatch detected on blk_-1608999687919862906",
#     "081109 203526 151 CRITICAL dfs.Audit: Multiple failed login attempts detected for user root",
#     "081109 203528 153 WARNING dfs.DataNode$DataXceiver: Receiving block blk_-1608999687919862906 from blacklisted node /10.250.66.66:50010",
#     "081109 203530 155 CRITICAL dfs.FSNamesystem: unexpected block allocation failure blk_-1608999687919862906",
#     "081109 203532 157 WARNING dfs.SecurityAlert: Suspicious repeated block transfer from unknown IP /10.99.99.99:50010",
#     "081109 203534 159 ERROR dfs.SecurityAlert: Unauthorized block deletion attempt detected on blk_-1608999687919862906"
# ]

# all_logs = normal_logs + anomaly_logs

# print("🟢 Starting synthetic log generator...")

# try:
#     while True:
#         # Randomly pick normal or anomaly
#         log_line = random.choice(all_logs)
#         # Append to live log file
#         with open(log_file, 'a', encoding='utf-8') as f:
#             f.write(log_line + '\n')
#         print(f"📝 Added log: {log_line}")

#         # Wait 2–5 seconds before next log
#         time.sleep(random.uniform(2, 5))
# except KeyboardInterrupt:
#     print("\n⏹️ Stopped synthetic log generator.")



import time
import random

# Path to the live log file (change if your path is different)
log_file = '/home/rksha/Documents/Projects/log-anamoly-detector/data/live_test.log'

# Templates for normal logs
normal_templates = [
    "{sec2} {sec1} {id} INFO dfs.DataNode$PacketResponder: Received block blk_{block_id} of size {size} from /{ip1}.{ip2}.{ip1}.{ip2}",
    "{sec1} {sec2} {id} INFO dfs.FSNamesystem: BLOCK* NameSystem.allocateBlock: block allocated successfully blk_{block_id}",
    "{sec1} {sec2} {id} INFO dfs.DataNode$PacketResponder: Received block {block_id} of size {size} from /{ip2}.{ip1}.{ip2}.{ip1}",
    "{sec2} {sec1} {id} INFO dfs.FSNamesystem: BLOCK* NameSystem.addStoredBlock: blockMap updated for {block_id}",
    "{sec1} {sec2} {id} INFO org.apache.hadoop.hdfs.server.datanode.DataNode: PacketResponder for {block_id} terminating",
    "{sec2} {sec1} {id} INFO org.apache.hadoop.hdfs.StateChange: BLOCK* NameSystem.allocateBlock: /user/hadoop/file{num}",
    "{sec2} {sec1} {id} INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Scheduling block report for {block_id}"

]

# Templates for anomaly logs
anomaly_templates = [
    "{sec1} {sec2} {id} ERROR dfs.FSNamesystem: BLOCK* NameSystem.addStoredBlock: checksum mismatch detected on blk_{block_id}",
    "{sec2} {sec1} {id} CRITICAL dfs.Audit: Multiple failed login attempts detected for user root{num}",
    "{sec2} {sec1} {id} ERROR dfs.DataNode$DataXceiver: Receiving block blk_{block_id} from blacklisted node /{ip1}.{ip2}.{ip1}.{ip2}:{port_no}",
    "{sec1} {sec2} {id} CRITICAL dfs.FSNamesystem: unexpected block allocation failure blk_{block_id}",
    "{sec1} {sec2} {id} WARNING dfs.SecurityAlert: Suspicious repeated block transfer from unknown IP /{ip2}.{ip1}.{ip2}.{ip1}:{port_no}",
    "{sec1} {sec2} {id} ERROR dfs.SecurityAlert: Unauthorized block deletion attempt detected on blk_{block_id}"
]

def generate_random_log():
    """Randomly create a normal or anomaly log line with random data"""
    is_anomaly = random.choice([False, True, False, True])  # More normal logs
    template = random.choice(anomaly_templates if is_anomaly else normal_templates)
    log_line = template.format(
        sec1=random.randint(100001, 498756),
        sec2=random.randint(500002, 987654),
        id=random.randint(1, 999),
        block_id=random.randint(-999999999999999999, -100000000000000000),
        size=random.randint(10000, 20000),
        ip1=random.randint(1, 254),
        ip2=random.randint(1, 254),
        port_no=random.randint(1, 65536),
        num=random.randint(1,100)
    )
    return log_line, 'anomaly' if is_anomaly else 'normal'

print("🟢 Starting live synthetic log generator... (Press Ctrl+C to stop)")

try:
    while True:
        log_line, label = generate_random_log()
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_line + '\n')
        print(f"📝 Added [{label}] log: {log_line}")

        # Wait 2–5 seconds before next log
        time.sleep(random.uniform(2, 5))

except KeyboardInterrupt:
    print("\n⏹️ Stopped synthetic log generator.")
