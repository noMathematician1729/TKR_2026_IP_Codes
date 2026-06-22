import cv2
from ultralytics import YOLO
import serial
import time
import zone_decision as zd
import closest_sph as csp
import april_tag_detection as atd

CAM_FOV     = 80        
CAM_INDEX   = 0         
MODEL_PATH  = '/home/robocon/main/spearheads_26n_first.pt'
SERIAL_PORT = "/dev/ttyTHS1"
BAUD_RATE   = 115200
frame_width = 640

# ─────────────────────────────────────────────
# Initialisation
# ─────────────────────────────────────────────
cam   = cv2.VideoCapture(CAM_INDEX)
model = YOLO(MODEL_PATH)
ser   = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)

prev_t    = time.time()
last_sent = None
signal    = None
z1 = False
z2 = False
z3 = False

ser.write(b"jetsonReady\n")

# ─────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────
while True:

    signal = None

    if ser.in_waiting > 0:
        try:
            signal = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Received signal: {signal}")
        except Exception as e:
            print(f"Serial read error: {e}")

    z1, z2, z3 = zd.zones(z1, z2, z3, signal)

    # ══════════════════════════════════════════════════════════════════════════
    # ZONE 1
    # ══════════════════════════════════════════════════════════════════════════
    if z1:
        ret, frame = cam.read()
        if not ret:
            print("cameraError")
            continue

        # ── FPS ───────────────────────────────────────────────────────────────
        curr_t = time.time()
        fps    = 1 / (curr_t - prev_t) if (curr_t - prev_t) != 0 else 0
        prev_t = curr_t

        h, w, _ = frame.shape
        frame_centre_x = w // 2
        frame_centre_y = h // 2

        results  = model(frame, conf=0.7)
        best_box = csp.closest(None, float('inf'), frame_centre_x, results)

        if best_box is not None:
            cls_id     = int(best_box.cls[0])
            class_name = model.names[cls_id]
            x1, y1, x2, y2 = map(int, best_box.xyxy[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            horizontal = cx - frame_centre_x

            angle = (horizontal / frame_width) * (CAM_FOV)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, class_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.circle(frame, (frame_centre_x, frame_centre_y), 5, (0, 0, 255), -1)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

            cv2.line(frame, (frame_centre_x, frame_centre_y), (cx, cy), (0, 255, 255), 1)

            cv2.putText(frame, f"Angle: {angle:.2f} deg",
                        (frame_centre_x - 80, frame_centre_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if angle != last_sent:
                ser.write(f"{angle}\n".encode('utf-8'))
                print(f"Sent angle: {angle:.2f}")
                last_sent = angle

        else:
            ser.write(f"next\n".encode('utf_8'))
            cv2.putText(frame, "No target", (frame_centre_x - 50, frame_centre_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # ── FPS overlay ───────────────────────────────────────────────────────
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 0, 255), 2)

        # ── April tag detection ───────────────────────────────────────────────
        april_tag = atd.april_tag_detected(frame, None)

        if april_tag == 0:
            z1 = True
            ser.write(b"sexDone\n")
        elif april_tag == 1:
            z1 = True
            ser.write(b"resetZone1\n")
        elif april_tag == 3:
            z1 = False
            ser.write(b"exit\n")

        cv2.imshow("Zone 1", frame)

    # ══════════════════════════════════════════════════════════════════════════
    # ZONE 2
    # ══════════════════════════════════════════════════════════════════════════
    if z2:
        pass

    # ══════════════════════════════════════════════════════════════════════════
    # ZONE 3
    # ══════════════════════════════════════════════════════════════════════════
    if z3:
        pass

    # ── Quit ──────────────────────────────────────────────────────────────────
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    ser.flush()

# ─────────────────────────────────────────────
# Cleanup
# ─────────────────────────────────────────────
cam.release()
cv2.destroyAllWindows()
ser.close()