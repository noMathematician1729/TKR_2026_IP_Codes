import cv2
from ultralytics import YOLO
import numpy as np
import time 
    
cam = cv2.VideoCapture(0)
prev_t = 0

model = YOLO('spf3.pt')

while True:
    _, frame = cam.read()

    curr_t = time.time()
    fps = 1 / (curr_t - prev_t)
    prev_t = curr_t

    h, w, c = frame.shape

    cv2.putText(frame, f"fps: {fps:.1f}", (100, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 0, 255), 2)

    results = model(frame, conf=0.8)

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)
            cv2.putText(frame, class_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

            # Compute center offset (PID error)
            obj_centre = (x1 + x2) // 2
            frame_centre = w // 2
            pxPID = frame_centre - obj_centre

            # Instead of sending via serial → just print / display
            print(f"PID Error: {pxPID}")

            cv2.putText(frame, f"Error: {pxPID}", (x1, y2 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imshow("YOLO Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()