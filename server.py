# Написати два класи (сервер і клієнт), використовуючи socket.
#
# 1. На старті сервер повинен очікувати на з’єднання клієнтів.
# Якщо клієнт під’єднався, сервер повинен отримувати повідомлення від клієнта у форматі json,
# яке містить ID клієнта та timestamp. Сервер повинен надрукувати це повідомлення,
# оновити timestamp і надіслати повідомлення назад клієнту.
#
# 2. Клієнт повинен з’єднатися з сервером на старті і надсилати кожної секунди
# плвідомлення json, яке буде містити ID клієнта та timestamp. Клієнти теж повинні друкувати те, що прийшло від сервера.
#
# Потрібно створити один об’єкт сервера і 5 об’єктів клієнта. Почекати 10 секунд і завершити роботу.
import socket
import sys
import datetime
import json
from concurrent.futures.thread import ThreadPoolExecutor


class Server:
    def __init__(self, host='', port=5555):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.bind()
        self.listen()
        self.executor = ThreadPoolExecutor(max_workers=10)

    def bind(self):
        try:
            self.socket.bind((self.host, self.port))
        except socket.error as msg:
            print('Bind failed.', msg)
            sys.exit()
        print('Socket bind complete')

    def listen(self, backlog=10):
        # Start listening on socket
        self.socket.listen(backlog)
        print('Socket now listening')

    def handle_request(self, data):
        print("Received from client: ", data)
        timestamp = datetime.datetime.now().timestamp()
        data["timestamp"] = timestamp
        print("Updated data", data)

        return data

    def handle_connection(self, conn):
        while True:
            data = conn.recv(1024)

            if not data:
                break

            try:
                data = json.loads(data.decode())
            except ValueError:
                data = json.dumps({"error": "Bad request"})
                conn.sendall(json.dumps(data).encode())
            else:
                response = self.handle_request(data)
                conn.sendall(json.dumps(response).encode())

        conn.close()

    def start(self):
        try:
            while True:
                # wait to accept a connection - blocking call
                conn, addr = self.socket.accept()
                print('Connected with ', addr[0], ':', str(addr[1]))
                self.executor.submit(self.handle_connection, conn)

        finally:
            print("Stop")
            self.socket.close()

s = Server()
s.start()








