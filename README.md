# apriltag-localization

Real-time camera pose estimation using AprilTag detection on a Raspberry Pi, with a live 3D visualization in the browser.

**[Demo video](https://youtu.be/viVidHBvcjc)**

---

## What it does

A Pi Camera Module attached to a Raspberry Pi 3B detects AprilTags (family `tag36h11`) in its field of view and streams the corner data over TCP to a Mac. The Mac server runs pose estimation using a calibrated camera matrix, computes the camera's position and orientation relative to the tag using homogeneous transform matrices, and pushes the result to a browser dashboard via WebSocket. The dashboard renders a live 3D scene — modeled after the actual room — where a box representing the camera moves and rotates in real time as you walk around.

---

## Architecture

```
Pi Camera
    │
    ▼
AprilTag Detection (dt-apriltags + OpenCV)
    │  corners + tag ID
    ▼
TCP Socket ──────────────────────────► Mac Server (FastAPI)
                                            │
                              Pose Estimation (OpenCV solvePnP)
                              Coordinate Transforms (NumPy)
                                            │
                                       WebSocket
                                            │
                                            ▼
                                  Browser Dashboard (Three.js)
                                  Live 3D scene, updates at ~30fps
```

---

## Hardware

- Raspberry Pi 3B
- Raspberry Pi Camera Module
- A printed tag36h11 AprilTag mounted on a wall
- Mac (or any machine) on the same local network as the Pi

---

## Project structure

```
apriltag-localization/
├── pi/
│   ├── tag_detection.py      # capture frames, detect tags, send corners over TCP
│   └── requirements.txt
└── server/
    ├── main.py               # FastAPI app, TCP receiver thread, WebSocket endpoint
    ├── socketServer.py       # TCP socket server class
    ├── static/
    │   ├── index.html
    │   └── main.js           # Three.js scene, WebSocket client
    └── requirements.txt
```

---

## Camera calibration

Pose estimation requires a calibrated camera matrix. To calibrate:

1. Print a checkerboard pattern (10×7 squares, 25mm per square)
2. Run the calibration script on the Pi, capturing 20–25 images from varied angles
3. Copy the resulting camera matrix and distortion coefficients into `main.py`

A reference calibration for the Pi Camera Module v2 at 640×480 is included in `main.py` as a starting point, but results will be more accurate with your own calibration.

---

## Running

**On the Pi** — start tag detection and begin streaming corner data:

```bash
source venv/bin/activate
python tag_detection.py --host <your-mac-ip>
```

**On the Mac** — start the server:

```bash
source venv/bin/activate
uvicorn main:app
```

Open `http://localhost:8000` in a browser. Point the Pi camera at the AprilTag and the box in the 3D scene will track the camera's position and orientation in real time.

---

## How the pose estimation works

The Pi sends the four 2D corner coordinates of each detected tag to the Mac. The server uses OpenCV's `solvePnP` with a calibrated camera matrix to recover the rotation and translation vectors describing the tag's pose relative to the camera. These are converted into a 4×4 homogeneous transform matrix, inverted to get camera-relative-to-tag, then composed with the tag's known position in the room to produce the camera's position in world coordinates. The rotation matrix is passed directly to Three.js to orient the scene object.

The coordinate frames are converted from OpenCV convention (Y-down, Z-forward) to Three.js convention (Y-up) by negating the Y axis in both the position vector and the rotation matrix before streaming to the browser.

---

## Tech stack

| Side | Tools |
|---|---|
| Pi | Python, picamera2, OpenCV, dt-apriltags, socket |
| Server | Python, FastAPI, uvicorn, OpenCV, NumPy |
| Frontend | Three.js, vanilla JavaScript, WebSocket API |

---

## What I'd improve with more time

- **Multi-tag fusion** — with multiple tags visible, weighted-average position estimates by detection confidence for a more stable result
- **Kalman filtering** — smooth out the jitter in position estimates between frames
- **Absolute field coordinates** — hardcode known tag positions on a defined field map so the coordinate origin is field-relative rather than tag-relative
- **Latency measurement** — instrument the full pipeline (capture → detect → transmit → estimate → render) and display it live on the dashboard
