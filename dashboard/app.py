from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Store connected WebSocket clients
clients = set()

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    print("✅ Client connected")
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        print("❌ Client disconnected")
    finally:
        clients.remove(websocket)

@app.post("/api/new_log")
async def new_log(data: dict):
    # print(f"📦 New log received: {data}")
    await broadcast({"type": "log", "data": data})
    return {"status": "ok"}

@app.post("/api/new_alert")
async def new_alert(data: dict):
    print(f"🚨 New alert received: {data}")
    await broadcast({"type": "alert", "data": data})
    return {"status": "ok"}

async def broadcast(message):
    disconnected = set()
    for client in clients:
        try:
            await client.send_json(message)
        except:
            disconnected.add(client)
    clients.difference_update(disconnected)
