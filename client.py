import socket
import threading

nickname = input("Choose a nickname: ")
if nickname == 'admin':
    password = input("Enter password for admin: ")


# user joins
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


# while loop to allow user to keep sending messages until it fails
def recieve():
    # stop_thread breaks the client's conncetion if true. Prob a better way to do this but it works
    stop_thread = False
    while True:
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            # set nickname
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                # if-statement to allow admin to type in password. next_message only works if the user inputs 'admin' for username
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connected was refused! Wrong password!")
                        stop_thread = True
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# setting up threads to allow for both functions to simultaneously run at the same time
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()