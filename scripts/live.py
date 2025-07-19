import random
import time
import datetime
import os

# File to write live logs
log_file = '/home/rksha/Documents/Projects/log-anamoly-detector/data/live_test.log'

def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def random_port():
    return random.randint(1024, 65535)

def random_user():
    return random.choice(['root', 'ubuntu', 'admin', 'guest', 'test', 'backup'])

def random_pid():
    return random.randint(1000, 30000)

def random_hostname():
    return random.choice(['LabSZ', 'server', 'prod1', 'testvm'])

def random_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%b %d %H:%M:%S")  # e.g., Dec 10 07:08:28

def random_number():
    return random.randint(11, 99)

# Templates
normal_templates = [
    "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:auth): check pass; user unknown",
    "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:session): session closed for user {user}",
    "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:session): session opened for user {user} by (uid={try1})",
    "{timestamp} {host} sshd[{pid}]: Connection closed by {ip} [preauth]",
    "{timestamp} {host} sshd[{pid}]: Received disconnect from {ip}: {num}: Bye Bye [preauth]",
    "{timestamp} {host} sshd[{pid}]: Received disconnect from {ip}: {num}: Closed due to user request [preauth]",
    "{timestamp} {host} sshd[{pid}]: Received disconnect from {ip}: {num}: disconnected by user",
    "{timestamp} {host} sshd[{pid}]: Did not receive identification string from {ip}",
    "{timestamp} {host} sshd[{pid}]: PAM service(sshd) ignoring max retries; {try2} > {try1}",
    "{timestamp} {host} sshd[{pid}]: Accepted password for {user} from {ip} port {port} ssh{try0}"
]

anomaly_templates = [
    "{timestamp} {host} sshd[{pid}]: reverse mapping checking getaddrinfo for ns.randomdomain.com [{ip}] failed - POSSIBLE BREAK-IN ATTEMPT!",
    "{timestamp} {host} sshd[{pid}]: Invalid user {user} from {ip}",
    "{timestamp} {host} sshd[{pid}]: input_userauth_request: invalid user {user} [preauth]",
    "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost={ip}",
    "{timestamp} {host} sshd[{pid}]: pam_unix(sshd:auth): authentication failure; logname= uid={try2} euid={try1} tty=ssh ruser= rhost={ip}",
    "{timestamp} {host} sshd[{pid}]: Failed password for invalid user {user} from {ip} port {port} ssh{try0}",
    "{timestamp} {host} sshd[{pid}]: message repeated {count} times: [ Failed password for root from {ip} port {port} ssh{try0}]",
    "{timestamp} {host} sshd[{pid}]: Disconnecting: Too many authentication failures for {user} [preauth]",
    "{timestamp} {host} sshd[{pid}]: PAM {count} more authentication failures; logname= uid={try1} euid={try2} tty=ssh ruser= rhost={ip}  user={user}",
    "{timestamp} {host} sshd[{pid}]: fatal: Read from socket failed: Connection reset by peer",
    "{timestamp} {host} sshd[{pid}]: error: maximum authentication attempts exceeded for {user} from {ip} port {port}",
    "{timestamp} {host} sshd[{pid}]: error: Received disconnect from {ip}: {port}: com.jcraft.jsch.JSchException: Auth fail [preauth]",
    "{timestamp} {host} sshd[{pid}]: error: Received disconnect from {ip}: {port}: No more user authentication methods available. [preauth]",
    "{timestamp} {host} sshd[{pid}]: Failed none for invalid user {try1} from {ip} port {port} ssh{try0}",
    "{timestamp} {host} sshd[{pid}]: Failed password for user {user} from {ip} port {port} ssh{try2}",
    "{timestamp} {host} sshd[{pid}]: fatal: Write failed: Connection reset by peer [preauth]",
    "{timestamp} {host} sshd[{pid}]: sudo: user{try1}: command not allowed ; TTY=pts/1 ; PWD=/home/user{try0} ; USER=root ; COMMAND=/bin/cat /etc/shadow",
    "{timestamp} {host} sshd[{pid}]: sudo: pam_unix(sudo:auth): authentication failure; logname={user}{try1} uid={pid} euid={try0} tty=/dev/pts/2 ruser=user1 rhost=  user=root",
    "{timestamp} {host} sshd[{pid}]: sudo: {user} : 3 incorrect password attempts ; TTY=pts/2 ; PWD=/home/user2 ; USER=root ; COMMAND=/usr/bin/vim /etc/sudoers",
    "{timestamp} {host} sshd[{pid}]: myservice[{pid}]: segfault at 000000000000 ip 00007f0a4e4b623a sp 00007ffde1e08a50 error {try1} in libc-{try2}.{num}.so[{rand}]",
    "{timestamp} {host} sshd[{pid}]: kernel: myapp[{pid}]: segfault at 7f0a00000000 ip 00007f0a4e4c0000 sp 00007ffde1e07000 error {try0} in libpthread-{try1}.{num}.so[7f0a4e480000+19000]",
    "{timestamp} {host} sshd[{pid}]: systemd[1]: myapp.service: Main process exited, code=killed, status={num}/SEGV",
    "{timestamp} {host} sshd[{pid}]: kernel: [12345.{rand}] Kernel panic - not syncing: Fatal exception",
    "{timestamp} {host} sshd[{pid}]: kernel: [12346.{rand}] Kernel panic - attempted to kill init! exitcode=0x00000009",
    "{timestamp} {host} sshd[{pid}]: kernel: panic occurred, switching back to text console"
]

def generate_normal_log():
    tpl = random.choice(normal_templates)
    return tpl.format(
        timestamp=random_timestamp(),
        host=random_hostname(),
        pid=random_pid(),
        user=random_user(),
        ip=random_ip(),
        port=random_port(),
        num=random_number(),
        try0=random.randint(1, 9),
        try1=random.randint(1, 4),
        try2=random.randint(5, 9)
    )

def generate_anomaly_log():
    tpl = random.choice(anomaly_templates)
    return tpl.format(
        timestamp=random_timestamp(),
        host=random_hostname(),
        pid=random_pid(),
        user=random_user(),
        ip=random_ip(),
        port=random_port(),
        count=random.randint(1, 10),
        num=random_number(),
        try0=random.randint(1, 9),
        try1=random.randint(1, 4),
        try2=random.randint(5, 9),
        rand=random.randint(123450, 987650)
    )

def main():
    print(f"🚀 Live log generation started! Writing to: {log_file}")
    while True:
        # Randomly choose normal or anomaly
        if random.random() < 0.1:  # 10% chance anomaly
            content = generate_anomaly_log()
            log_line = f"anomaly log generated: {content}"
        else:
            content = generate_normal_log()
            log_line = f"normal log generated: {content}"
        
        # Append to log file
        with open(log_file, 'a') as f:
            f.write(log_line + '\n')

        print(f"📝 {log_line}")
        time.sleep(random.uniform(0.5, 2))  # wait a bit before next log

if __name__ == "__main__":
    main()
