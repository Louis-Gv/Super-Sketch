from socket import *
import time

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 50000))

timeout = time.time() + 10

while 1:
    data, wherefrom = s.recvfrom(1500, 0)  # (b'du texte', ('192.168.1.32', 62587))
    if data.decode() == "SuperS":
        print(wherefrom[0])
        break
    # if time.time() > timeout:
    #   break


port = 5000

monSocket = socket()
monSocket.connect((wherefrom[0], port))  # On se conncecte à l'ip du stream

message = input(" -> ")

while message != 'q':
    monSocket.send(message.encode())
    data = monSocket.recv(1024).decode()

    print('Received from server: ' + data)

    message = input(" -> ")

monSocket.close()
