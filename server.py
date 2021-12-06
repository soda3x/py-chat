import socket
import sys
import threading
import datetime
from rich import print
import common


def broadcast(message):  # broadcast function declaration
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:  # recieving valid messages from client
            message = client.recv(1024)
            broadcast(message)
        except:  # removing clients
            timestamp = datetime.datetime.now()
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} {} left!'.format(
                timestamp, ((nickname).encode('ascii'))))
            nicknames.remove(nickname)
            break


def receive():  # accepting multiple clients
    while True:
        timestamp = datetime.datetime.now()
        client, address = server.accept()
        print("{} Connected with {}".format(str(timestamp), str(address)))
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("{} Nickname is {}".format(str(timestamp), nickname))
        broadcast("{} joined!   ".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if len(sys.argv) < 2:
    print("Failed to start server\nUsage: server.py ip port")
    quit()

common.try_import('rich')

host = sys.argv[1]  # ip
port = int(sys.argv[2])  # port

# socket initialization
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))  # binding host and port to socket
server.listen()

print("Started chat server on {}:{}...".format(str(host), str(port)))

clients = []
nicknames = []

receive()
