import socket
import time

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        location = "loc1"
        device_id = 5
        timestamp = time.time()
        location_data = f"{device_id}, {location}, {int(timestamp)}"
        s.sendall(location_data.encode())
        time.sleep(5)
