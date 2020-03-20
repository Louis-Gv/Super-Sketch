import time
from socket import *
from multiprocessing import Process


def diffuIpHote():  # Diffusion d'un msg sur tout le reseau local pour pouvoir récupérer l'ip
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while True:
        print('diffusion')
        s.sendto("SuperS".encode(), ('<broadcast>', 50000))
        time.sleep(1)


def serveur(dessin):
    # On va initialiser le serveur d'ecoute
    host = ""
    port = 5000

    monSocket = socket()
    monSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    monSocket.bind((host, port))
    monSocket.listen(1)

    procDiffu = Process(target=diffuIpHote)
    procDiffu.start()  # Lancement du processus de la diffusion de l'ip

    conn, addr = monSocket.accept()  # attente d'une connection (prgm bloqué)

    procDiffu.terminate()
    procDiffu.join()  # fin de la diffusion

    print("Connection de: " + str(addr))
    while True:
        pos = dessin.get()
        conn.send(pos)
        if pos == b'\xff\xff\xff\xff':  # fin
            break
        # data = conn.recv(1024).decode()  # recoit et decode les 1024 carac (bloqué)
        # if not data:  # Si client ferme la conn
        #     break
        # print("msg recu : " + data)
        #
        # print("on envoie : " + data.upper())
        # conn.send(data.upper().encode())
    conn.close()
    print("conn fermée")
