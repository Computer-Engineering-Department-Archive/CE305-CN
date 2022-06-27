import socket
from const import TOPIC_SUBSCRIPTION
from focket import send, sendall


def subscribe(conn: socket.socket, topics):
    register(conn, topics)
            
    message = "$ SUBSCRIBING ON :"
    for topic in TOPIC_SUBSCRIPTION.keys():
        if conn in TOPIC_SUBSCRIPTION[topic]:
            message += " " + topic
            
    send(conn, message)


def register(conn, topics):
    for topic in topics:
        if topic in TOPIC_SUBSCRIPTION.keys():
            if conn not in TOPIC_SUBSCRIPTION[topic]:
                TOPIC_SUBSCRIPTION[topic].append(conn)
        else:
            TOPIC_SUBSCRIPTION[topic] = [conn]


def unsubscribe(conn):
    for subscriber in TOPIC_SUBSCRIPTION.keys():
        if conn in TOPIC_SUBSCRIPTION[subscriber]:
            TOPIC_SUBSCRIPTION[subscriber].remove(conn)


def publish(topic, message):
    publication = "$ MESSAGE \"" + topic + '\"'
    for c in message:
        publication += " " + c

    for t in TOPIC_SUBSCRIPTION.keys():
        if t == topic:
            sendall(publication, t)
            break
