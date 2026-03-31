import serial
import time

arduino = serial.Serial(port='ttyTHS1', baudrate=9600, timeout=1)

def send_data(data):
    print(f"Sending: {data}")
    arduino.write(f"{data}\\n".encode())
    arduino.flush()
    time.sleep(0.1)
    response = arduino.readline().decode().strip() 
    if response:
        print(f"Arduino responded: {response}")

if __name__ == "__main__":
    time.sleep(2)
    print("Connected to Arduino")

    while True:
        user_input = input("Enter data to send: ")
        send_data(user_input)

