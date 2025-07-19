# import random
# import datetime

# def random_ip():
#     return ".".join(str(random.randint(1, 255)) for _ in range(4))

# def random_port():
#     return random.randint(1024, 65535)

# def random_user():
#     return random.choice(['fztu', 'root', 'ubuntu', 'admin', 'test', 'guest', 'oracle', 'backup', 'webmaster', 'chen', 'pgadmin', 'matlab', '123'])

# def random_pid():
#     return random.randint(1000, 30000)

# def random_timestamp():
#     now = datetime.datetime.now()
#     return now.strftime("%b %d %H:%M:%S")  # e.g., Dec 10 07:08:28

# def random_hostname():
#     return random.choice(['LabSZ', 'server', 'prod1', 'testvm'])

# def random_number():
#     return random.randint(11, 99)

# def generate_normal_log():
#     templates = [
#         "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:auth): check pass; user unknown",
#         "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:session): session closed for user {user}",
#         "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:session): session opened for user {user} by (uid={try1})",
#         "{timestamp} {host} sshd[{pid}]: Connection closed by {ip} [preauth]",
#         "{timestamp} {host} sshd[{pid}]: Received disconnect from {ip}: {num}: Bye Bye [preauth]",
#         "{timestamp} {host} sshd[{pid}]: Received disconnect from {ip}: {num}: Closed due to user request [preauth]",
#         "{timestamp} {host} sshd[{pid}]: Received disconnect from {ip}: {num}: disconnected by user",
#         "{timestamp} {host} sshd[{pid}]: Did not receive identification string from {ip}",
#         "{timestamp} {host} sshd[{pid}]: PAM service(sshd) ignoring max retries; {try2} > {try1}",
#         "{timestamp} {host} sshd[{pid}]: Accepted password for {user} from {ip} port {port} ssh{try0}"
#     ]
#     tpl = random.choice(templates)
#     return tpl.format(
#         timestamp=random_timestamp(),
#         host=random_hostname(),
#         pid=random_pid(),
#         user=random_user(),
#         ip=random_ip(),
#         port=random_port(),
#         num=random_number(),
#         try0=random.randint(1,9),
#         try1=random.randint(1, 4),
#         try2=random.randint(5, 9)
#     )

# def generate_anomaly_log():
#     templates = [
#         "{timestamp} {host} sshd[{pid}]: reverse mapping checking getaddrinfo for ns.randomdomain.com [{ip}] failed - POSSIBLE BREAK-IN ATTEMPT!",
#         "{timestamp} {host} sshd[{pid}]: Invalid user {user} from {ip}",
#         "{timestamp} {host} sshd[{pid}]: input_userauth_request: invalid user {user} [preauth]",
#         "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost={ip}",
#         "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:auth): authentication failure; logname= uid={try2} euid={try1} tty=ssh ruser= rhost={ip}"
#         "{timestamp} {host} sshd[{pid}]: Failed password for invalid user {user} from {ip} port {port} ssh{try0}",
#         "{timestamp} {host} sshd[{pid}]: message repeated {count} times: [ Failed password for root from {ip} port {port} ssh{try0}]",
#         "{timestamp} {host} sshd[{pid}]: Disconnecting: Too many authentication failures for {user} [preauth]",
#         "{timestamp} {host} sshd[{pid}]: PAM {count} more authentication failures; logname= uid={try1} euid={try2} tty=ssh ruser= rhost={ip}  user={user}",
#         "{timestamp} {host} sshd[{pid}]: fatal: Read from socket failed: Connection reset by peer",
#         "{timestamp} {host} sshd[{pid}]: error: maximum authentication attempts exceeded for {user} from {ip} port {port}",
#         "{timestamp} {host} sshd[{pid}]: error: Received disconnect from {ip}: {port}: com.jcraft.jsch.JSchException: Auth fail [preauth]",
#         "{timestamp} {host} sshd[{pid}]: error: Received disconnect from {ip}: {port}: No more user authentication methods available. [preauth]",
#         "{timestamp} {host} sshd[{pid}]: Failed none for invalid user {try1} from {ip} port {port} ssh{try0}",
#         "{timestamp} {host} sshd[{pid}]: Failed password for user {user} from {ip} port {port} ssh{try2}",
#         "{timestamp} {host} sshd[{pid}]: fatal: Write failed: Connection reset by peer [preauth]"
#     ]
#     tpl = random.choice(templates)
#     return tpl.format(
#         timestamp=random_timestamp(),
#         host=random_hostname(),
#         pid=random_pid(),
#         user=random_user(),
#         ip=random_ip(),
#         port=random_port(),
#         count=random.randint(1, 10),
#         num=random_number(),
#         try0=random.randint(1,9),
#         try1=random.randint(1, 4),
#         try2=random.randint(5, 9)
#     )

# def generate_logs(n_normal=35, n_anomaly=15):
#     logs = []
#     for _ in range(n_normal):
#         logs.append( (generate_normal_log(), 1) )
#     for _ in range(n_anomaly):
#         logs.append( (generate_anomaly_log(), -1) )
#     random.shuffle(logs)
#     return logs






import random
import datetime
import pandas as pd
import os

def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def random_port():
    return random.randint(1024, 65535)

def random_user():
    return random.choice(['fztu', 'root', 'ubuntu', 'admin', 'test', 'guest', 'oracle', 'backup', 'webmaster', 'chen', 'pgadmin', 'matlab', '123'])

def random_pid():
    return random.randint(1000, 30000)

def random_timestamp():
    now = datetime.datetime.now()
    # e.g., Dec 10 07:08:28 → 'Dec', '10', '07:08:28'
    month_str = now.strftime("%b")
    day_str = now.strftime("%d")
    time_str = now.strftime("%H:%M:%S")
    return month_str, day_str, time_str

