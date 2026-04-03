import cv2
from ultralytics import YOLO
import numpy as np
import serial
import time 
from zones import detectZones
    
cam = cv2.VideoCapture(0)
prev_t = 0

model = YOLO('spf3.pt')
#pxPID = ""
ser = serial.Serial(port="/dev/cu.usbserial-0001", baudrate=115200)
from pupil_apriltags import Detector

zone1 = zone2 = zone3 = False
detector = Detector(families='tag36h11', nthreads=1, quad_decimate=1.0, 
                    quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25)

while True:
    if ser.in_waiting >0:
        signal = ser.readline().decode().strip()
    _, frame = cam.read()
    if not _:
        print("Frame read error")
        break

    z1, z2, z3 = detectZones(signal)
