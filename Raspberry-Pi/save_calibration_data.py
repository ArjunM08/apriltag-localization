import os
import cv2
from picamera2 import Picamera2

SAVE_DIR = "calibration-images"
os.makedirs(SAVE_DIR, exist_ok=True)

camera = Picamera2()
camera.configure(camera.create_preview_configuration())
camera.start()

counter = 1
print("Press 's' to save, 'q' to quit.")

while True:
    frame = camera.capture_array()
    cv2.imshow("Camera", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Done.")
        break
    elif key == ord('s'):
        filename = os.path.join(SAVE_DIR, f"image_{counter:03d}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")
        counter += 1

camera.stop()
cv2.destroyAllWindows()