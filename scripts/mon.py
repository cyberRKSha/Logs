import time
import joblib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import requests
# import simpleaudio as sa
import subprocess

def alert(file_path):
    # try:
    #     wave_obj = sa.WaveObject.from_wave_file(file_path)
    #     wave_obj.play()  # async play; doesn’t block
    #     # time.sleep(5)
    #     # play_obj.stop()
    # except Exception as e:
    #     print(f"⚠️ Failed to play alert sound: {e}")
    try:
        subprocess.Popen(['paplay', file_path])
    except Exception as e:
        print(f"⚠️ Sound playback failed: {e}")


# Paths (update if needed)
log_file = '/home/rksha/Documents/Projects/log-anamoly-detector/data/live_test.log'
prediction_log = '/home/rksha/Documents/Projects/log-anamoly-detector/data/prediction.log'

# Load model and vectorizer
print("📦 Loading model & vectorizer...")
model = joblib.load('/home/rksha/Documents/Projects/log-anamoly-detector/models/rf_model.pkl')
vectorizer = joblib.load('/home/rksha/Documents/Projects/log-anamoly-detector/models/tfidf_vectorizer.pkl')

print(f"👀 Watching file: {log_file}")

# Define critical keywords and suggested advice
critical_alerts = {
    "Failed password": "Possible brute-force attack detected. Consider blocking offending IP.",
    "Invalid user": "Possible scanning detected. Review firewall rules.",
    "Kernel panic": "❗ CRITICAL: Kernel panic detected! Immediate attention required.",
    "segfault": "⚠️ Warning: Application crashed with segmentation fault.",
    "command not allowed": "🚨 Possible sudo misuse attempt detected.",
    "sudo" "su": "Review sudoers config."
}

class LogHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_size = os.path.getsize(log_file) if os.path.exists(log_file) else 0

    def on_modified(self, event):
        if event.src_path.endswith('live_test.log'):
            try:
                current_size = os.path.getsize(log_file)
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    f.seek(self._last_size)
                    new_lines = f.read().splitlines()
                self._last_size = current_size

                for line in new_lines:
                    if not line.strip():
                        continue

                    if ':' in line:
                        _, actual_log = line.split(':', 1)
                        actual_log = actual_log.strip()
                    else:    
                        print(f"⚠️ Skipping malformed line: {line}")
                        continue

                    # Predict anomaly
                    X_new = vectorizer.transform([actual_log])
                    pred = model.predict(X_new)[0]
                    label_str = 'anomaly' if pred == -1 else 'normal'

                    if pred == -1:
                        print(f"\033[91m⚠️ Anomaly detected: {actual_log}\033[0m")
                    else:
                        print(f"\033[92m✅ Normal log: {actual_log}\033[0m")

                    # Send log to dashboard
                    try:
                        requests.post(
                            "http://127.0.0.1:8000/api/new_log",
                            json={"log": actual_log, "label": label_str},
                            timeout=1
                        )
                    except Exception as e:
                        print(f"⚠️ Failed to send to dashboard: {e}")

                    # If it's an anomaly, check if it's critical and send alert
                    if label_str == 'anomaly':
                        for keyword, advice in critical_alerts.items():
                            if keyword.lower() in actual_log.lower():
                                try:
                                    requests.post(
                                        "http://127.0.0.1:8000/api/new_alert",
                                        json={"log": actual_log, "advice": advice},
                                        timeout=1
                                    )
                                    print(f"\033[93m🚨 Alert sent: {advice}\033[0m")
                                    alert("/home/rksha/Documents/Projects/log-anamoly-detector/data/alert.wav")
                                except Exception as e:
                                    print(f"⚠️ Failed to send alert: {e}")

                    # Append to prediction log
                    with open(prediction_log, 'a') as pf:
                        pf.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{label_str},{actual_log}\n")

            except Exception as e:
                print(f"❌ Error while processing log: {e}")

if __name__ == "__main__":
    observer = Observer()
    event_handler = LogHandler()
    observer.schedule(event_handler, path='data', recursive=False)

    observer.start()
    print("🔵 Live monitoring started! Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
