import numpy as np
#constants for apriltags
# id : corner positions in 3D space (in meters)

#Coordinates are in [x, y, z] space where:
# positive x = right
# positive y = up
# positive z = out from the tag

APRILTAG_SIZE = 0.2 #meters

def getApriltagCorners(tagCenter: list, tagSize: float = APRILTAG_SIZE) -> list:
    distToEdge = tagSize/2
    x, y, z = tagCenter
    return np.array([
        [x - distToEdge, y - distToEdge, z],
        [x + distToEdge, y - distToEdge, z],
        [x + distToEdge, y + distToEdge, z],
        [x - distToEdge, y + distToEdge, z]
    ], dtype=np.float32)

Apriltags = {  
    0 : getApriltagCorners([0, 0, 0]),
}