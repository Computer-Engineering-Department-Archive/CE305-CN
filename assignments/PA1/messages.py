from enum import Enum


class ServerMessages(Enum):
    # COMMANDS
    MESSAGE = 'MESSAGE'
    SUBACK = 'SUBACK'
    PUBACK = 'PUBACK'
    PING = 'PING'
    PONG = 'PONG'
    # CONNECTION
    OPENED = 'OPENED'
    CLOSED = 'CLOSED'


class ClientMessages(Enum):
    PUBLISH = 'PUBLISH'
    SUBSCRIBE = 'SUBSCRIBE'
    PING = 'PING'
    PONG = 'PONG'
    # CONNECTION
    QUIT = 'QUIT'
