import socket

host = 'localhost'
port = 5000

monSocket = socket.socket()
monSocket.connect((host, port))

message = input(" -> ")

while message != 'q':
    monSocket.send(message.encode())
    data = monSocket.recv(1024).decode()

    print('Received from server: ' + data)

    message = input(" -> ")

monSocket.close()
