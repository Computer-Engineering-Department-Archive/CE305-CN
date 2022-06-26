import logging
import socket
import threading
from const import HOST, PORT
from focket import send, recv
from fclient import publish, subscribe, quit_conn, pong

_pong = True


def listener(conn: socket.socket):
    global _pong

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
        elif message == "Closed":
            print("$ CONN CLOSED")
            conn.close()

            break

        text = '$ RCV: ' + message
        print(text)

    connect()


def handler(conn: socket.socket):
    global _pong

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

            publish(conn, command[1], command[2:])
        elif command[0] == "Subscribe":
            if len(command) == 1:
                err = '$ INCOMPLETE TOPIC'
                print(err)

                continue

            subscribe(conn, command[1:])
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

            handler(client)
    except Exception as e:
        text = 'ERROR!'
        # print(text, e)
        connect()
