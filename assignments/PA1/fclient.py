import socket
from focket import send, recv


def quit_conn(conn: socket.socket):
    message = "Quit"
    send(conn, message)


def publish(conn: socket.socket, topic, body):
    message = "Publish " + topic
    for b in body:
        message += " " + b
    send(conn, message)


def subscribe(conn: socket.socket, topics):
    message = "Subscribe"
    for topic in topics:
        message += " " + topic
    send(conn, message)


def pong(conn: socket.socket):
    send(conn, 'Pong')
