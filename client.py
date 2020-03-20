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

while True:
    data = monSocket.recv(4)
    px = int.from_bytes(data[0:2], 'big', signed=False)
    py = int.from_bytes(data[2:4], 'big', signed=False)
    print('px: ' + str(px) + "  py : " + str(py))
    if data == b'\xff\xff\xff\xff':  # fin
        break
monSocket.close()
