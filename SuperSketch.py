import pygame
from pygame.locals import *
from random import *
import ctypes
from multiprocessing import Process, Pipe
from time import *
# Nos Fichiers
import serveur
import client

#---------------------------------------------FONCTIONS---------------------------------------------------------------------------------------------------------

# Déclaration de la fonction de sélection de la couleur
def selection(pbt, cbt, tbt):
    global couleur  # Définition de variable globale du programme
    global idFrame2  # Animation de l'image
    global txtCouleur 
    idFrame2 = (idFrame2 + 1) % 40
    if idFrame2 < 30:
        fenetre.blit(pal1, pbt)
    else:
        fenetre.blit(pal2, pbt)
    if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de couleur lors d'un clic gauche
        couleur = cbt
        txtCouleur = tbt
    return

#---------Cette fonction permet un dessin beaucoup plus fluide que l'ancien algorithme, il calcule les positions intermiédiares entre deux positions détectées
#en rajoutant des cercles sur ces positions permettant un dessin fluide, de plus ce système est beaucoup plus efficace côté serveur
   
def dessin(fen, couleur, pos, last, rayon):
    dx = last[0]-pos[0]          #On calcule la distance entre les deux positions
    dy = last[1]-pos[1]           
    distance = max(abs(dx), abs(dy))      #On regarde quelle valeur est la plus grande entre dx et dy
    for i in range(distance):          #Pour i jusqu'à distance
        x = int( pos[0]+float(i)/distance*dx)     #On calcule x et y
        y = int( pos[1]+float(i)/distance*dy)
        pygame.display.update(pygame.draw.circle(fen, couleur, (x, y), rayon))   #On met à jour la fenetre avec un nouveau cercle

def selectioncercle1():  # + rayon
    global rayon  # Définition de variable globale du programme
    if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de rayon lors d'un clic
        rayon = rayon + 5
    pygame.time.wait(100)
    return

def selectioncercle2():  # - rayon
    global rayon  # Définition de variable globale du programme
    if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de rayon lors d'un clic
        if rayon > 7:
            rayon = rayon - 5
    pygame.time.wait(100)
    return

def effacfx():
    pygame.draw.rect(fenetre, noir, (1720, 10, 190, 5))
    pygame.draw.rect(fenetre, noir, (1720, 10, 5, 80))
    pygame.draw.rect(fenetre, noir, (1910, 10, 5, 80))
    pygame.draw.rect(fenetre, noir, (1720, 85, 190, 5))
    if pygame.mouse.get_pressed() == (1, 0, 0):  # Detection du clic
        pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
        tunnelParent.send("E".encode())

def reini():
    global couleur
    global rayon
    tunnelParent.send("E".encode())
    txtCouleur = 'noir'
    couleur = noir
    rayon = 10
    pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))

#-----------------------------------------------------------------INITIALISATION DES VARIABLES-------------------------------------------------------------------------------

