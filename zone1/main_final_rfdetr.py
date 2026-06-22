import cv2
from rfdetr import RFDETRNano
import serial
import time
from pupil_apriltags import Detector

import zone_decision as zd
print("RFDETR Ready")
# ==================================
# Camera
# ==================================
cam = cv2.VideoCapture(0)

detector = Detector(
    families='tag36h11',
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25
)

# ==================================
# RF-DETR Model
# ==================================
model = RFDETRNano.from_checkpoint(
    "/home/robocon/robocon_main/main/main_final/spearhead_20_rfdetr.pth",
    device="cuda"
)

model.optimize_for_inference()

# ==================================
# Class Names
# Replace with your actual classes
# ==================================
class_names = {
    0: "Fist",
    1: "Palms",
    2: "Plam",
    3: "Spearheads"
}

# ==================================
# Serial
# ==================================
ser = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    timeout=1
)

curr_t = 0
prev_t = 0

signal = None

z1 = True
z2 = None
z3 = None

FOV = 27
tag0 = False
angleF = False
# ==================================
# Main Loop
# ==================================
while True:

    # -------------------------------
    # Read serial signal
    # -------------------------------
    if ser.in_waiting > 0:
        signal = ser.readline().decode().strip()

    z1, z2, z3 = zd.zones(
        z1,
        z2,
        z3,
        signal
    )

    # -------------------------------
    # Zone 1
    # -------------------------------
    if z1:

        ret, frame = cam.read()

        if not ret:
            continue
        #April tag
        angle = True
        tag0 = False
        detections = detector.detect(frame)
        for det in detections:
            if det.tag_id == 0:
                angle = False
                ser.write(b"nxt\n")
                ser.flush()

        curr_t = time.time()

        fps = (
            1 / (curr_t - prev_t)
            if (curr_t - prev_t) > 0
            else 0
        )

        prev_t = curr_t

        h, w, _ = frame.shape

        frame_center = w // 2

        # RF-DETR inference
        detections = model.predict(
            frame,
            threshold=0.6,
            device="cuda"
        )

        boxes = detections.xyxy
        scores = detections.confidence
        classes = detections.class_id

        best_box = None
        best_distance = float("inf")

        for box, score, cls in zip(
            boxes,
            scores,
            classes
        ):

            x1, y1, x2, y2 = map(int, box)

            obj_center = (x1 + x2) // 2

            distance = abs(
                obj_center - frame_center
            )

            if distance < best_distance:

                best_distance = distance

                best_box = {
                    "xyxy": [x1, y1, x2, y2],
                    "class_id": int(cls),
                    "score": float(score)
                }

        angle = "no"

        if best_box is not None:

            cls_id = best_box["class_id"]

            name = class_names.get(
                cls_id,
                str(cls_id)
            )

            x1, y1, x2, y2 = best_box["xyxy"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"{name}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            obj_center = (x1 + x2) // 2

            px_offset = (
                frame_center -
                obj_center
            )

            angle = px_offset * FOV / w

            cv2.putText(
                frame,
                f"Angle: {angle:.1f}",
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            cv2.circle(
                frame,
                (frame_center, h // 2),
                5,
                (0, 0, 255),
                -1
            )

            cv2.circle(
                frame,
                (obj_center, (y1 + y2)//2),
                5,
                (255, 0, 0),
                -1
            )

        # Send angle to STM32
        if angleF:
            ser.write(
                f"{angle}\n".encode("utf-8")
            )

        ser.write(
            b"ack\n"
        )

        # FPS display
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

        cv2.imshow(
            "RF-DETR Zone1",
            frame
        )

        print(angle)
        if signal == "ack":
            angle = True
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
ser.close()


