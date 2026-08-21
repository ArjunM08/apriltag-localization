try: 
    from dt_apriltags import Detector
    import cv2
    from picamera2 import Picamera2
    import numpy
    import socket
    import pickle
    import struct
except:
    raise RuntimeError("Importing libraries failed")

ATdetector = Detector(families='tag36h11',
                      nthreads = 2,
                      quad_decimate=2.0,
                      quad_sigma = 0.0,
                      refine_edges = 1,
                      decode_sharpening = 0.25,
                      debug = 0)

cam_params = [650.0, 650.0, 320.0, 240.0]

cv2.startWindowThread()
picam2 = Picamera2()

main = {'format': 'RGB888', 'size':(640,480)}
lores = {'format':'YUV420', 'size':(640, 480)}

picam2.configure(picam2.create_preview_configuration(main, lores = lores))
picam2.start()

HOST = '192.168.1.223'
PORT = 6800

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Using TCP to ensure data recived in order for accurate pose estimation
connection.connect((HOST, PORT))
    
def sendDataToServer(payload):
    serialized_payload = pickle.dumps(payload)
    header = struct.pack("!I", len(serialized_payload))
    
    connection.send(header + serialized_payload)
    
while True:
    with picam2.captured_request() as request:
        grey = request.make_array('lores')[:480, :640]
        
        tags = ATdetector.detect(grey, True, camera_params = cam_params, tag_size=0.1)
        
        for tag in tags:
            for idx in range(len(tag.corners)):
                cv2.line(grey, tuple(tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx,:].astype(int)), (255,0,0))
            sendDataToServer((tag.corners, tag.tag_id))
            print("sent!")
            #print(str(tag.tag_id))
        
        cv2.imshow("Tags", grey)
    cv2.waitKey(1)
                         
        
