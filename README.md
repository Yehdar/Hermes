# Hermes
## Abstract
Remember LAN parties or when you used to play with your friends locally on the same wifi? Well, this is the same thing but a messaging platform.

<p align="center"><img src="https://github.com/Yehdar/hermes/blob/master/demo/demo.png" width="80%"></p>

## Things to note:
- so i used the socket and threading libary for the low-level networking and running multiple processes simultaneously
- since its a simple project, i dont really need to use an IPv6 address. I understand IPv6 is the future and stuff, so I will play around with it in the future. But for now, we use IPv4

#### Admin Rules:
- username is "admin" and password is "masteroogway12"
- /kick kicks users
- /ban bans users

## Configuration:
1. Open two terminals (1 server, 1 client)
2. Be in the file directory in both terminals
3. run "python3 server.py" on the server terminal and "python3 client.py" on the client terminal
