import socket
from const import ENCODING, MESSAGE_LENGTH_SIZE, TOPIC_SUBSCRIPTION


def send(conn: socket.socket, message):
    packet = message.encode(ENCODING)
    packet_length = str(len(packet)).encode(ENCODING)
    packet_length += b' ' * (MESSAGE_LENGTH_SIZE - len(packet_length))

    conn.send(packet_length)
    conn.send(packet)


def sendall(publication, t):
    for conn in TOPIC_SUBSCRIPTION[t]:
        send(conn, publication)


def recv(conn: socket.socket):
    received = conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING)
    message_length = int(received)
    return conn.recv(message_length).decode(ENCODING)
