import cv2
from ultralytics import YOLO
import numpy as np
import serial
import time 
    
cam = cv2.VideoCapture(0)
prev_t = 0

model = YOLO('spf3.pt')
#pxPID = ""
ser = serial.Serial(port="/dev/cu.usbserial-0001", baudrate=115200)

def send_data(data): 
    print(f"Sending: {data}")
    ser.write(f"{data}\n".encode())
    ser.flush()
    time.sleep(0.1)
zone1 = False
while True:
    signal = None
    if ser.in_waiting:
        try:
            signal = ser.readline().decode()
            print("Signal: ", signal)
        except:
            signal = None
    _,frame = cam.read()
    if signal == "zone1":
        zone1 = True
    if zone1:
        curr_t = time.time()
        fps = 1/(curr_t - prev_t)
        prev_t = curr_t
        h,w,c = frame.shape
        cv2.putText(frame, f"fps: {fps:.1f}", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 0, 255), 2)
        
        results = model(frame,conf=0.65)
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])  
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)
                cv2.putText(frame, class_name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
                obj_centre = (x1+x2)//2
                frame_centre = w//2
                pxPID = frame_centre - obj_centre
                send_data(pxPID)
    cv2.imshow("f",frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        ser.close()
        cv2.destroyAllWindows()
        cam.release()
        break        