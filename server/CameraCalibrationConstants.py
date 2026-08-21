import numpy as np

CAMERA_MATRIX = np.array([[603.43854642,   0.0,           310.21395414],
                          [0.0,            604.26649542,  245.78167848],
                          [0.0,            0.0,           1.0        ]], 
                          dtype=np.float32)

DIST_COEFFS = np.array([0.12437986, -0.35577559, 0.0042249, -0.00272845, 0.17593277], dtype=np.float32)