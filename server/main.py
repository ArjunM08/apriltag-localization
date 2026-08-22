import asyncio
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from server.SocketServer import SocketServer
from server.CameraCalibrationConstants import CAMERA_MATRIX, DIST_COEFFS
from server.PoseEstimator import PoseEstimator
import numpy as np
from fastapi import FastAPI, WebSocket
import threading
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory='server/static', html=True), name="static")

HOST = '192.168.1.223'
PORT = 6800

latest_pose = {
    "x": 0.0,
    "y": 0.0,
    "z": 0.0,
    "R": np.eye(3).tolist()
}
def begin_server():
    socket_server = SocketServer(HOST, PORT)
    socket_server.start_server()

    poseEstimator = PoseEstimator(CAMERA_MATRIX, DIST_COEFFS)

    while True:
        data = socket_server.get_full_Payload()
        position, rotation = poseEstimator.getCameraPose(np.array(data[0]), data[1])
        latest_pose["x"] = position[0]
        latest_pose["y"] = position[1]
        latest_pose["z"] = position[2]
        latest_pose["R"] = rotation.tolist()

    socket_server.close_connection()

@app.on_event("startup")
async def startup():
    server_thread = threading.Thread(target=begin_server, daemon=True)
    server_thread.start()
    

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text(json.dumps(latest_pose))
            await asyncio.sleep(0.033)  # Send updates every 33ms (~30 FPS)
    except websocket.WebSocketDisconnect:
        print("WebSocket disconnected")

@app.get("/")
async def root():
    return FileResponse("server/static/index.html")