# Code réseau. 1er char :
# 'D' = dessin
# 't' = test / proposition
# 'P' = Pseudo
# 'T' = tableau de joueur
# 'F' = Fin / Déconnexion
# 'R' = Rôle, Joueur, Dessine

from socket import *
import threading


def client(ip, tunel, pseudo):
    def reception():
        while True:
            try:
                message_recu = monSocket.recv(1024)
            except ConnectionResetError:
                break
            if not message_recu:  # Si la connexion est close par le serv
                break
            tunel.send(message_recu)  # On envoie le message recu au Process principal
        print("Client arrêté. Connexion interrompue.")
        monSocket.close()

    def emission():
        while True:
            message_emis = tunel.recv()  # On attend les messages du Process principal / Blocant
            monSocket.send(message_emis)  # Puis on les send au serveur pour les redistribuer aux autres clients

    if ip == "0.0.0.0":  # récupérer l'ip sur le msg broadcasté par le serv si pas renseigné
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', 50000))
        while 1:
            data, emmeteur = s.recvfrom(1500, 0)  # (b'du texte', ('192.168.1.32', 62587))
            if data.decode() == "SuperS":  # Si on a reçu "SuperS" sur le port 50 000
                break
        ip = emmeteur[0]
        s.close()

    port = 5000

    # Programme principal - Établissement de la connexion :
    monSocket = socket()
    monSocket.connect((ip, port))  # On se conncecte à l'ip du stream
    monSocket.send(('P,' + pseudo).encode())  # Envoi du pseudo
    tunel.send(('P,' + pseudo).encode())

    # Dialogue avec le serveur : on lance deux threads pour gérer indépendamment l'émission et la réception des messages :
    threadEmission = threading.Thread(target=emission)
    threadEmission.daemon = True  # Pour le kill a la fin du Process
    threadReception = threading.Thread(target=reception)
    threadEmission.start()
    threadReception.start()
