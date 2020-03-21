from socket import *
import time


def client(estDistant, dessin, pseudo):
    if estDistant:
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
        ip = wherefrom[0]
        s.close()
    else:
        ip = '127.0.0.1'
    port = 5000

    monSocket = socket()
    monSocket.connect((ip, port))  # On se conncecte à l'ip du stream
    data = monSocket.recv(1)
    if data == b'\x01':  # envoi du dessin
        monSocket.send(pseudo.encode())
        print('on dessine')
        while True:
            data = dessin.get()
            monSocket.send(data)
            if data == b'\xff\xff\xff\xff':
                break
    elif data == b'\x02':  # téléchargement du dessin
        monSocket.send(pseudo.encode())
        print("on regarde")
        dessin.put(b'L')
        while True:
            data = monSocket.recv(4)
            if data == b'\x11':
                print('c parti')
            dessin.put(data)
            if data == b'\xff\xff\xff\xff':  # fin
                break
    elif data == b'\xff':
        print("fermeture")
    else:
        print(data)
    monSocket.close()
    print("conn fermée")
