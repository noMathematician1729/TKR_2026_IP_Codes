import cv2
from ultralytics import YOLO
import numpy as np
import serial
import zone1.Cam_data as cd
import zone1.Row_data as rd
import zone1.pos_change as pc
    
left = cv2.VideoCapture(1)
right = cv2.VideoCapture(2)
sph = cv2.VideoCapture(3)

model_zone1 = YOLO('spf3.pt')
model_zone2 = YOLO('symbol300.pt')

j=1
areaR=areaG=0
curr_pos= [0]
next_pos = [0]
next_column = [0]
data_to_next = 0
class_of_next = ['empty']
curr_column = [0]
curr_row = [0]
pos_to_change = False
ser = serial.Serial(port="COMx", baudrate=9600, timeout=1)
z1 = True
z2 = False  
FOV = 80

box_dict = {
    1 : 'empty',
    2: 'empty',
    3: 'empty',
    4: 'empty',
    5: 'empty',
    6: 'empty',
    7: 'empty',
    8: 'empty',
    9: 'empty',
    10: 'empty',
    11: 'empty',
    12: 'empty',
}

while True:
    signal = None
    if ser.in_waiting:
        try:
            signal = ser.readline().decode()
            print("Signal: ", signal)
        except:
            signal = None
    
    if z1==True:
        sph_bool, sph_cam = sph.read()
        hz1,wz1,cz1 = sph_cam.shape
        frame_width = wz1
        hsv_z1 = cv2.cvtColor(sph_cam, cv2.COLOR_BGR2HSV)
        
        lower_green = np.array([35, 60, 180])
        upper_green = np.array([95, 255, 255])

        lower_red1 = np.array([0, 70, 180])
        upper_red1 = np.array([12, 255, 255])
        lower_red2 = np.array([160, 70, 180])
        upper_red2 = np.array([179, 255, 255])

        mask_green = cv2.inRange(hsv_z1, lower_green, upper_green)
        mask_r = cv2.bitwise_or(cv2.inRange(hsv_z1, lower_red1, upper_red1),cv2.inRange(hsv_z1, lower_red2, upper_red2))

        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(mask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        results_z1 = model_zone1(sph_cam, conf= 0.7, verbose=False)
        sph_centre = None
        if results_z1[0].boxes is not None:
            for box in results_z1[0].boxes:
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                name = model_zone2.names[cls_id]
                sph_centre = (x1+x2)//2
                dx = sph_centre - 320
                spf_angle = (dx/frame_width)*FOV

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            if signal == 'f':
                if sph_centre is not None and 260 <= sph_centre <= 380:
                    process_zone1 = True
                    print("YES | Angle:", spf_angle)
            else:
                print("NEXT")
                process_zone1 = False
        for cnt in contours_red:
                xr, yr, wr, hr = cv2.boundingRect(cnt)
                arear = wr * hr
        for cnt in contours_green:
                xg, yg, wg, hg = cv2.boundingRect(cnt)
                areag = wg * hg
        
        


    
    if z2==True:
        ret_l, frame = left.read()
        ret_r, frame1 = right.read()

        results = model_zone2(frame, conf=0.7, verbose=False)

        results1 = model_zone2(frame1, conf=0.7, verbose=False)

        cv2.line(frame, (320, 0), (320, 480), (255, 0, 0), 2)
        cv2.line(frame, (0, 160), (640, 160), (255, 0, 0), 2)
        cv2.line(frame, (0, 320), (640, 320), (255, 0, 0), 2)

        cv2.line(frame1, (320, 0), (320, 480), (255, 0, 0), 2)
        cv2.line(frame1, (0, 160), (640, 160), (255, 0, 0), 2)
        cv2.line(frame1, (0, 320), (640, 320), (255, 0, 0), 2)
        xc = yc = xc1 = yc1 = 0



        if results[0].boxes is not None:
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                name = model_zone2.names[cls_id]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        if results1[0].boxes is not None:
            for box in results1[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                name = model_zone2.names[cls_id]

                cv2.rectangle(frame1, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame1, name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        if signal == 'c':
            left_class, mid_class = cd.Left_camera_Detection(results, model_zone2)
            right_class = cd.Right_camera_Detection(results1, model_zone2)
            box_dict, data_to_next, class_of_next = rd.first_row(left_class, mid_class, right_class, box_dict, data_to_next, class_of_next)
            while(j<=3):
                if j==data_to_next:
                    next_pos[0] = data_to_next
                    next_column[0] = data_to_next
                j+=1
            print("current position", curr_pos[0])
            print("next position", next_pos[0])
            print("class of next", class_of_next[0])
        

        if signal=='n':
            curr_pos[0]=next_pos[0]
            curr_column[0] = next_column[0]
            left_class, mid_class = cd.Left_camera_Detection(results, model_zone2)
            right_class = cd.Right_camera_Detection(results1, model_zone2)
            curr_row, curr_column, box_dict, class_of_next, data_to_next, pos_to_change, next_pos, curr_pos= rd.further_rows(left_class, mid_class, right_class, curr_pos, curr_row, curr_column, box_dict, class_of_next, data_to_next, pos_to_change, next_pos)
            print("current position", curr_pos[0])
            print("next position", next_pos[0])
            print("class of next", class_of_next[0])
            if pos_to_change==True:
                curr_row, curr_column, data_to_next, next_pos, curr_pos, next_column = pc.pos_is_true(curr_row, curr_column, data_to_next, next_pos, curr_pos, next_column)
            if pos_to_change==False:
                curr_row, curr_column, data_to_next, next_pos, curr_pos, next_column = pc.pos_is_false(curr_row, curr_column, data_to_next, next_pos, curr_pos, next_column)

    
        cv2.imshow('left', frame)
        cv2.imshow('right', frame1)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

left.release()
right.release
cv2.destroyAllWindows()