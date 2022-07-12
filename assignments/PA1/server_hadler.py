import logging
import socket
import threading
import time

from const import HOST, PORT
from focket import send, recv
from fclient import publish, subscribe, quit_conn, pong

_pong = True
_sub = None
_pub = None


def listener(conn: socket.socket):
    global _pong, _pub, _sub

    while True:
        try:
            message = recv(conn)
        except Exception as e:
            interrupt = '$ CONN INT'

            logging.error(interrupt, e)
            print(interrupt)

            break
        if message == "Ping" and _pong:
            pong(conn)
        elif 'SubAck' in message:
            print('$ SUBACK RCV')
            if _sub is not None:
                _sub = None
        elif 'PubAck' in message:
            print('$ PUBACK RCV')
            if _pub is not None:
                _pub = None
        elif 'MESSAGE' in message:
            print('$ MESSAGE RCV. SEND ACKQ')
            send(conn, 'AckQ')
        elif message == "Closed":
            print("$ CONN CLOSED")
            conn.close()

            break

        if _sub is not None and (time.time() - _sub) >= 10.0:
            print('$ SUBACK DIDNT RCV.')
            _sub = None
        if _pub is not None and (time.time() - _pub) >= 10.0:
            print('$ SUBACK DIDNT RCV.')
            _pub = None

        text = '$ RCV: ' + message
        print(text)

    connect()


def cmd(conn: socket.socket):
    global _pong, _pub, _sub

    while True:
        command = input().split()

        if len(command) == 0:
            continue
        if command[0] == "Publish":
            if len(command) == 1:
                err = '$ INCOMPLETE TOPIC & MESSAGE BODY'
                print(err)

                continue
            if len(command) == 2:
                err = '$ INCOMPLETE MESSAGE BODY'
                print(err)

                continue

            if _pub is None:
                publish(conn, command[1], command[2:])
                _pub = time.time()
            else:
                print('HAS\'NT RCV PUBACK FOR PREVIOUS REQUEST. TRY AGAIN LATER.')
        elif command[0] == "Subscribe":
            if len(command) == 1:
                err = '$ INCOMPLETE TOPIC'
                print(err)

                continue

            if _sub is None:
                subscribe(conn, command[1:])
                _sub = time.time()
            else:
                print('HAS\'NT RCV SUBACK FOR PREVIOUS REQUEST. TRY AGAIN LATER.')
        elif command[0] == 'Ping':
            send(conn, 'Ping')
        elif command[0] == "Quit":
            quit_conn(conn)


def connect():
    try:
        client_input = input("HOST, PORT : ")
        if client_input == "default":
            _info = (HOST, PORT)
        else:
            addr, port = tuple(client_input.split())
            _info = (addr, int(port))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(_info)
            # THREAD SERVER LISTENER
            threading.Thread(target=listener, args=(client,)).start()
            print('$ CONN OPEN')

            cmd(client)
    except Exception as e:
        text = 'ERROR!'
        # print(text, e)
        connect()
