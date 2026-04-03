import serial
import cv2
import time

ser = serial.Serial(
    port="/dev/cu.usbserial-0001",
    baudrate=115200,
    timeout=1
)
print("Listening on serial port...")

path = "apriltags/black.jpg"
img = cv2.imread(path)
try:
    while True:
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode().strip()
                print("Received:", data)
                if data == "ready":
                    path = "apriltags/tag36_11_00001.png"
                elif data == "prev":
                    path = "apriltags/tag36_11_00002.png"
                elif data == "next":
                    path = "apriltags/tag36_11_00003.png"

                new_img = cv2.imread(path)
                if new_img is not None:
                    img = new_img
                else:
                    print("Failed to load image:", path)

            except Exception as e:
                print("Error decoding data:", e)

        if img is not None:
            cv2.imshow("frame", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.close()
    cv2.destroyAllWindows()