# FAUT FERMER AVEC ECHAP ET PROPREMENT
if __name__ == '__main__':  # Si c'est le programme pricipal / obligatoire pour multiprocessing

    pygame.init()
    
    # Etat du menu
    fini = False
    acceuil = True
    host = False
    join = False
    online = False
    offline = False
    accip = True

    # Initialisation des variables de l'écran
    ctypes.windll.user32.SetProcessDPIAware()
    largeur = ctypes.windll.user32.GetSystemMetrics(0)
    hauteur = ctypes.windll.user32.GetSystemMetrics(1)
    fenetre = pygame.display.set_mode((largeur, hauteur), pygame.FULLSCREEN)
    pygame.display.set_caption("Super-sketch")

    # Initialisation cadence
    clock = pygame.time.Clock()

    # Initialisation des images
                # Interface
    pal1 = pygame.pal1 = pygame.image.load("img/pal1.png").convert_alpha()
    pal2 = pygame.image.load("img/pal2.png").convert_alpha()
    fon = pygame.image.load("img/pal4.png").convert_alpha()
    imgpeu = pygame.image.load("img/406sw.png").convert_alpha()
    image =pygame.image.load("img/ima.png").convert_alpha()
    gomme1 = pygame.image.load("img/gomme1.png").convert_alpha()
                # Accueil
    logo1 = pygame.image.load("img/lobby/logo1.png")
    logo2 = pygame.image.load("img/lobby/logo2.png")
    nuage = pygame.image.load("img/lobby/nuage.png")
    soleil = pygame.image.load("img/lobby/soleil.png")
    croix = pygame.image.load("img/lobby/croix.png")
    play = pygame.image.load("img/lobby/play.png")

    # Initialisation des couleurs
    rouge = (255, 0, 0)
    vert = (0, 255, 0)
    jaune = (255, 215, 0)
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    bleuc = (38, 188, 254)
    rose = (238, 130, 238)
    marron = (88, 41, 0)
    gris = (192, 192, 192)
    bgColor = (118, 188, 194)

    # Initialisation des boucles
    motChoisi = False
    selectionMot = True
    dess = False
    verif = False

    # Initialisation des polices
    police2 = pygame.font.SysFont("roboto-bold", 35)
    police = pygame.font.SysFont("roboto-bold", 65)

    # Initialisation des message et mots    
    motEcrit = ''
    motdevin = "mot pas choisi"
    motcache = "mot pas choisi"
    listmsg = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']  # Initialisation de la liste du chat vide
    mot1 = mot2 = mot3 = affmot1 = affmot2 = affmot3 = affmotcache = ""
    limots = [word.strip() for word in open("dico.txt", encoding="utf-8")]  # On créer une liste à partir d'un document texte

    # Initialisation des variables de dessin
    rayon = 10
    couleur = noir
    txtCouleur = 'noir'
    lastpos = (0, 0)
    px = 5000
    py = 5000

    #Initialisation des variables de temps
    tempsFin = 0
    temps = 80  # temps pour dessiner

    # Initialisation des variables d'animations et infos positions
                # Nuage
                    # info position nuage Gauche
    xNuageG = randint(-600, 1500)
    vxNuageG = random() / 3 + .15
    yNuageG = randint(0, 250)
                    # info nuage Droite
    xNuageD = randint(400, 2000)
    vxNuageD = -(random() / 3 + .15)
    yNuageD = randint(0, 250)
                # Easter egg
    easter = 0
    xE = 400
    yE = 0
                # Logo et couleur
    idFrame = 0
    idFrame2 = 0
                # Boutons
    padding = 10     # espace autour du texte des btn
                # Croix
    poscroix = croix.get_rect(topright=(largeur - 15, 15))
                # Logo
    poslogo = logo1.get_rect(center=(int(largeur / 2), 100))
                # Play
    posplay = play.get_rect(topright=(largeur - 15, 15))

    # Initialisation des variables du serveur
    pseudo = ''
    ip = ''
    procServeur = Process()  # on initialise les process pour pouvoir les fermer
    procDiffu = Process()
    procClient = Process()
    tunnelParent, tunnelEnfant = Pipe()  # Tunnel de données entre le Process principal et le Process client
    init = True
    start = False
    joueurs = {}
    point = 0
    monID = 0
    roles = {}
    score = {}
    pinceau = pygame.image.load("img/pinceau.png")
    trouves = 0
    
    etat = 0

    # Initialisation des variables de textes
    textPseudo = police.render('Entrez votre pseudo : ', True, (0, 0, 0))  # Rendu du texte avec (texte, antialiasing, noir)
    txtAttente = police.render("En attente de l'hote", True, (0, 0, 0))

    # Initialisation des sons
    pygame.mixer.music.load("musique/menu.wav")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)
    minuteur_song = pygame.mixer.Sound(file="musique/minuteur.ogg")
    playerguessed_song = pygame.mixer.Sound(file="musique/playerGuessed.ogg")
    roundstart_song = pygame.mixer.Sound(file="musique/roundstart.ogg")
    autrequitrouve_song = pygame.mixer.Sound(file="musique/autrequitrouve.ogg")
    erreur_song = pygame.mixer.Sound(file="musique/erreur.ogg")
    #------------------------------------------------------------------INITIALISATION DE L'ACCUEIL------------------------------------------------------------------------------

    # Chargement des boutons

    # Pour positionner mes bouttons j'ai recupéré les rectangles de mes objets Surface(des objets qu'on peut blit contenant
    # les pixels a afficher)
    #
    # Surface.get_rect() retourne un Rect(x=0, y=0, largeur, hauteur) sans couleur, qui recouvre toute la Surface de l'image
    #
    # Surface.get_rect(center=(X, Y)) retourne un Rect(x, y, largeur, hauteur). On donne centre du Rect == X, Y; la méthode
    # retourne x et y correspondant
    #
    # On pourras ensuite utiliser fenetre.blit(btnA, posbtnA) qui placera la Surface(btnA) aux coordonnés de Rect(posbtnA)

    #-----------------------------------------------------Boutton héberger--------------------------------------------#
    
    btnHost = police.render('Héberger Une Partie', True, (0, 0, 0))  # Rendu du texte avec (antialiasing, noir)
    posbtnHost = btnHost.get_rect(center=(int(largeur / 2), 510))

    # Rectangle noir plus grand qui sert de bordure
    borderbtnHost = pygame.Surface((posbtnHost[2] + 2 * padding, posbtnHost[3] + 2 * padding))
    borderbtnHost.fill((0, 0, 0))
    # Trouve le rectangle de la surface (x=0, y=0, largeur, hauteur) pour le plaçage au centre
    posborderbtnHost = borderbtnHost.get_rect(center=(int(largeur / 2), 510))

    # Rectangle bleu plus petit
    paddingbtnHost = pygame.Surface((posbtnHost[2] + padding, posbtnHost[3] + padding))
    paddingbtnHost.fill(bgColor)
    paddingbtnHostOmbre = pygame.Surface((posbtnHost[2] + padding, posbtnHost[3] + padding))  # Pour le survol
    paddingbtnHostOmbre.set_alpha(100)
    paddingbtnHostOmbre.fill((0, 0, 0))
    # Trouve le rectangle de la surface (x=0, y=0, largeur, hauteur) pour le plaçage au centre
    pospaddingbtnHost = paddingbtnHost.get_rect(center=(int(largeur / 2), 510))

    #-----------------------------------------------------Boutton rejoindre-------------------------------------------#
    
    btnJoin = police.render('Rejoindre Une Partie', True, (0, 0, 0))
    posbtnJoin = btnJoin.get_rect(center=(int(largeur / 2), 680))

    borderbtnJoin = pygame.Surface((posbtnJoin[2] + 2 * padding, posbtnJoin[3] + 2 * padding))
    borderbtnJoin.fill((0, 0, 0))
    posborderbtnJoin = borderbtnJoin.get_rect(center=(int(largeur / 2), 680))

    paddingbtnJoin = pygame.Surface((btnJoin.get_rect()[2] + padding, posbtnJoin[3] + padding))
    paddingbtnJoin.fill(bgColor)
    paddingbtnJoinOmbre = pygame.Surface((posbtnJoin[2] + padding, posbtnJoin[3] + padding))
    paddingbtnJoinOmbre.set_alpha(100)
    paddingbtnJoinOmbre.fill((0, 0, 0))
    pospaddingbtnJoin = paddingbtnJoin.get_rect(center=(int(largeur / 2), 680))

    #-----------------------------------------------------Boutton IP manuelle-----------------------------------------#
    
    btnOnline = police.render('Entrer une IP', True, (0, 0, 0))
    posbtnOnline = btnOnline.get_rect(center=(int(largeur / 2), 510))

    borderbtnOnline = pygame.Surface((posbtnOnline[2] + 2 * padding, posbtnOnline[3] + 2 * padding))
    borderbtnOnline.fill((0, 0, 0))
    posborderbtnOnline = borderbtnOnline.get_rect(center=(int(largeur / 2), 510))

    paddingbtnOnline = pygame.Surface((posbtnOnline[2] + padding, posbtnOnline[3] + padding))
    paddingbtnOnline.fill(bgColor)
    paddingbtnOnlineOmbre = pygame.Surface((posbtnOnline[2] + padding, posbtnOnline[3] + padding))  # Pour le survol
    paddingbtnOnlineOmbre.set_alpha(100)
    paddingbtnOnlineOmbre.fill((0, 0, 0))
    pospaddingbtnOnline = paddingbtnOnline.get_rect(center=(int(largeur / 2), 510))

    #-----------------------------------------------------Boutton LAN Automatique-------------------------------------#
    
    btnOffline = police.render('LAN Automatique', True, (0, 0, 0))
    posbtnOffline = btnOffline.get_rect(center=(int(largeur / 2), 680))

    borderbtnOffline = pygame.Surface((posbtnOffline[2] + 2 * padding, posbtnOffline[3] + 2 * padding))
    borderbtnOffline.fill((0, 0, 0))
    posborderbtnOffline = borderbtnOffline.get_rect(center=(int(largeur / 2), 680))

    paddingbtnOffline = pygame.Surface((posbtnOffline[2] + padding, posbtnOffline[3] + padding))
    paddingbtnOffline.fill(bgColor)
    paddingbtnOfflineOmbre = pygame.Surface((posbtnOffline[2] + padding, posbtnOffline[3] + padding))  # Pour le survol
    paddingbtnOfflineOmbre.set_alpha(100)
    paddingbtnOfflineOmbre.fill((0, 0, 0))
    pospaddingbtnOffline = paddingbtnOffline.get_rect(center=(int(largeur / 2), 680))

