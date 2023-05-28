import threading
import socket

# local host
host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while true:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            nickname = nickname[clients.index(client)]
            broadcast(f"{nickname} was sent to the phantom zone!".encode('ascii'))
            nicknames.remove(nickname)
            break