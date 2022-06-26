import socket
import threading
from const import HOST, PORT
from client_handler import handler


if __name__ == '__main__':
    lock = threading.Lock()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            _conn, _addr = s.accept()
            threading.Thread(target=handler, args=(_conn, _addr)).start()
