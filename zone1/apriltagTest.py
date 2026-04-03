import cv2
import numpy as np
from pupil_apriltags import Detector

detector = Detector(families='tag36h11', nthreads=1, quad_decimate=1.0, 
                    quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25)

cap = cv2.VideoCapture(0)

print("AprilTag Detection Started")
print("Press 'q' to quit\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame")
        break
    
 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    detections = detector.detect(gray)
    
    for det in detections:
        corners = det.corners.astype(int)
        cv2.polylines(frame, [corners], True, (0, 255, 0), 2)
        

        center = det.center.astype(int)
        cv2.circle(frame, tuple(center), 5, (0, 0, 255), -1)
        
       
        cv2.putText(frame, f"ID: {det.tag_id}", 
                    tuple(center + np.array([10, -10])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        if det.tag_id == 0:
            print("Seen 0")
        elif det.tag_id == 1:
            print("Seen 1")
        elif det.tag_id == 2:
            print("Seen 2")
       
        print("Tag ID: " + str(det.tag_id) + ", Center: (" + str(det.center[0]) + ", " + str(det.center[1]) + ")")
    
   
    cv2.imshow('AprilTag Detection', frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Detection stopped")