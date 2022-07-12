import logging
import socket
import threading

from server import HOST, PORT, send, recv


def listener(conn: socket.socket):
    with conn:
        print('[CONNECTION ESTABLISHED]')

        while True:
            try:
                message = recv(conn)
            except Exception as e:
                logging.error('[CONNECTION INTERRUPT', e)
                break

            if '[CLOSE CONNECTION]' in message:
                break

            print('[MESSAGE RCV]: {}'.format(message))

    print('[CONNECTION CLOSED]')


def handler(conn: socket.socket):
    while True:
        client_input = input()
        command = client_input.split()

        if command[0] == 'Ping':
            send(conn, 'Ping')
        elif command[0] == "Quit":
            send(conn, 'Quit')
        else:
            send(conn, client_input)


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        # THREAD FOR SERVER LISTENER
        threading.Thread(target=listener, args=(client,)).start()
        handler(client)
