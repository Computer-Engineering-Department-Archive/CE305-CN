import logging
import socket
import threading


# CONNECTION CONF
HOST = '127.0.0.1'
PORT = 8087
# PACKET CONF
MESSAGE_LENGTH_SIZE = 64
ENCODING = 'utf-8'


def send(conn: socket.socket, message):
    packet = message.encode(ENCODING)
    packet_length = str(len(packet)).encode(ENCODING)
    packet_length += b' ' * (MESSAGE_LENGTH_SIZE - len(packet_length))

    conn.send(packet_length)
    conn.send(packet)


def recv(conn: socket.socket):
    received = conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING)
    message_length = int(received)
    return conn.recv(message_length).decode(ENCODING)


def handler(conn: socket.socket, addr):
    with conn:
        print('[NEW CONNECTION]: {}'.format(addr))

        while True:
            try:
                message = recv(conn)
            except Exception as e:
                logging.error('[CONNECTION INTERRUPT]', e)
                break

            command = message.split()
            if command[0] == 'Ping':
                send(conn, 'Pong')
            elif command[0] == 'Quit':
                send(conn, '[CLOSE CONNECTION]')
            else:
                send(conn, '[ACK]')

            print('[MESSAGE RCV] [FROM {}]: {}'.format(addr, message))

    print('[CONNECTION {} CLOSED]'.format(addr))


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        while True:
            _conn, _addr = server.accept()
            threading.Thread(target=handler, args=(_conn, _addr)).start()