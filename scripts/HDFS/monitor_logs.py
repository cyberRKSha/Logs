import time
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import requests

# Path to your live log file (update path if needed)
log_file = '/home/rksha/Documents/Projects/log-anamoly-detector/data/live_test.log'   # relative to monitor/
prediction_log = '/home/rksha/Documents/Projects/log-anamoly-detector/data/prediction.log'

# Load trained model & vectorizer
print("📦 Loading model & vectorizer...")
with open('/home/rksha/Documents/Projects/log-anamoly-detector/models/model.pkl', 'rb') as f:
    data = pickle.load(f)
model = data['model']
vectorizer = data['vectorizer']

print("👀 Watching file:", log_file)

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
                    if line.strip():
                        X_new = vectorizer.transform([line.strip()])
                        pred = model.predict(X_new)[0]
                        label = 'anamoly' if pred == -1 else 'normal'
                        if pred == -1:
                            print(f"\033[91m⚠️ Anomaly detected: {line}\033[0m")
                        else:
                            print(f"\033[92m✅ Normal log: {line}\033[0m")
                        
                        # ⭐ Send to dashboard
                        try:
                            requests.post(
                                "http://127.0.0.1:8000/api/new_log",
                                json={"log": line.strip(), "label": label},
                                timeout=1
                            )
                        except Exception as e:
                            print(f"⚠️ Failed to send to dashboard: {e}")

                        with open(prediction_log, 'a') as pf:
                            pf.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{label},{line}\n")
            except Exception as e:
                print(f"❌Error while processing log: {e}")

if __name__ == "__main__":
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/home/rksha/Documents/Projects/log-anamoly-detector/data', recursive=False)
    observer.start()
    print("🔵 Live monitoring started! Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
