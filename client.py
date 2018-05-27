import socket
import datetime
import uuid
from concurrent.futures import ThreadPoolExecutor

import json
from time import sleep, time


class Client:
    def __init__(self, host='', port=5555):
        self.id = uuid.uuid1()
        self.socket = socket.socket()
        self.host = host
        self.port = port

    def start(self):
        self.socket.connect((self.host, self.port))
        start = time()

        while True:
            ts = json.dumps({
                "timestamp": datetime.datetime.now().timestamp(),
                "ID": str(self.id)
            })
            print("Send to server: ", ts)
            self.socket.send(str(ts).encode())
            data = self.socket.recv(1024).decode()

            print('Received from server: ', data)
            sleep(1)
            if time() - start >= 10:
                print(time() - start)
                break

        self.socket.close()


with ThreadPoolExecutor(max_workers=5) as executor:
    for _ in range(5):
        c = Client()
        executor.submit(c.start)



