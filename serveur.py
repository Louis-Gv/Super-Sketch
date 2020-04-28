import time
from socket import *
import threading


def diffuIpHote():  # Diffusion d'un msg sur tout le reseau local pour pouvoir récupérer l'ip
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while True:
        # print('diffusion')
        s.sendto("SuperS".encode(), ('<broadcast>', 50000))
        time.sleep(1)


def serveur():  # Process qui va rediffuser les messages à tout les autres clients
    def gestionDuClient(conn, idConnThread):  # Thread de dialogue avec un client :
        # Ce thread a accès à la mémoire du process
        while 1:
            msgClient = conn.recv(1024)
            if msgClient == b'':
                break
            # Faire suivre le message à tous les autres clients :
            for cle in conn_client:
                if cle != idConnThread:  # ne pas le renvoyer à l'émetteur
                    conn_client[cle].send(msgClient)
            if msgClient.decode()[0] == 'F':
                break
        # On ferme la connexion et le thread
        conn.close()  # couper la connexion côté serveur
        del conn_client[idConnThread]  # supprimer son entrée dans le dictionnaire

    # On va initialiser le serveur d'ecoute
    host = ""
    port = 5000

    serveurSocket = socket()
    serveurSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        serveurSocket.bind((host, port))
    except error:
        print("Serveur> La liaison du socket à l'adresse choisie a échoué.")
    else:
        print("Serveur> prêt, en attente de requêtes ...")
        serveurSocket.listen(5)
        
        # Attente et prise en charge des connexions demandées par les clients :
        conn_client = {}  # dictionnaire des connexions clients
        idConn = 1
        while 1:
            connexion, adresse = serveurSocket.accept()
            # Créer un nouvel objet thread pour gérer la connexion :
            threadClient = threading.Thread(target=gestionDuClient, args=(connexion, idConn))
            threadClient.start()
            # Mémoriser la connexion dans le dictionnaire :
            conn_client[idConn] = connexion
            print("Serveur> Client " + str(idConn) + " connecté,  adresse IP : " + adresse[0] + ", port : " + str(adresse[1]))
            idConn += 1
