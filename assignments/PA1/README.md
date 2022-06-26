# CE305-CN
## Message Broker is a more complex implementation of publisher design pattern where a server sends messages to clients which are a member of specific club.
### files
#### CONST
This file includes all client/server configs
#### SERVER
Server is constructed around 4 files 1) server 2) client handler 3) fserver (server functions) and 4) fsocket (socket functions e.g. send, rcv).
These files work with each other to handel requests and listen to incoming messages from clients; save messages in message queue and deliver them to their destinations.
#### CLIENT
Client is constructed around 4 files 1) client 2) server handler 3) fclient (client functions) and 4) fsocket (as mentioned above).
These files read clients commands, parse them and send specific messages, acks and packets to server. it also handler some errors such as invalid imput etc.

overall implementation is easy to understand and easy to use. for further questions contact bardia.ardakanian@yahoo.com.
