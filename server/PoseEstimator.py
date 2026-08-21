
import numpy as np
from Apriltags import Apriltags
import cv2

class PoseEstimator:
    def __init__(self, camera_matrix, distortion_coeffs) -> None:
        self.CAMERA_MATRIX = camera_matrix
        self.DIST_COEFFS = distortion_coeffs
    
    def solveForCameraToTagPose(self, TagCorners: list, TagID: int):
        try:
            success, rvec, tvec = cv2.solvePnP(
                objectPoints = Apriltags.get(TagID),
                imagePoints = TagCorners,
                cameraMatrix = self.CAMERA_MATRIX,
                distCoeffs = self.DIST_COEFFS,
                flags = cv2.SOLVEPNP_ITERATIVE
            )
        except Exception as e:
            raise RuntimeError("Error solving for camera to tag pose") from e
        
        if success:
            return rvec, tvec
        if not success:
            raise RuntimeWarning("SolvePnP failed, using default values")

    def getCameraPose(self, TagCorners: list, TagID: int):
        rvec, tvec = self.solveForCameraToTagPose(TagCorners, TagID)
        
        print(f"rvec: {rvec}")
        print(f"tvec: {tvec}")


