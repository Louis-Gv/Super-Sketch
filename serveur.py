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


def traitement(conn, pipe, nbClient, clients, lockServ, mode):
    if mode == 1:  # si dessine
        conn.send(b'\x01')
        pseudo = conn.recv(16)
        lockServ.acquire()
        clients[nbClient.value*17] = b'D'
        y = 0
        for i in range(nbClient.value*17+1, (nbClient.value+1)*17):
            if y < len(pseudo):
                clients[i] = pseudo[y]
            y += 1
        nbClient.value += 1
        lockServ.release()
        while True:
            try:
                data = conn.recv(4)
            except ConnectionError:
                pass
            else:
                for i in range(nbClient.value-1):
                    pipe[i].send(data)
                if not data:
                    break
    if mode == 2:  # si ca lit
        conn.send(b'\x02')
        pseudo = conn.recv(16)
        lockServ.acquire()
        clients[nbClient.value * 17] = b'L'
        idClient=nbClient.value
        y = 0
        for i in range(nbClient.value * 17 + 1, (nbClient.value+1) * 17):
            if y < len(pseudo):
                clients[i] = pseudo[y]
            y += 1
        nbClient.value += 1
        lockServ.release()
        emmeteur = 0
        while True:
            element = pipe[emmeteur].recv()
            if element == b'\x11':
                for i in range(4):
                    if clients[i*17] == b'D':
                        emmeteur = i
                        print('emmeteur')
                        break
            try:
                conn.send(element)
            except ConnectionError:
                print(str(idClient)+" est parti")
                break
            if not element:
                break
    conn.close()

def serveur(nbClient,clients,lockServ):
    # On va initialiser le serveur d'ecoute
    host = ""
    port = 5000

    serveurSocket = socket()
    serveurSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serveurSocket.bind((host, port))
    serveurSocket.listen(5)

    conn1vers2, conn2vers1 = Pipe()
    conn1vers3, conn3vers1 = Pipe()
    conn1vers4, conn4vers1 = Pipe()
    conn2vers3, conn3vers2 = Pipe()
    conn2vers4, conn4vers2 = Pipe()
    conn3vers4, conn4vers3 = Pipe()

    conn, addr = serveurSocket.accept()
    process = Process(target=traitement, args=(conn, (conn1vers2, conn1vers3, conn1vers4), nbClient, clients, lockServ, 1))
    process.daemon = True
    process.start()

    conn2, addr2 = serveurSocket.accept()
    print("Got connection 2")
    # TODO + if not started
    process2 = Process(target=traitement, args=(conn2, (conn2vers1, conn2vers3, conn2vers4), nbClient, clients, lockServ, 2))
    process2.daemon = True
    process2.start()

    conn3, addr3 = serveurSocket.accept()
    # TODO + if not started
    print("Got connection 3")
    process2 = Process(target=traitement, args=(conn3, (conn3vers1, conn3vers2, conn3vers4), nbClient, clients, lockServ, 2))
    process2.daemon = True
    process2.start()

    conn4, addr4 = serveurSocket.accept()
    # TODO + if not started
    print("Got connection 4")
    process2 = Process(target=traitement, args=(conn4, (conn4vers1, conn4vers2, conn4vers3), nbClient, clients, lockServ, 2))
    process2.daemon = True
    process2.start()

    while True:
        time.sleep(5)