#--------------------------------------------------------------------LANCEMENT DU PROGRAMME-----------------------------------------------------------------------

    while not fini:  # Boucle tant que le joueur reste dans le menu
        if acceuil:

            # Chargement de la couleur de fond
            fenetre.fill(bgColor)

            # Chargement du logo au centre de l'écran
            fenetre.blit(logo1, poslogo)
    
            # Chargement du soleil
            fenetre.blit(soleil, (1645, 22))
    
            # Chargement de la croix
            fenetre.blit(croix, poscroix)

            pos = pygame.mouse.get_pos()

            # Affichage des nuages
            xNuageG += vxNuageG  # On ajoute la vitesse a la pos du nuage
            if xNuageG > 1930:  # Si sort de l'écran
                xNuageG = randint(-600, -300)  # Retourne au départ
            fenetre.blit(nuage, (int(xNuageG), yNuageG))

            xNuageD += vxNuageD  # On ajoute la vitesse a la pos du nuage
            if xNuageD < -200:  # Si sort de l'écran
                xNuageD = randint(1930, 2100)  # Retourne au départ
            fenetre.blit(nuage, (int(xNuageD), yNuageD))

            # Affichage du logo
            idFrame = (idFrame + 1) % 40  # logo qui bouge tout les 1/4s ou 20images car 80fps
            if idFrame < 20:
                fenetre.blit(logo1, poslogo)
            else:
                fenetre.blit(logo2, poslogo)

            if idFrame < 24:  # barre qui clignotte du pseudo
                barre = '|'
            else:
                barre = ''
                
            # Menu sans avoir cliquer
            if not host and not join:  
                fenetre.blit(borderbtnHost, posborderbtnHost)  # Bordure
                fenetre.blit(paddingbtnHost, pospaddingbtnHost)  # Fond bleu
                if posborderbtnHost.collidepoint(pos):
                    fenetre.blit(paddingbtnHostOmbre, pospaddingbtnHost)
                fenetre.blit(btnHost, posbtnHost)  # Affichage du texte

                fenetre.blit(borderbtnJoin, posborderbtnJoin)  # Bordure
                fenetre.blit(paddingbtnJoin, pospaddingbtnJoin)  # Fond bleu
                if posborderbtnJoin.collidepoint(pos):  # si pos souris est sur le btn rejoindre
                    fenetre.blit(paddingbtnJoinOmbre, pospaddingbtnJoin)
                fenetre.blit(btnJoin, posbtnJoin)  # Affichage du texte

            # Si on héberge
            if host:  
                textPseudo = police.render('Entrez votre pseudo : ' + pseudo + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textPseudo, (400, 530))

            # Si on a cliqué sur rejoindre une partie
            if join and not online and not offline:
                fenetre.blit(borderbtnOnline, posborderbtnOnline)  # Bordure
                fenetre.blit(paddingbtnOnline, pospaddingbtnOnline)  # Fond bleu

                if posborderbtnOnline.collidepoint(pos):
                    fenetre.blit(paddingbtnOnlineOmbre, pospaddingbtnOnline)
                fenetre.blit(btnOnline, posbtnOnline)  # Affichage du texte

                fenetre.blit(borderbtnOffline, posborderbtnOffline)  # Bordure
                fenetre.blit(paddingbtnOffline, pospaddingbtnOffline)  # Fond bleu
                if posborderbtnOffline.collidepoint(pos):  # si pos souris est sur le btn offline
                    fenetre.blit(paddingbtnOfflineOmbre, pospaddingbtnOffline)
                fenetre.blit(btnOffline, posbtnOffline)  # Affichage du texte

            # Si on a cliqué sur le mode LAN
            if offline:
                textPseudo = police.render('Entrez votre pseudo : ' + pseudo + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textPseudo, (400, 530))

            # Si on a cliqué sur le mode ONLINE
            if online:

                # Si on a pas rentré l'IP
                if accip:
                    textIP = police.render("Entrez l'addresse IP du serveur : " + ip + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                    fenetre.blit(textIP, (400, 530))
                else:
                    textPseudo = police.render('Entrez votre pseudo : ' + pseudo + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                    fenetre.blit(textPseudo, (400, 530))
                    
            # On récupère les actions du joueurs
            for event in pygame.event.get():

                # Si le joueur appuie sur ECHAP ou la croix
                if event.type == QUIT or (event.type == MOUSEBUTTONDOWN and poscroix.collidepoint(pos)):
                    acceuil = False
                    fini = True
                if event.type == pygame.KEYDOWN:

                    # Si on héberge, que l'on rejoint en LAN, ou rejoint en ONLINE et que l'IP a été saisie
                    if host or (join and (offline or (online and not accip))):  # Si une touche est pressée
                        if event.key == pygame.K_RETURN:  # Si entrer
                            if host:
                                procDiffu = Process(target=serveur.diffuIpHote)
                                procDiffu.daemon = True
                                procDiffu.start()  # Lancement du processus de la diffusion de l'ip
                                procServeur = Process(target=serveur.serveur)
                                procServeur.start()  # lancement du serveur dans un processus parallèle
                            acceuil = False  # fin de l'acceuil

                        # Si on appuie sur retour
                        elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                            pseudo = pseudo[:-1]  # du 1er caractère inclus jusqu'au dernier exclu

                        # Si on écrit son pseudo 
                        elif len(pseudo) < 16:  # 16 caractères max
                            pseudo += event.unicode

                    # Si on est sur la page qui demande l'IP
                    elif online and accip:
                        if event.key == pygame.K_RETURN and ip != '':
                            accip = False

                        # Si on appuie sur retour
                        elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                            ip = ip[:-1]  # du 1er caractère inclus jusqu'au dernier exclu
                            
                        # Si on écrit l'IP
                        elif len(ip) < 16:  # 16 caractères max
                            ip += event.unicode

                # Réception des infos de clic sur les boutons de l'accueil
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if not host and not join:  # menu sans avoir cliquer
                        if posborderbtnHost.collidepoint(pos):
                            host = True
                        elif posborderbtnJoin.collidepoint(pos):  # si pos souris est sur le btn rejoindre
                            join = True
                    elif join and not online and not offline:
                        if posborderbtnOnline.collidepoint(pos):
                            online = True
                        elif posborderbtnOffline.collidepoint(pos):  # si pos souris est sur le btn offline
                            offline = True
                            ip = "0.0.0.0"
                            
            clock.tick(80)  # limite 80fps
            pygame.display.flip()  # Rafraichissement écran acceuil avec toutes nos modifs

        # Pas dans l'acceuil
        else:  
            if init:
                if host:
                    procClient = Process(target=client.client, args=("127.0.0.1", tunnelEnfant, pseudo))
                    procClient.start()  # Lancement du client
                    idJoueur = 0
                    while not start and not fini:
                        if tunnelParent.poll():  # Si tunnel pas vide
                            data = tunnelParent.recv().decode().split(",")
                            if data[0] == 'P':  # Si on recoit un pseudo
                                joueurs[idJoueur] = data[1]
                                if data[1] == pseudo:  # on recupère notre ID
                                    monID = idJoueur
                                idJoueur += 1
                            elif data[0] == 'F':
                                print("Déconnexion d'un joueur a fait planté")
                                fini = True
                        pos = pygame.mouse.get_pos()

                        # Affichage de l'interface d'attente
                        fenetre.fill((255, 255, 255))  # fond blanc
                        texteConn = police.render(str(len(joueurs)) + ' personnes connectés', True, (0, 0, 0))
                        fenetre.blit(texteConn, (0, 0))
                        fenetre.blit(play, posplay)

                        for event in pygame.event.get():
                            if event.type == MOUSEBUTTONDOWN and poscroix.collidepoint(pos):
                                if len(joueurs) >= 2:
                                    if procDiffu.is_alive():
                                        procDiffu.terminate()
                                        procDiffu.join()
                                    tableauJoueur = "T"
                                    idD = choice(list(joueurs.keys()))
                                    if idD == monID:
                                        etat = 'D'
                                    else:
                                        etat = 'L'
                                    for idTableauJoueur in joueurs:  # Envoi de tout les pseudos + Roles
                                        score[idTableauJoueur] = 0
                                        tableauJoueur = tableauJoueur + "," + str(idTableauJoueur) + ";" + joueurs[idTableauJoueur] + ";"
                                        if idTableauJoueur == idD:
                                            roles[idTableauJoueur] = 'D'
                                            tableauJoueur += 'D'
                                        else:
                                            roles[idTableauJoueur] = 'L'
                                            tableauJoueur += 'L'
                                    # "T,0;Michel;L,1;Marcel;D,2;Jean;L" == T,id;pseudo;role
                                    tunnelParent.send(tableauJoueur.encode())
                                    start = True
                                else:
                                    print('manque un client')
                            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                                tunnelParent.send('F'.encode())
                                fini = True
                        yMsg = 60
                        for idJoueurFor in joueurs:  # Affichage des pseudos connectés
                            txtJoueurs = police.render(joueurs[idJoueurFor] + ' est connecté', True, (0, 0, 0))
                            fenetre.blit(txtJoueurs, (60, yMsg))
                            yMsg += 60
                        pygame.display.flip()
                        clock.tick(20)
                    fenetre.fill((255, 255, 255))
                else:
                    procClient = Process(target=client.client, args=(ip, tunnelEnfant, pseudo))
                    procClient.start()
                    data = '0'
                    while not fini:  # attente de l'état
                        fenetre.fill((255, 255, 255))
                        if tunnelParent.poll():
                            data = tunnelParent.recv().decode().split(",")
                            if data[0] == 'T':  # On va décoder les infos des joueurs
                                data = data[1:]  # On enlève 'T'
                                for joueur in data:
                                    infos = joueur.split(";")  # 0;Marcel;L
                                    joueurs[int(infos[0])] = infos[1]
                                    roles[int(infos[0])] = infos[2]
                                    score[int(infos[0])] = 0
                                    if infos[1] == pseudo:
                                        monID = infos[0]
                                        etat = infos[2]
                                break
                            elif data[0] == 'F':
                                print("Déconnexion d'un joueur a fait planté")
                                fini = True
                        fenetre.blit(txtAttente, (500, 500))
                        for event in pygame.event.get():  # Pour pas que ca freeze durant le get
                            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                                tunnelParent.send('F'.encode())
                                fini = True
                        pygame.display.flip()
                init = False
                #----------------------------------------POUR CELUI QUI DESSINE------------------------------------------------------------------------------------------
            if etat == 'D':
                # Réception des données
                if tunnelParent.poll():
                    
                    # Séparation des données               
                    for raw_data in tunnelParent.recv().decode().split("@"):
                        data = raw_data.split(",")

                        # Si un joueur a quitté
                        if data[0] == 'F':
                            print(joueurs[int(data[1])] + " est parti")
                            del joueurs[int(data[1])]
                            del roles[int(data[1])]

                        # Si un joueur a envoyé un message
                        elif data[0] == 't':
                            listmsg.append(joueurs[int(data[1])] + " : " + data[2])  # On ajoute à la liste du chat le pseudo de l'envoyeur et son texte

                        # Si un joueur à trouvé le mot
                        elif data[0] == "O":
                            listmsg.append(joueurs[int(data[1])] + " a trouvé le mot")
                            trouves += 1
                            autrequitrouve_song.play(0 ,0 ,0)

                        elif data[0] == "P":
                            score[int(data[1])]+= int(data[2])
                            print(data[1], "marque", data[2], "pts")
                            print(score)
                        # Si un joueur a activé l'easter egg
                        elif data[0] == "V":
                            easter = 1

                #Récupération de la position de la souris
                px, py = pygame.mouse.get_pos()

                # Détection des évenements
                for e in pygame.event.get():
                    # Si on appuie sur ECHAP
                    if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):  
                        tunnelParent.send(("F," + str(monID) + '@').encode())  # On envoie l'info que l'on quitte le serveur
                        fini = True  # On ferme la fenêtre

                    # Si on fait un clique souris et que le mot a été choisi
                    elif e.type == pygame.MOUSEBUTTONDOWN and motChoisi:
                        pygame.draw.circle(fenetre, couleur, e.pos, rayon)      # On fait un cercle à la position du clic
                        dess = True

                    # Si on lache le bouton souris
                    elif e.type == pygame.MOUSEBUTTONUP:           
                        dess = False

                    #Si la souris bouge et que le clique est enfoncé
                    elif e.type == pygame.MOUSEMOTION:       
                        if dess:
                            pygame.display.update(pygame.draw.circle(fenetre, couleur, e.pos, rayon))      #On met à jour la fenêtre avec un nouveau cercle juste à coté de l'ancien
                            dessin(fenetre, couleur, e.pos, lastpos,  rayon)   #On active la fonction dessin
                            tunnelParent.send(('D,' + str(e.pos[0]) + ";" + str(e.pos[1]) + "," + str(lastpos[0]) + ";" + str(lastpos[1]) + "," + str(couleur[0]) + ";" + str(couleur[1]) + ";" + str(couleur[2]) + "," + str(rayon) + '@').encode())    #envoie des infos au serv
                        lastpos = e.pos  #On stocke l'ancienne position
                        
                # Afficahge de l'entête
                entete = pygame.draw.rect(fenetre, gris, (400, 0, 1920, 100))
                
                # Si l'easter egg n'est pas activé et ne l'a jamais été
                if easter != 1 or xE > 1520:
                    if idFrame < 20:
                        poslogo = logo1.get_rect(center=(int(largeur / 2), 50))
                        fenetre.blit(logo1, poslogo)
                    else:
                        poslogo = logo2.get_rect(center=(int(largeur / 2), 50))
                        fenetre.blit(logo2, poslogo)
                        
                # Si l'easter egg est activé        
                else:
                    fenetre.blit(imgpeu, (int(xE), yE))
                    xE += 3


                # Affichage de la pallete de couleur et de la sélection du rayon
                pygame.draw.rect(fenetre, blanc, (1820, 500, 100, 100))
                pygame.draw.rect(fenetre, blanc, (1720, 500, 100, 100))
                btr = pygame.draw.rect(fenetre, rouge, (1820, 100, 100, 100))
                btv = pygame.draw.rect(fenetre, vert, (1720, 100, 100, 100))
                btbl = pygame.draw.rect(fenetre, blanc, (1820, 200, 100, 100))
                btn = pygame.draw.rect(fenetre, noir, (1720, 200, 100, 100))
                btm = pygame.draw.rect(fenetre, marron, (1820, 300, 100, 100))
                btvi = pygame.draw.rect(fenetre, rose, (1720, 300, 100, 100))
                btj = pygame.draw.rect(fenetre, jaune, (1820, 400, 100, 100))
                btbc = pygame.draw.rect(fenetre, bleuc, (1720, 400, 100, 100))
                fenetre.blit(gomme1, (1830, 220))
                btcg = pygame.draw.circle(fenetre, noir, (1870, 550), 35)  # bouton circulaire gros rayon
                btcp = pygame.draw.circle(fenetre, noir, (1770, 550), 15)  # bouton circulaire petit rayon

                # Affichage des éléments de l'interface
                tab = pygame.draw.rect(fenetre, gris, (0, 0, 390, 1920))
                ligne = pygame.draw.rect(fenetre, noir, (390, 0, 10, 980))
                ligne2 = pygame.draw.rect(fenetre, noir, (0, 970, 1920, 10))
                bas = pygame.draw.rect(fenetre, gris, (0, 980, 1920, 1920))
                droite = pygame.draw.rect(fenetre, gris, (1720, 600, 200, 1000))
                ligne3 = pygame.draw.rect(fenetre, noir, (1720, 100, 1000, 5))
                ligne4 = pygame.draw.rect(fenetre, noir, (1720, 200, 1000, 5))
                ligne5 = pygame.draw.rect(fenetre, noir, (1720, 300, 1000, 5))
                ligne6 = pygame.draw.rect(fenetre, noir, (1720, 400, 1000, 5))
                ligne7 = pygame.draw.rect(fenetre, noir, (1720, 500, 1000, 5))
                ligne8 = pygame.draw.rect(fenetre, noir, (1720, 600, 1000, 5))
                ligne9 = pygame.draw.rect(fenetre, noir, (1720, 100, 10, 1000))
                ligne10 = pygame.draw.rect(fenetre, noir, (1820, 100, 5, 500))
                ligne11 = pygame.draw.rect(fenetre, noir, (1915, 100, 5, 500))
                souligne = pygame.draw.rect(fenetre, noir, (10, 50, 340, 5))
                ligne12 = pygame.draw.rect(fenetre, noir, (390, 100, 1920, 5))


                # Affichage du bouton tout effacer
                effac = pygame.draw.rect(fenetre, blanc, (1720, 10, 190, 80))
                txteffac = police2.render("Tout effacer", True, (0, 0, 0))
                fenetre.blit(txteffac, (1745, 40))
                
                # Si il ne reste qu'un joueur sur le serveur
                if len(joueurs) <= 1:
                    fini = True  # On ferme la fenêtre
                    break
                
                # Si le mot n'a pas été choisi
                if not motChoisi:

                    # Si trois mot n'ont pas été choisis au hasard
                    if selectionMot:  
                        mot1 = choice(limots)  # On choisi le premier mot
                        mot2 = choice(limots)  # On choisit le deuxième mot
                        mot3 = choice(limots)  # On chosit le troisième mot
                        selectionMot = False  # On ferme la boucle de la selection de mots
                        reini()  # On lance la fonction reini

                    # Affichage du filtre 
                    fenetre.blit(image, (0, 0))

                    # Initialisation des boutons
                    
                    #------------------------------------------------------Bouton mot 1-----------------------------------------------------#
                    btMot1 = police.render(mot1, True, (0, 0, 0))  # Rendu du texte avec (antialiasing, noir)
                    posbtMot1 = btMot1.get_rect(center=(int(largeur / 2), 410))
                    borderbtMot1 = pygame.Surface((posbtMot1[2] + 2 * padding, posbtMot1[3] + 2 * padding))
                    borderbtMot1.fill((0, 0, 0))
                    posborderbtMot1 = borderbtMot1.get_rect(center=(int(largeur / 2), 410))
                    paddingbtMot1 = pygame.Surface((posbtMot1[2] + padding, posbtMot1[3] + padding))
                    paddingbtMot1.fill((255,255,255))
                    paddingbtMot1Ombre = pygame.Surface((posbtMot1[2] + padding, posbtMot1[3] + padding))  # Pour le survol
                    paddingbtMot1Ombre.set_alpha(100)
                    paddingbtMot1Ombre.fill((0, 0, 0))
                    pospaddingbtMot1 = paddingbtMot1.get_rect(center=(int(largeur / 2), 410))

                    #------------------------------------------------------Bouton mot 2-----------------------------------------------------#
                    btMot2 = police.render(mot2, True, (0, 0, 0))  # Rendu du texte avec (antialiasing, noir)
                    posbtMot2 = btMot2.get_rect(center=(int(largeur / 2), 510))
                    borderbtMot2 = pygame.Surface((posbtMot2[2] + 2 * padding, posbtMot2[3] + 2 * padding))
                    borderbtMot2.fill((0, 0, 0))
                    posborderbtMot2 = borderbtMot2.get_rect(center=(int(largeur / 2), 510))
                    paddingbtMot2 = pygame.Surface((posbtMot2[2] + padding, posbtMot2[3] + padding))
                    paddingbtMot2.fill((255,255,255))
                    paddingbtMot2Ombre = pygame.Surface((posbtMot2[2] + padding, posbtMot2[3] + padding))  # Pour le survol
                    paddingbtMot2Ombre.set_alpha(100)
                    paddingbtMot2Ombre.fill((0, 0, 0))
                    pospaddingbtMot2 = paddingbtMot2.get_rect(center=(int(largeur / 2), 510))

                    #------------------------------------------------------Bouton mot 3-----------------------------------------------------#
                    btMot3 = police.render(mot3, True, (0, 0, 0))  # Rendu du texte avec (antialiasing, noir)
                    posbtMot3 = btMot3.get_rect(center=(int(largeur / 2), 610))
                    borderbtMot3 = pygame.Surface((posbtMot3[2] + 2 * padding, posbtMot3[3] + 2 * padding))
                    borderbtMot3.fill((0, 0, 0))
                    posborderbtMot3 = borderbtMot3.get_rect(center=(int(largeur / 2), 610))
                    paddingbtMot3 = pygame.Surface((posbtMot3[2] + padding, posbtMot3[3] + padding))
                    paddingbtMot3.fill((255,255,255))
                    paddingbtMot3Ombre = pygame.Surface((posbtMot3[2] + padding, posbtMot3[3] + padding))  # Pour le survol
                    paddingbtMot3Ombre.set_alpha(100)
                    paddingbtMot3Ombre.fill((0, 0, 0))
                    pospaddingbtMot3 = paddingbtMot3.get_rect(center=(int(largeur / 2), 610))

                    # Affichage du bouton mot 1
                    fenetre.blit(borderbtMot1, posborderbtMot1)
                    fenetre.blit(paddingbtMot1, pospaddingbtMot1)
                    fenetre.blit(btMot1, posbtMot1)

                    # Lorsqu'on clique sur le mot, le mot est choisi et on active la boucle motChoisi
                    if posborderbtMot1.collidepoint(px,py):
                        fenetre.blit(paddingbtMot1Ombre, pospaddingbtMot1)
                        fenetre.blit(btMot1, posbtMot1)
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            motChoisi=True
                            motdevin=mot1
                            
                    # Affichage du bouton mot 2
                    fenetre.blit(borderbtMot2, posborderbtMot2)
                    fenetre.blit(paddingbtMot2, pospaddingbtMot2)
                    fenetre.blit(btMot2, posbtMot2)

                    # Lorsqu'on clique sur le mot, le mot est choisi et on active la boucle motChoisi
                    if posborderbtMot2.collidepoint(px,py):
                        fenetre.blit(paddingbtMot2Ombre, pospaddingbtMot2)
                        fenetre.blit(btMot2, posbtMot2)
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            motChoisi=True
                            motdevin=mot2
                            
                    # Affichage su bouton mot 3
                    fenetre.blit(borderbtMot3, posborderbtMot3)
                    fenetre.blit(paddingbtMot3, pospaddingbtMot3)
                    fenetre.blit(btMot3, posbtMot3)

                    # Lorsqu'on clique sur le mot, le mot est choisi et on active la boucle motChoisi
                    if posborderbtMot3.collidepoint(px,py):
                        fenetre.blit(paddingbtMot3Ombre, pospaddingbtMot3)
                        fenetre.blit(btMot3, posbtMot3)
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            motChoisi=True
                            motdevin=mot3
                            
                    # Lorsque le mot a été choisi
                    if motChoisi:
                        tunnelParent.send(("M" + "," + motdevin + '@').encode())  # On envoie le mot aux autres joueurs
                        pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))   # On efface la fenêtre
                        tempsFin = time() + temps   # On lance le timer
                        
                else:
                    # Affichage du timer 
                    affChrono = police.render(str(int(tempsFin - time())), True, (0, 0, 0))
                    fenetre.blit(affChrono, (1810, 610))

                    # Lorsque le temps arrive à 10
                    if int(tempsFin - time()) <= 10:
                        minuteur_song.play(0 ,10000 ,2000)



                    # Lorsque le temps arrive à 0 
                    if trouves >= len(joueurs)-1 or int(tempsFin - time()) <= 0:
                        idD = int(monID)
                        while int(idD) == int(monID):
                            idD = choice(list(joueurs.keys()))

                        # On change le rôle des joueurs
                        for j in joueurs:
                            if j == idD:
                                roles[j] = "D"
                            else:
                                roles[j] = "L"

                        # On réinitialise les variables        
                        etat = "L"
                        trouves = 0
                        motdevin = "mot pas choisi"
                        motcache = "mot pas choisi"
                        verif = False
                        pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
                        tunnelParent.send(("R," + str(idD) + '@').encode())  #On envoie le mot qui devait être deviné aux autres joueurs

                # On affiche le rayon et la couleur sélectionée à celui qui dessine                        
                affrayon = police.render('rayon : '+ str(rayon), True, (0, 0, 0))
                fenetre.blit(affrayon, (600, 1000))
                affCouleur = police.render(txtCouleur, True, couleur)
                fenetre.blit(affCouleur, (900, 1000))

                # Détection du moment quand la souris passe sur les boutons
                if btj.collidepoint(px, py):
                    selection(btj, jaune, 'jaune')
                if btr.collidepoint(px, py):
                    selection(btr, rouge, 'rouge')
                if btv.collidepoint(px, py):
                    selection(btv, vert, 'vert')
                if btbl.collidepoint(px, py):
                    selection(btbl, blanc, 'gomme')
                if btn.collidepoint(px, py):
                    selection(btn, noir, 'noir')
                if btm.collidepoint(px, py):
                    selection(btm, marron, 'marron')
                if btvi.collidepoint(px, py):
                    selection(btvi, rose, 'rose')
                if btbc.collidepoint(px, py):
                    selection(btbc, bleuc, 'bleu clair')
                if btcg.collidepoint(px, py):
                    selectioncercle1()
                if btcp.collidepoint(px, py):
                    selectioncercle2()
                if effac.collidepoint(px, py):
                    effacfx()
                    
                # On affiche le mot qu'il faut faire deviner
                affmotdevin = police.render(motdevin, True, (0, 0, 0))
                fenetre.blit(affmotdevin, (1400, 1000))

                # Affichage du chat
                i = 0
                for i in range(10):
                    listmsg = listmsg[-10:]
                    textchat = police2.render(listmsg[i], True, (0, 0, 0))
                    fenetre.blit(textchat, (50, 480 + 50 * i))
                    
                # Affichage des joueurs en ligne et leurs rôles
                textJoueur = police.render('Joueurs en ligne : ', True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textJoueur, (10, 0))
                xJoueur = 0
                for j in joueurs:
                    nomJoueur = police.render(joueurs[j] + " : " + str(score[j]), True, (0, 0, 0))
                    fenetre.blit(nomJoueur, (10, 60 + xJoueur * 50))
                    if roles[j] == "D":
                        fenetre.blit(pinceau, (340, 60 + xJoueur * 50))
                    xJoueur += 1
                    
                # Animation du logo super-Sketch
                idFrame = (idFrame + 2) % 40  
                if idFrame < 20:
                    poslogo = logo1.get_rect(center=(int(largeur / 2), 50))
                    fenetre.blit(logo1, poslogo)
                else:
                    poslogo = logo2.get_rect(center=(int(largeur / 2), 50))
                    fenetre.blit(logo2, poslogo)

                # Rafraichissement de la fenêtre
                pygame.display.flip()
                clock.tick(40)
                # ------------------------------------------------QUAND ON REGARDE LE DESSIN-----------------------------------------------------------------------------
            elif etat == 'L':
                # On reçoit les données
                if tunnelParent.poll():
                    # On trie les données
                    for raw_data in tunnelParent.recv().decode().split("@"):
                        data = raw_data.split(",")

                        # Si c'est un dessin, on décode les infos
                        if data[0] == 'D':
                            pos = data[1].split(";")
                            pos = tuple(map(int, pos))
                            last = data[2].split(";")
                            last = tuple(map(int, last))
                            couleur = data[3].split(";")
                            couleur = tuple(map(int, couleur))
                            rayon = int(data[4])
                            pygame.display.update(pygame.draw.circle(fenetre, couleur, pos, rayon))
                            dessin(fenetre, couleur, pos, last,  rayon)

                        # Si un joueur est parti    
                        elif data[0] == 'F':
                            print(joueurs[int(data[1])] + " est parti")
                            del joueurs[int(data[1])]  # On supprime le joueur
                            del roles[int(data[1])]

                        # Si on reçoit un message
                        elif data[0] == 't':
                            listmsg.append(joueurs[int(data[1])] + " : " + data[2])

                        # Si on reçoit cette valeur c'est que le dessinateur a tout effacé
                        elif data[0] == "E":
                            pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))

                        # Si on reçoit le mot qu'il faut faire deviner
                        elif data[0] == "M":
                            motdevin = data[1]
                            tempsFin = time() + temps   # On lance le timer
                            debutround_song.play(0 ,0 ,0)

                        #2éme son
                        # Si un joueur a trouvé le mot
                        elif data[0] == "O":
                            listmsg.append(joueurs[int(data[1])] + " a trouvé le mot")
                            autrequitrouve_song.play(0 ,0 ,0)  
                            
                        # Si une personne n'a pas trouvé le mot à la fin du timer
                        elif data[0] == "R":
                            listmsg.append("C'était " + motdevin)
                            
                            # On change les rôles
                            for j in joueurs:
                                if j == int(data[1]):
                                    roles[j] = "D"
                                else:
                                    roles[j] = "L"
                            if int(data[1]) == int(monID):
                                etat = "D"

                            # On réinitialise les variables
                            trouves = 0
                            motChoisi = False
                            selectionMot = True
                            motdevin = "mot pas choisi"
                            motcache = "mot pas choisi"
                            verif = False
                            pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))

                        elif data[0] == "P":
                            score[int(data[1])] += int(data[2])
                            print(data[1], "marque", data[2], "pts")
                            print(score)
        
                        # Si un joueur a activé l'easter egg
                        elif data[0] == "V":
                            easter = 1
                            
                # Si le mot n'a pas été trouvé ou qu'il a été choisi
                if not verif and motdevin != "mot pas choisi":  
                    motcache = ['_'] * len(motdevin)
                    motcache = str(' '.join(motcache))
                    affmotcache = police.render(motcache, True, (0, 0, 0))

                # Si le mot n'a pas été choisi
                elif motdevin == "mot pas choisi":
                    motcache = motdevin
                    affmotcache = police.render(motcache, True, (0, 0, 0))
                    
                # On détecte les actions
                for event in pygame.event.get():
                    
                    # Si on appuie sur ECHAP
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  
                        tunnelParent.send(("F," + str(monID) + '@').encode())  # On envoie F pour signaler que le joueur est parti au serveur
                        fini = True  # On ferme la fenêtre
                        
                    if event.type == pygame.KEYDOWN:
                        # Si on appuie sur entrée et que le mot n'est pas vide
                        if event.key == pygame.K_RETURN and motEcrit != '':

                            # Si le mot écrit est celui qu'il fallait deviner et que celui n'a pas déjà été trouvé
                            if motEcrit == motdevin and not verif:
                                motcache = motdevin  # On affiche le mot qui devait être deviné au joueur qui l'a trouvé
                                affmotcache = police.render(motcache, True, (0, 0, 0))
                                point = int(tempsFin - time())
                                score[int(monID)] += point 
                                listmsg.append("Vous avez trouvé le mot!")
                                tunnelParent.send(("O," + str(monID) + '@').encode())  # On envoie au serveur son pseudo en disant qu'on a trouvé le mot
                                tunnelParent.send(("P," + str(monID) + "," + str(point) + '@').encode())
                                verif = True    # Le mot est trouvé
                                print(score)
                                playerguessed_song.play(0 ,0 ,0)

                            # Si on active l'easter egg   
                            elif motEcrit == "406SW":
                                easter = 1
                                tunnelParent.send("V@".encode())

                            # Quand le mot et faux
                            else:
                                listmsg.append(joueurs[int(monID)] + " : " + motEcrit)  # On ajoute le mot à la liste du chat
                                tunnelParent.send(("t," + str(monID) + "," + motEcrit + '@').encode())  # On envoie le message avec le pseudo au serveur
                                erreur_song.play(0 ,0 ,0)
                            motEcrit = ''  # On réinitialise le mot

                        elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                            motEcrit = motEcrit[:-1]  # du 1er caractère inclus jusqu'au dernier exclu

                        elif len(motEcrit) < 16 and motdevin != "mot pas choisi":  # 16 caractères max
                            motEcrit = motEcrit + event.unicode
                            
                # Affichage de l'entête
                entete = pygame.draw.rect(fenetre, gris, (400, 0, 1920, 100))  # Fond gris de le zone de l'entête

                # Si l'easter egg n'est pas activé et ne l'a jamais été on affiche le logo
                if easter != 1 or xE > 1520:
        
                    if idFrame < 20:
                        poslogo = logo1.get_rect(center=(int(largeur / 2), 50))
                        fenetre.blit(logo1, poslogo)
                    else:
                        poslogo = logo2.get_rect(center=(int(largeur / 2), 50))
                        fenetre.blit(logo2, poslogo)

                # Si l'easter egg a été activé
                else:
                    xE += 3
                    fenetre.blit(imgpeu, (int(xE), yE))
                    
                # Affichage des éléments de l'interface
                fonpal = pygame.draw.rect(fenetre, blanc, (1720, 100, 200, 980))  # Fond de la palette de couleur
                tab = pygame.draw.rect(fenetre, gris, (0, 0, 390, 1920))  # Fond gris de le zone de chat
                ligne = pygame.draw.rect(fenetre, noir, (390, 0, 10, 980))  # Dessin des lignes de la palette
                ligne2 = pygame.draw.rect(fenetre, noir, (0, 970, 1920, 10))
                bas = pygame.draw.rect(fenetre, gris, (0, 980, 1920, 1920))  # Fond gris de le zone de texte
                souligne = pygame.draw.rect(fenetre, noir, (10, 50, 340, 5))
                ligne12 = pygame.draw.rect(fenetre, noir, (390, 100, 1920, 5))
                effac = pygame.draw.rect(fenetre, gris, (1720, 10, 190, 80))
                fenetre.blit(affmotcache, (1400, 1000))
                
                # Si le mot a été choisi
                if motdevin != "mot pas choisi":
                    affChrono = police.render(str(int(tempsFin - time())), True, (0, 0, 0))
                    fenetre.blit(affChrono, (1810, 610))

                # Animation de la barre de saisie
                idFrame = (idFrame + 0.1) % 40  
                if idFrame < 20:
                    barre = '|'
                else:
                    barre = ''

                # Si il n'y a qu'un joueur sur le serveur
                if len(joueurs) <= 1:
                    fini = True  # On ferme la fenêtre
                    break

                # Affichage de mot écrit
                textMotEcrit = police.render('Ecrivez un mot : ' + motEcrit + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textMotEcrit, (50, 1000))
                textJoueur = police.render('Joueurs en ligne : ', True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textJoueur, (10, 0))

                # Affichage des joueurs et de leurs rôles
                xJoueur = 0
                for j in joueurs:
                    nomJoueur = police.render(joueurs[j] + " : " + str(score[j]), True, (0, 0, 0))
                    fenetre.blit(nomJoueur, (10, 60 + xJoueur*50))
                    if roles[j] == "D":
                        fenetre.blit(pinceau, (340, 60 + xJoueur * 50))
                    xJoueur += 1
                    
                # Affichage du texte dans le chat
                for i in range(10):  
                    listmsg = listmsg[-10:]  # On garde uniquement les 10 derniers termes de la listes
                    textchat = police2.render(listmsg[i], True, (0, 0, 0))
                    fenetre.blit(textchat, (50, 480 + 50 * i))  # On affiche la liste avec les coord saisie précédemment
                    
                # Raffraichissment de la fenêtre
                pygame.display.flip()  
                clock.tick(200)
    pygame.quit()
    if procClient.is_alive():
        procClient.join()
    if procServeur.is_alive():
        procServeur.terminate()  # ferme le serveur
        procServeur.join()
