import socket
import threading

nickname = input("Choose a nickname: ")

# user joins
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# while loop to allow user to keep sending messages until it fails
def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            # set nickname
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break