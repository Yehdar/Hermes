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
    # keeps sending messages until the client is removed
    while true:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            nickname = nickname[clients.index(client)]
            broadcast(f'{nickname} was sent to the phantom zone!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    # a while loop to accept every client. NO AUTHENTICATION BTW lol
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # asks user to enter nickname, recieves it, and then store it in the clients list
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # let everyone know a new client joined on the server
        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        # lets client know they connected
        client.send('Connected to the server!'.encode('ascii'))

        # starts a new thread each time to manage a new client. Better this way because 
        # it allows for multiple messages to be sent at the same time, rather than waiting for one to go at a time
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()