from SocketServer import SocketServer
from CameraCalibrationConstants import CAMERA_MATRIX, DIST_COEFFS
from PoseEstimator import PoseEstimator
import numpy as np


HOST = '192.168.1.223'
PORT = 6800

socket_server = SocketServer(HOST, PORT)
socket_server.start_server()

poseEstimator = PoseEstimator(CAMERA_MATRIX, DIST_COEFFS)
poseEstimator.getCameraPose(np.array([
    [210.0, 150.0],     # Top-left corner in image
    [430.0, 160.0],     # Top-right corner in image
    [440.0, 380.0],     # Bottom-right corner in image
    [190.0, 370.0]      # Bottom-left corner in image
], dtype=np.float32), 0)


# while True:
#     msg = socket_server.get_full_Payload()
#     print(msg)


socket_server.close_connection()
