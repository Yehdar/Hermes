from config import HOST, PORT
import socket
import threading

nickname = input("Choose a nickname: ")
if nickname == 'admin':
    password = input("Enter password for admin: ")

# user joins
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# stop_thread breaks the client's conncetion if true. Prob a better way to do this but it works
stop_thread = False

# while loop to allow user to keep sending messages until it fails
def recieve():
    while True: 
        global stop_thread
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
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        # i have to break it here as well so the client cannot write messages as well. without this, the client can still write but not recieve
        if stop_thread:
            break
        message = f'{nickname}: {input("")}' 
        # admin's commands
        # the message slice starts after the username + 2 (includes ": ")
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2].startswith('/kick'):
                    #  i could have split the message into a list and then extract the last index to get the name, but i believe this is a lot faster and easier lol. That
                    # said, it forces the admin to properly space out command
                    # the + 6 stands for "/kick "
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                    # the + 5 stands for "/ban "
                elif message[len(nickname)+2].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                print("Commands can only be executed by the admin!")

        client.send(message.encode('ascii'))

# setting up threads to allow for both functions to simultaneously run at the same time
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
