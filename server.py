import threading
import socket

# local host
host = '127.0.0.1'
port = 55555

# built-in socket method that intializes what IPv and what internet protocol (TCP)
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
    while True:
        try:
            msg = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                # 5 because "KICK "
                name_to_kick = msg.decode('ascii')[5:]
                kick_user(name_to_kick)
            elif msg.decode('ascii').startswith('BAN'):
                # 4 because "BAN" "
                name_to_ban = msg.decode('ascii')[4:]
                kick_user(name_to_ban)
                # banned list
                with open('bans.text', 'a') as f:
                    f.write(f'{name_to_ban}\n')
                print(f'{name_to_ban} was banned!')
            else:
                broadcast(msg)
        except:
            if client in clients:
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
        
        # to check if client was previously banned
        with open('bans.txt', 'r') as f:
            bans = f.readlines() 
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        # super simple if-statement password system for admin. Too lazy to implement hash algorithms.
        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password !=  'masteroogway12':
                client.send('REFUSE'.encode('ascii'))
                client.close
                continue

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

def kick_user(name):
    if name in nicknames:
        # calculates position of name to kick the client out
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))

print("Server is listening...")
receive()