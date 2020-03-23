# Code réseau
# 'D' = dessin, puis x sur 2o, y sur 2o, size sur 1o, coul sur 1o
# 't' = test / proposition, puis utf8 sur 16o
# 'P' = Pseudo, idConn+16o en utf8
# 'T' = tableau de joueur
# 'F' = Fin / Déco
# 'G' = Go
# 'R' = Rôle, Joueur, Dessine

from socket import *
import threading


def client(estDistant, tunel, pseudo):
    def reception():
        while True:
            try:
                message_recu = monSocket.recv(200)
            except ConnectionResetError:
                break
            if not message_recu:  # Si la connexion est close par le serv
                break
            tunel.send(message_recu)
        print("Client arrêté. Connexion interrompue.")
        monSocket.close()

    def emission():
        while True:
            message_emis = tunel.recv()  # Blocant
            monSocket.send(message_emis)

    if estDistant:  # récup de l'ip sur le msg broadcasté par le serv
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', 50000))
        while 1:
            data, emmeteur = s.recvfrom(1500, 0)  # (b'du texte', ('192.168.1.32', 62587))
            if data.decode() == "SuperS":  # Si on a reçu "SuperS" sur le port 50 000
                break
        ip = emmeteur[0]
        s.close()
    else:
        ip = '127.0.0.1'
    port = 5000

    # Programme principal - Établissement de la connexion :
    monSocket = socket()
    monSocket.connect((ip, port))  # On se conncecte à l'ip du stream
    monSocket.send(('P,' + pseudo).encode())
    tunel.send(('P,' + pseudo).encode())

    # Dialogue avec le serveur : on lance deux threads pour gérer
    # indépendamment l'émission et la réception des messages :
    threadEmission = threading.Thread(target=emission)
    threadEmission.daemon = True
    threadReception = threading.Thread(target=reception)
    threadEmission.start()
    threadReception.start()
