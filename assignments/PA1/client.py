import socket
import sys
import threading
from const import HOST, PORT
from server_hadler import cmd, listener, connect


if __name__ == '__main__':
    try:
        if len(sys.argv) == 1 and sys.argv[1] == 'default':
            info = (HOST, PORT)
        elif len(sys.argv) == 2:
            info = (sys.argv[1], int(sys.argv[2]))
        else:
            info = (HOST, PORT)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(info)
            # THREAD FOR SERVER LISTENER
            threading.Thread(target=listener, args=(client,)).start()
            cmd(client)

    except Exception as e:
        text = 'ERROR?'
        # print(text, e)
        connect()
