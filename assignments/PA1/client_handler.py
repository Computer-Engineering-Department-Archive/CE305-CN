import logging
import socket
import threading
import time
from const import TOPIC_SUBSCRIPTION
from focket import send, recv
from fserver import subscribe, unsubscribe, publish


def listener(conn: socket.socket, addr, close, ping):
    ack = 0
    recent_ack = 0
    recent = None
    buff = []

    while True:
        try:
            message = recv(conn)
        except Exception as e:
            text = '$ CONN INT' + str(addr)

            logging.error(text, e)
            print(text)

            break

        text = '$ FROM: ' + str(addr) + '\n $ RCV: ' + str(message)
        print(text)

        message = message.split()
        if message[0] == "Subscribe":
            try:
                subscribe(conn, message[1:])

                suback = 'SubAck\n'
                send(conn, suback)
            except Exception as e:
                failed = '$ SUB FAILED'

                logging.error(failed, e)
                send(conn, failed)
        elif message[0] == "Publish":
            try:
                publish(message[1], message[2:])

                puback = 'PubAck'
                send(conn, puback)

                ack = len(TOPIC_SUBSCRIPTION[message[1]])
                recent_ack = 0
                buff = message
                recent = time.time()
            except Exception as e:
                failed = '$ PUB FAILED'

                logging.error(failed, e)
                send(conn, failed)
        elif message[0] == 'Ping':
            try:
                send(conn, 'Pong')
            except Exception as e:
                failed = '$ PONG FAILED'

                logging.error(failed, e)
                send(conn, failed)
        elif message[0] == "Pong":
            del ping[:]
        elif message[0] == 'AckQ':
            recent_ack = recent_ack + 1
            print('$ ACK {} RCV FROM {}'.format(recent_ack, addr))
        elif message[0] == "Quit":
            close.append(1)
            break

        if recent is not None:
            if recent_ack == ack:
                recent = None
                recent_ack = 0
                ack = 0
            elif (time.time() - recent) >= 5.0:
                publish(buff[1], buff[2:])
                recent_ack = 0


def handler(conn: socket.socket, addr):
    with conn:
        text = '$ NEW CONN: ' + str(addr)
        print(text)
        # CONST
        recent = time.time()
        close = []
        pings = []
        # CONNECTION HANDLER
        t = threading.Thread(target=listener, args=(conn, addr, close, pings))
        t.start()

        while True:
            if (time.time() - recent) >= 10.0:
                if len(pings) != 0:
                    ping = '$ PONG NOT RCV: ' + str(len(pings)) + ' ON: ' + str(addr)
                    print(ping)
                if len(pings) == 3:
                    ping3 = '$ PONG NOT RCV. CONN CLOSE ON: ' + str(addr)
                    print(ping3)

                    break
                # UPDATE CONST
                recent = time.time()
                send(conn, "Ping")
                pings.append(1)

            if len(close) > 0:
                break

        unsubscribe(conn)
        send(conn, "Closed")

    close = '$ CONN CLOSE ON: ' + str(addr)
    print(close)
