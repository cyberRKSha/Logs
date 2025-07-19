import random
import datetime

def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def random_block():
    return f"blk_{random.randint(-9999999999999999999, 9999999999999999999)}"

def random_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%y%m%d %H%M%S") + f" {random.randint(100, 999)}"

def generate_normal_log():
    templates = [
        "INFO dfs.DataNode$PacketResponder: Received block {block} of size {size} from /{ip}",
        "INFO dfs.FSNamesystem: BLOCK* NameSystem.addStoredBlock: blockMap updated for {block}",
        "INFO org.apache.hadoop.hdfs.server.datanode.DataNode: PacketResponder for {block} terminating",
        "INFO org.apache.hadoop.hdfs.StateChange: BLOCK* NameSystem.allocateBlock: /user/hadoop/file{num}",
        "INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Scheduling block report for {block}"
    ]
    tpl = random.choice(templates)
    return f"{random_timestamp()} {tpl.format(block=random_block(), size=random.randint(1000,100000), ip=random_ip(), num=random.randint(1,100))}"

def generate_anomaly_log():
    templates = [
        "ERROR dfs.FSNamesystem: BLOCK* NameSystem.addStoredBlock: checksum mismatch detected on {block}",
        "CRITICAL dfs.Audit: Multiple failed login attempts detected for user root",
        "WARNING dfs.Security: Root password changed outside maintenance window",
        "ERROR dfs.SecurityAlert: Unauthorized block deletion attempt detected on {block}",
        "ERROR dfs.DataNode$DataXceiver: Receiving block {block} from blacklisted node /{ip}:50010",
        "ERROR dfs.Security: Unauthorized user hacker attempted to access secure block {block}",
        "CRITICAL dfs.FSNamesystem: BLOCK* NameSystem.allocateBlock: unexpected block allocation failure {block}",
        "WARNING dfs.SecurityAlert: Suspicious repeated block transfer from unknown IP /{ip}:50010"
    ]
    tpl = random.choice(templates)
    return f"{random_timestamp()} {tpl.format(block=random_block(), ip=random_ip())}"

def generate_logs(n_normal=35, n_anomaly=15):
    logs = []
    for _ in range(n_normal):
        logs.append( (generate_normal_log(), 1) )
    for _ in range(n_anomaly):
        logs.append( (generate_anomaly_log(), -1) )
    random.shuffle(logs)
    return logs
