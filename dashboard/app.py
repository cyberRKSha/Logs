from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

PREDICTION_LOG = '/home/rksha/Documents/Projects/log-anamoly-detector/data/prediction.log'

templates = Jinja2Templates(directory="templates")
clients = set()

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        pass
    finally:
        clients.remove(websocket)

@app.post("/api/new_log")
async def new_log(request: Request):
    data = await request.json()
    dead = set()
    for ws in clients:
        try:
            await ws.send_json(data)
        except Exception:
            dead.add(ws)
    clients.difference_update(dead)
    return {"status": "sent"}

@app.post("/api/new_alert")
async def new_alert(request: Request):
    data = await request.json()
    message = {
        "type": "alert",
        "log": data.get("log"),
        "advice": data.get("advice")
    }
    dead = set()
    for ws in clients:
        try:
            await ws.send_json(message)
        except Exception:
            dead.add(ws)
    clients.difference_update(dead)
    return {"status": "alert sent"}

@app.get("/api/stats")
def get_stats():
    normal_count = 0
    anomaly_count = 0
    timeline = []

    if os.path.exists(PREDICTION_LOG):
        with open(PREDICTION_LOG, 'r') as f:
            lines = f.readlines()
            # for line in lines:
            #     parts = line.strip().split(",")
            #     if len(parts) >= 3:
            #         timestamp, label, log = parts
            #         if label == 'normal':
            #             normal_count += 1
            #         elif label == 'anomaly':
            #             anomaly_count += 1
            #         timeline.append({"time": timestamp, "label": label})
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    timestamp, label = parts[0], parts[1]
                    log = ",".join(parts[2:]).strip()
                    if label == 'normal':
                        normal_count += 1
                    elif label == 'anomaly':
                        anomaly_count += 1
                    timeline.append({"time": timestamp, "label": label})

    return JSONResponse({
        "normal": normal_count,
        "anomaly": anomaly_count,
        "timeline": timeline
    })
