
import numpy as np
from server.Apriltags import ApriltagCorners, Apriltags
import cv2
import math
import numpy as np

class PoseEstimator:
    def __init__(self, camera_matrix, distortion_coeffs) -> None:
        self.CAMERA_MATRIX = camera_matrix
        self.DIST_COEFFS = distortion_coeffs
    
    def solveForCameraToTagPose(self, TagCorners: list, TagID: int):
        try:
            success, rvec, tvec = cv2.solvePnP(
                objectPoints = np.array(ApriltagCorners.get(TagID)),
                imagePoints = TagCorners,
                cameraMatrix = self.CAMERA_MATRIX,
                distCoeffs = self.DIST_COEFFS,
                flags = cv2.SOLVEPNP_ITERATIVE
            )
        except Exception as e:
            print(e)
            raise RuntimeError("Error solving for camera to tag pose")
        
        if success:
            return rvec, tvec
        if not success:
            raise RuntimeWarning("SolvePnP failed, using default values")

    def getCameraPose(self, TagCorners: list, TagID: int):
        rvec, tvec = self.solveForCameraToTagPose(TagCorners, TagID)
        
        tag_to_field = np.eye(4)
        tag_to_field[:3,3] = Apriltags.get(TagID)

        R, _ = cv2.Rodrigues(rvec) # convert to rotation matrix
        T = np.eye(4)
        T[:3, :3] = R
        T[:3, 3] = tvec.flatten() #Transform representing translation and rotation

        #inverts cam-to-tag and finds tag-to-cam
        #multiply matrices to find camera pose in real coordinates
        camera_in_field = tag_to_field @ np.linalg.inv(T)

        position = camera_in_field[:3, 3]
        rotation = camera_in_field[:3, :3]

        # flip_y = np.array([
        #     [1,  0,  0],
        #     [0, -1,  0],
        #     [0,  0,  1]
        # ])

        # rotation = flip_y @ rotation @ flip_y

        return position, rotation


