import cv2
import math
import numpy as np
from ultralytics import YOLO

model = YOLO('spf3.pt') 
cap = cv2.VideoCapture(0)

lower_green = np.array([35, 100, 40])
upper_green = np.array([85, 255, 255])

lower_red1 = np.array([0, 100, 40])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 40])
upper_red2 = np.array([180, 255, 255])

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    key = cv2.waitKey(1) & 0xFF
    h, w, _ = frame.shape
    f_center = (w // 2, h // 2)
    l1_x, l2_x = int(w * 0.25), int(w * 0.75)

    cv2.line(frame, (l1_x, 0), (l1_x, h), (0, 255, 255), 2)
    cv2.line(frame, (l2_x, 0), (l2_x, h), (0, 255, 255), 2)

    results = model(frame, verbose=False)
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            obj_cx, obj_cy = (x1 + x2) // 2, (y1 + y2) // 2
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            if l1_x < obj_cx < l2_x:
                print(True)
                if key == ord('c'):
                    dx, dy = obj_cx - f_center[0], obj_cy - f_center[1]
                    angle = math.degrees(math.atan2(dy, dx))
                    print(f"Angle: {angle:.2f} degrees")
            else:
                if key == ord('n'):
                    print("next")

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask_g = cv2.inRange(hsv, lower_green, upper_green)
    conts_g, _ = cv2.findContours(mask_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in conts_g:
        area = cv2.contourArea(cnt)
        if 10000 <= area <= 30000:
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            if key == ord('r'):
                print("repeat")

    mask_r = cv2.add(cv2.inRange(hsv, lower_red1, upper_red1), cv2.inRange(hsv, lower_red2, upper_red2))
    conts_r, _ = cv2.findContours(mask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in conts_r:
        area = cv2.contourArea(cnt)
        if 10000 <= area <= 30000:
            cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 2)
            if key == ord('r'):
                print("zone 2")

    cv2.imshow("Detection Frame", frame)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()