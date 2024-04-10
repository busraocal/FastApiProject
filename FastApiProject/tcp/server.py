import socket
import requests
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432
url = "http://127.0.0.1:8000"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode().split(",")
            location_date = datetime.fromtimestamp(int(data[2]))
            location_date = location_date.strftime("%Y-%m-%d %H:%M:%S")
            insert_data = {"device_id": data[0], "location": data[1],
                           "location_date": location_date}
            requests.post(f"{url}/insert_location", json=insert_data)
