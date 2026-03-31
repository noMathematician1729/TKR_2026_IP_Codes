import cv2
import math
import numpy as np
from ultralytics import YOLO
from vision_module import get_camera_detections
from navigation_module4final import run_navigation_logic

model_z1 = YOLO('spf3.pt')
model_z2 = YOLO('symbol300.pt')

cap = cv2.VideoCapture(0)

lower_green = np.array([35, 100, 40])
upper_green = np.array([85, 255, 255])
lower_red1  = np.array([0,   100, 40])
upper_red1  = np.array([10,  255, 255])
lower_red2  = np.array([160, 100, 40])
upper_red2  = np.array([180, 255, 255])

green_flag = False
red_flag   = False
r_pressed  = False
zone       = 1

l_cap = None
r_cap = None
curr_pos   = [0]
next_pos   = [0]
next_label = ["empty"]
block_dict = {i: 'empty' for i in range(1, 13)}


def apply_ui(frame, results, mdl):
    h, w, _ = frame.shape
    cv2.line(frame, (w // 2, 0),        (w // 2, h),        (255, 0, 0), 2)
    cv2.line(frame, (0, h // 3),        (w, h // 3),        (255, 0, 0), 2)
    cv2.line(frame, (0, (2 * h) // 3),  (w, (2 * h) // 3),  (255, 0, 0), 2)
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = mdl.names[int(box.cls[0])]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame


def start_zone2():
    global l_cap, r_cap
    l_cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Camera 2 → Port 003
    r_cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)  # Camera 3 → Port 002


def stop_zone2():
    global l_cap, r_cap
    if l_cap:
        l_cap.release()
        l_cap = None
    if r_cap:
        r_cap.release()
        r_cap = None
    cv2.destroyWindow('Left_Cam')
    cv2.destroyWindow('Right_Cam')


while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    if zone == 1:
        success, frame = cap.read()
        if not success:
            continue

        if key == ord('r'):
            r_pressed = True

        h, w, _ = frame.shape
        f_center = (w // 2, h // 2)
        l1_x = int(w * 0.25)
        l2_x = int(w * 0.75)

        cv2.line(frame, (l1_x, 0), (l1_x, h), (0, 255, 255), 2)
        cv2.line(frame, (l2_x, 0), (l2_x, h), (0, 255, 255), 2)

        object_in_middle = False
        object_detected  = False

        results = model_z1(frame, verbose=False)

        for r in results:
            for box in r.boxes:
                object_detected = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                obj_cx = (x1 + x2) // 2
                obj_cy = (y1 + y2) // 2
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                if l1_x < obj_cx < l2_x:
                    object_in_middle = True
                    cv2.circle(frame, (obj_cx, obj_cy), 5, (255, 255, 0), -1)

                    if key == ord('c'):
                        dx    = obj_cx - f_center[0]
                        dy    = obj_cy - f_center[1]
                        angle = math.degrees(math.atan2(dy, dx))
                        print(f"Angle: {angle:.2f} degrees")

        if object_in_middle:
            print(True)
        elif object_detected and key == ord('n'):
            print("next")

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        green_detected = False
        red_detected   = False

        mask_g = cv2.inRange(hsv, lower_green, upper_green)
        contours_g, _ = cv2.findContours(mask_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours_g:
            if 10000 <= cv2.contourArea(cnt) <= 30000:
                green_detected = True
                x, y, wb, hb = cv2.boundingRect(cnt)
                cx, cy = x + wb // 2, y + hb // 2
                cv2.rectangle(frame, (x, y), (x + wb, y + hb), (0, 255, 0), 2)
                cv2.putText(frame, "Green", (cx - 20, cy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        mask_r = cv2.add(cv2.inRange(hsv, lower_red1, upper_red1),
                         cv2.inRange(hsv, lower_red2, upper_red2))
        contours_r, _ = cv2.findContours(mask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours_r:
            if 10000 <= cv2.contourArea(cnt) <= 30000:
                red_detected = True
                x, y, wb, hb = cv2.boundingRect(cnt)
                cx, cy = x + wb // 2, y + hb // 2
                cv2.rectangle(frame, (x, y), (x + wb, y + hb), (0, 0, 255), 2)
                cv2.putText(frame, "Red", (cx - 20, cy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        if green_detected:
            green_flag = True
            red_flag   = False
        if red_detected:
            red_flag   = True
            green_flag = False

        if r_pressed:
            if green_flag:
                print("repeat")
                green_flag = False
            if red_flag:
                print("zone2")
                red_flag = False
                zone = 2
                start_zone2()
                cv2.destroyWindow("Detection Frame")
            r_pressed = False

        if zone == 1:
            cv2.imshow("Detection Frame", frame)

    elif zone == 2:
        ret_l, f_l = l_cap.read()
        ret_r, f_r = r_cap.read()
        if not ret_l or not ret_r:
            continue

        res_l = model_z2.predict(f_l, conf=0.7, verbose=False)
        res_r = model_z2.predict(f_r, conf=0.7, verbose=False)

        L_cls, M_cls, R_cls = get_camera_detections(res_l, res_r, model_z2)

        f_l = apply_ui(f_l, res_l, model_z2)
        f_r = apply_ui(f_r, res_r, model_z2)

        if key == ord('c') or key == ord('n'):
            if key == ord('n'):
                curr_pos[0] = next_pos[0]

            next_pos, next_label, block_dict = run_navigation_logic(
                L_cls, M_cls, R_cls, curr_pos, next_pos, next_label, block_dict
            )

            print(f"CURRENT POSITION: {curr_pos[0]}")
            print(f"NEXT TARGET     : {next_pos[0]}")
            print(f"NEXT LABEL      : {next_label[0]}")

        cv2.imshow('Left_Cam',  f_l)
        cv2.imshow('Right_Cam', f_r)

cap.release()
stop_zone2()
cv2.destroyAllWindows()