def random_hostname():
    return random.choice(['LabSZ', 'server', 'prod1', 'testvm'])

def random_number():
    return random.randint(11, 99)

def generate_normal_log_row():
    templates = [
        "pam_unix(sshd:auth): check pass; user unknown",
        "pam_unix(sshd:session): session closed for user {user}",
        "pam_unix(sshd:session): session opened for user {user} by (uid={try1})",
        "Connection closed by {ip} [preauth]",
        "Received disconnect from {ip}: {num}: Bye Bye [preauth]",
        "Received disconnect from {ip}: {num}: Closed due to user request [preauth]",
        "Received disconnect from {ip}: {num}: disconnected by user",
        "Did not receive identification string from {ip}",
        "PAM service(sshd) ignoring max retries; {try2} > {try1}",
        "Accepted password for {user} from {ip} port {port} ssh{try0}"
    ]
    tpl = random.choice(templates)
    month, day, time = random_timestamp()
    return [
        month,
        day,
        time,
        random_hostname(),
        random_pid(),
        tpl.format(
            user=random_user(),
            ip=random_ip(),
            port=random_port(),
            num=random_number(),
            try0=random.randint(1, 9),
            try1=random.randint(1, 4),
            try2=random.randint(5, 9)
        ),
        1  # label for normal log
    ]

def generate_anomaly_log_row():
    templates = [
        "reverse mapping checking getaddrinfo for ns.randomdomain.com [{ip}] failed - POSSIBLE BREAK-IN ATTEMPT!",
        "Invalid user {user} from {ip}",
        "input_userauth_request: invalid user {user} [preauth]",
        "pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost={ip}",
        "pam_unix(sshd:auth): authentication failure; logname= uid={try2} euid={try1} tty=ssh ruser= rhost={ip}",
        "Failed password for invalid user {user} from {ip} port {port} ssh{try0}",
        "message repeated {count} times: [ Failed password for root from {ip} port {port} ssh{try0}]",
        "Disconnecting: Too many authentication failures for {user} [preauth]",
        "PAM {count} more authentication failures; logname= uid={try1} euid={try2} tty=ssh ruser= rhost={ip}  user={user}",
        "fatal: Read from socket failed: Connection reset by peer",
        "error: maximum authentication attempts exceeded for {user} from {ip} port {port}",
        "error: Received disconnect from {ip}: {port}: com.jcraft.jsch.JSchException: Auth fail [preauth]",
        "error: Received disconnect from {ip}: {port}: No more user authentication methods available. [preauth]",
        "Failed none for invalid user {try1} from {ip} port {port} ssh{try0}",
        "Failed password for user {user} from {ip} port {port} ssh{try2}",
        "fatal: Write failed: Connection reset by peer [preauth]",
        "sudo: user{try1}: command not allowed ; TTY=pts/1 ; PWD=/home/user{try0} ; USER=root ; COMMAND=/bin/cat /etc/shadow",
        "sudo: pam_unix(sudo:auth): authentication failure; logname={user}{try1} uid={rand} euid={try0} tty=/dev/pts/2 ruser=user1 rhost=  user=root",
        "sudo: {user} : 3 incorrect password attempts ; TTY=pts/2 ; PWD=/home/user2 ; USER=root ; COMMAND=/usr/bin/vim /etc/sudoers",
        "myservice[{rand}]: segfault at 000000000000 ip 00007f0a4e4b623a sp 00007ffde1e08a50 error {try1} in libc-{try2}.{num}.so[{rand}]",
        "kernel: myapp[{rand}]: segfault at 7f0a00000000 ip 00007f0a4e4c0000 sp 00007ffde1e07000 error {try0} in libpthread-{try1}.{num}.so[7f0a4e480000+19000]",
        "systemd[1]: myapp.service: Main process exited, code=killed, status={num}/SEGV",
        "kernel: [12345.{rand}] Kernel panic - not syncing: Fatal exception",
        "kernel: [12346.{rand}] Kernel panic - attempted to kill init! exitcode=0x00000009",
        "kernel: panic occurred, switching back to text console"
    ]
    tpl = random.choice(templates)
    month, day, time = random_timestamp()
    return [
        month,
        day,
        time,
        random_hostname(),
        random_pid(),
        tpl.format(
            user=random_user(),
            ip=random_ip(),
            port=random_port(),
            count=random.randint(1, 10),
            num=random_number(),
            try0=random.randint(1, 9),
            try1=random.randint(1, 4),
            try2=random.randint(5, 9),
            rand=random.randint(123450, 987650)
        ),
        -1  # label for anomaly
    ]

def generate_logs(n_normal=70, n_anomaly=30):
    rows = []
    for _ in range(n_normal):
        rows.append(generate_normal_log_row())
    for _ in range(n_anomaly):
        rows.append(generate_anomaly_log_row())
    random.shuffle(rows)
    return rows

if __name__ == "__main__":
    log_csv_path = '/home/rksha/Documents/Projects/log-anamoly-detector/data/logs.csv'

    # Generate new logs
    new_logs = generate_logs(n_normal=70, n_anomaly=30)
    new_df = pd.DataFrame(new_logs, columns=['Date', 'Day', 'Time', 'Component', 'PID', 'Content', 'Label'])

    if os.path.exists(log_csv_path):
        # Load existing logs
        old_df = pd.read_csv(log_csv_path)
        # Append new logs
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
        # Save back
        combined_df.to_csv(log_csv_path, index=False)
        print(f"✅ Appended {len(new_df)} new logs to existing log file at /data folder.")
    else:
        # File doesn't exist → create new one
        new_df.to_csv(log_csv_path, index=False)
        print(f"✅ Created new log file with {len(new_df)} logs at /data folder.")