import cv2
from ultralytics import YOLO
import numpy as np
import serial
import time 
    
cam = cv2.VideoCapture(0)
prev_t = 0

model = YOLO('spf3.pt')
pxPID = None
ser = serial.Serial(port="/dev/cu.usbmodem11101", baudrate=9600, timeout=1)

while True:
    signal = None
    if ser.in_waiting:
        try:
            signal = ser.readline().decode()
            print("Signal: ", signal)
        except:
            signal = None
    _,frame = cam.read()

    curr_t = time.time()
    fps = 1/(curr_t - prev_t)
    prev_t = curr_t
    h,w,c = frame.shape
    cv2.putText(frame, f"fps: {fps:.1f}", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 0, 255), 2)
    
    results = model(frame,conf=0.8)
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
            if pxPID:
                print(pxPID)

                message = str(pxPID)          
                ser.write((message + "\n").encode())

                print("Sent:", message)
                        
    
    cv2.imshow("f",frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break