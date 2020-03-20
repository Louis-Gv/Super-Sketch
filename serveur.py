import time
from socket import *
from multiprocessing import Process, Value, Pipe


def diffuIpHote():  # Diffusion d'un msg sur tout le reseau local pour pouvoir récupérer l'ip
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while True:
        # print('diffusion')
        s.sendto("SuperS".encode(), ('<broadcast>', 50000))
        time.sleep(1)


def traitement(conn, pipe, nbClient, mode):
    nbClient.value += 1
    if nbClient.value == 100:  # si ca quitte
        conn.send(b'\xff')
        conn.close()
    if mode == 1:  # si dessine
        conn.send(b'\x01')
        while nbClient.value < 2:
            time.sleep(0.05)
        while True:
            data = conn.recv(4)
            pipe.send(data)
            if not data:
                break
    if mode == 2:  # si ca lit
        print('bruh')
        conn.send(b'\x02')
        while True:
            element = pipe.recv()
            conn.send(element)
            if not element:
                break
    conn.close()

def serveur(nbClient):
    # On va initialiser le serveur d'ecoute
    host = ""
    port = 5000

    serveurSocket = socket()
    serveurSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serveurSocket.bind((host, port))
    serveurSocket.listen(5)

    procDiffu = Process(target=diffuIpHote)
    procDiffu.start()  # Lancement du processus de la diffusion de l'ip


    emmeteur1, recepteur1 = Pipe()


    conn, addr = serveurSocket.accept()
    print("Got connection 1")
    process = Process(target=traitement, args=(conn, emmeteur1, nbClient, 1))
    process.daemon = True
    process.start()
    print("Started")

    conn2, addr2 = serveurSocket.accept()
    print("Got connection 2")
    process2 = Process(target=traitement, args=(conn2, recepteur1, nbClient, 2))
    process2.daemon = True
    process2.start()
    print("Started")

    while True:
        time.sleep(5)
