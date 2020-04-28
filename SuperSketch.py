import pygame
from pygame.locals import *
from random import *
import ctypes
from multiprocessing import Process, Pipe
from time import *
# Nos Fichiers
import serveur
import client

# FAUT FERMER AVEC ECHAP ET PROPREMENT
if __name__ == '__main__':  # Si c'est le programme pricipal / obligatoire pour multiprocessing
    # Etat du menu
    fini = False
    acceuil = True
    host = False
    join = False
    online = False
    offline = False
    accip = True

    # Style fenetre
    bgColor = (118, 188, 194)

    pygame.init()

    # caractéristiques de l'écran
    ctypes.windll.user32.SetProcessDPIAware()
    largeur = ctypes.windll.user32.GetSystemMetrics(0)
    hauteur = ctypes.windll.user32.GetSystemMetrics(1)
    fenetre = pygame.display.set_mode((largeur, hauteur), pygame.FULLSCREEN)

    pygame.display.set_caption("Super-sketch")
    fenetre.fill(bgColor)

    # initialisation cadence
    clock = pygame.time.Clock()
    idFrame = 0

    # INITIALISATION :
    # - Partie accueil

    # chargement du logo au centre de l'écran
    logo1 = pygame.image.load("img/lobby/logo1.png")
    logo2 = pygame.image.load("img/lobby/logo2.png")
    poslogo = logo1.get_rect(center=(int(largeur / 2), 100))
    fenetre.blit(logo1, poslogo)

    nuage = pygame.image.load("img/lobby/nuage.png")
    # info position nuage Gauche
    xNuageG = randint(-600, 1500)
    vxNuageG = random() / 3 + .15
    yNuageG = randint(0, 250)
    # info nuage Droite
    xNuageD = randint(400, 2000)
    vxNuageD = -(random() / 3 + .15)
    yNuageD = randint(0, 250)

    soleil = pygame.image.load("img/lobby/soleil.png")
    fenetre.blit(soleil, (1645, 22))

    croix = pygame.image.load("img/lobby/croix.png")
    poscroix = croix.get_rect(topright=(largeur - 15, 15))
    fenetre.blit(croix, poscroix)

    padding = 10  # espace autour du texte des btn
    police = pygame.font.SysFont("roboto-bold", 65)

    # Pour positionner mes bouttons j'ai recupéré les rectangles de mes objets Surface(des objets qu'on peut blit contenant
    # les pixels a afficher)
    #
    # Surface.get_rect() retourne un Rect(x=0, y=0, largeur, hauteur) sans couleur, qui recouvre toute la Surface de l'image
    #
    # Surface.get_rect(center=(X, Y)) retourne un Rect(x, y, largeur, hauteur). On donne centre du Rect == X, Y; la méthode
    # retourne x et y correspondant
    #
    # On pourras ensuite utiliser fenetre.blit(btnA, posbtnA) qui placera la Surface(btnA) aux coordonnés de Rect(posbtnA)

    # --- Boutton héberger --- #
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

    # --- Boutton rejoindre --- #
    btnJoin = police.render('Rejoindre Une Partie', True, (0, 0, 0))
    # Trouve le rectangle de la surface
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

    # --- Boutton IP manuelle --- #
    btnOnline = police.render('Entrer une IP', True, (0, 0, 0))
    posbtnOnline = btnOnline.get_rect(center=(int(largeur / 2), 510))

    # Rectangle noir plus grand qui sert de bordure
    borderbtnOnline = pygame.Surface((posbtnOnline[2] + 2 * padding, posbtnOnline[3] + 2 * padding))
    borderbtnOnline.fill((0, 0, 0))
    # Trouve le rectangle de la surface (x=0, y=0, largeur, hauteur) pour le plaçage au centre
    posborderbtnOnline = borderbtnOnline.get_rect(center=(int(largeur / 2), 510))

    # Rectangle bleu plus petit
    paddingbtnOnline = pygame.Surface((posbtnOnline[2] + padding, posbtnOnline[3] + padding))
    paddingbtnOnline.fill(bgColor)
    paddingbtnOnlineOmbre = pygame.Surface((posbtnOnline[2] + padding, posbtnOnline[3] + padding))  # Pour le survol
    paddingbtnOnlineOmbre.set_alpha(100)
    paddingbtnOnlineOmbre.fill((0, 0, 0))

    # Trouve le rectangle de la surface (x=0, y=0, largeur, hauteur) pour le plaçage au centre
    pospaddingbtnOnline = paddingbtnOnline.get_rect(center=(int(largeur / 2), 510))

    # --- Boutton LAN Automatique --- #
    btnOffline = police.render('LAN Automatique', True, (0, 0, 0))
    posbtnOffline = btnOffline.get_rect(center=(int(largeur / 2), 680))

    # Rectangle noir plus grand qui sert de bordure
    borderbtnOffline = pygame.Surface((posbtnOffline[2] + 2 * padding, posbtnOffline[3] + 2 * padding))
    borderbtnOffline.fill((0, 0, 0))
    # Trouve le rectangle de la surface (x=0, y=0, largeur, hauteur) pour le plaçage au centre
    posborderbtnOffline = borderbtnOffline.get_rect(center=(int(largeur / 2), 680))

    # Rectangle bleu plus petit
    paddingbtnOffline = pygame.Surface((posbtnOffline[2] + padding, posbtnOffline[3] + padding))
    paddingbtnOffline.fill(bgColor)
    paddingbtnOfflineOmbre = pygame.Surface((posbtnOffline[2] + padding, posbtnOffline[3] + padding))  # Pour le survol
    paddingbtnOfflineOmbre.set_alpha(100)
    paddingbtnOfflineOmbre.fill((0, 0, 0))

    # Trouve le rectangle de la surface (x=0, y=0, largeur, hauteur) pour le plaçage au centre
    pospaddingbtnOffline = paddingbtnOffline.get_rect(center=(int(largeur / 2), 680))

    textPseudo = police.render('Entrez votre pseudo : ', True, (0, 0, 0))  # Rendu du texte avec (texte, antialiasing, noir)
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
    trouves = 0
    etat = 0

    play = pygame.image.load("img/lobby/play.png")
    posplay = play.get_rect(topright=(largeur - 15, 15))
    txtAttente = police.render("En attente de l'hote", True, (0, 0, 0))

    px = 5000
    py = 5000

    # Déclaration de la fonction de sélection de la couleur
    def selection(pbt, cbt):
        global couleur  # Définition de variable globale du programme
        global idFrame2  # Animation de l'image
        idFrame2 = (idFrame2 + 1) % 40
        if idFrame2 < 30:
            fenetre.blit(pal1, pbt)
        else:
            fenetre.blit(pal2, pbt)
        if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de couleur lors d'un clic gauche
            couleur = cbt
        return

    #---------Cette fonction permet un dessin beaucoup plus fluide que l'ancien algorithme, il calcule les positions intermiédiares entre deux positions détectée
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
        couleur = noir
        rayon = 10
        pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))

    pygame.draw.rect(fenetre, (255, 255, 255), (0, 0, 1920, 1080))

    # Initialisation des variables de couleur et des animations
    pal1 = pygame.pal1 = pygame.image.load("img/pal1.png").convert_alpha()
    pal2 = pygame.image.load("img/pal2.png").convert_alpha()
    fon = pygame.image.load("img/pal4.png").convert_alpha()
    imgpeu = pygame.image.load("img/406sw.png").convert_alpha()
    image =pygame.image.load("img/ima.png").convert_alpha()
    rouge = (255, 0, 0)
    vert = (0, 255, 0)
    jaune = (255, 215, 0)
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    bleuc = (38, 188, 254)
    violet = (238, 130, 238)
    marron = (88, 41, 0)
    gris = (192, 192, 192)
    police2 = pygame.font.SysFont("roboto-bold", 35)
    motEcrit = ''
    listmsg = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']  # Initialisation de la liste du chat vide
    couleur = noir
    rayon = 10
    ancienpx = 2500  # hors écran
    ancienpy = 2500
    gomme1 = pygame.image.load("img/gomme1.png").convert_alpha()
    limots = [word.strip() for word in open("dico.txt", encoding="utf-8")]  # On créer une liste à partir d'un document texte
    motChoisi = False
    selectionMot = True
    motdevin = "mot pas choisi"
    motcache = "mot pas choisi"
    mot1 = mot2 = mot3 = affmot1 = affmot2 = affmot3 = affmotcache = ""
    tempsFin = 0
    temps = 80  # temps pour dessiner
    verif = False
    idFrame2 = 0
    easter = 0
    xE = 400
    yE = 0
    draw_on = False
    lastpos = (0, 0)

    while not fini:  # Boucle tant que le joueur reste dans le menu
        if acceuil:
                
            fenetre.fill(bgColor)  # Retour à zéro

            pos = pygame.mouse.get_pos()

            fenetre.blit(soleil, (1645, 22))

            xNuageG += vxNuageG  # On ajoute la vitesse a la pos du nuage
            if xNuageG > 1930:  # Si sort de l'écran
                xNuageG = randint(-600, -300)  # Retourne au départ
            fenetre.blit(nuage, (int(xNuageG), yNuageG))

            xNuageD += vxNuageD  # On ajoute la vitesse a la pos du nuage
            if xNuageD < -200:  # Si sort de l'écran
                xNuageD = randint(1930, 2100)  # Retourne au départ
            fenetre.blit(nuage, (int(xNuageD), yNuageD))

            fenetre.blit(croix, poscroix)

            idFrame = (idFrame + 1) % 40  # logo qui bouge tout les 1/4s ou 20images car 80fps
            if idFrame < 20:
                fenetre.blit(logo1, poslogo)
            else:
                fenetre.blit(logo2, poslogo)

            if idFrame < 24:  # barre qui clignotte du pseudo
                barre = '|'
            else:
                barre = ''

            if not host and not join:  # menu sans avoir cliquer
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

            if host:  # Si on héberge
                textPseudo = police.render('Entrez votre pseudo : ' + pseudo + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textPseudo, (400, 530))

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

            if offline:
                textPseudo = police.render('Entrez votre pseudo : ' + pseudo + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textPseudo, (400, 530))

            if online:
                if accip:
                    textIP = police.render("Entrez l'addresse IP du serveur : " + ip + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                    fenetre.blit(textIP, (400, 530))
                else:
                    textPseudo = police.render('Entrez votre pseudo : ' + pseudo + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                    fenetre.blit(textPseudo, (400, 530))

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == MOUSEBUTTONDOWN and poscroix.collidepoint(pos)):
                    acceuil = False
                    fini = True
                if event.type == pygame.KEYDOWN:
                    if host or (join and (offline or (online and not accip))):  # Si une touche est pressée
                        if event.key == pygame.K_RETURN:  # si entrer
                            if host:
                                procDiffu = Process(target=serveur.diffuIpHote)
                                procDiffu.daemon = True
                                procDiffu.start()  # Lancement du processus de la diffusion de l'ip
                                procServeur = Process(target=serveur.serveur)
                                procServeur.start()  # lancement du serveur dans un processus parallèle
                            acceuil = False  # fin de l'acceuil
                        elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                            pseudo = pseudo[:-1]  # du 1er caractère inclus jusqu'au dernier exclu
                        elif len(pseudo) < 16:  # 16 caractères max
                            pseudo += event.unicode
                    elif online and accip:
                        if event.key == pygame.K_RETURN and ip != '':
                            accip = False
                        elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                            ip = ip[:-1]  # du 1er caractère inclus jusqu'au dernier exclu
                        elif len(pseudo) < 16:  # 16 caractères max
                            ip += event.unicode
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
        else:  # pas dans l'acceuil
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
                #----------------
            if etat == 'D':  # Si on dessine
                if tunnelParent.poll():  # On get les nouveaux points
                    for raw_data in tunnelParent.recv().decode().split("@"):
                        data = raw_data.split(",")
                        if data[0] == 'F':
                            print(joueurs[int(data[1])] + " est parti")
                            del joueurs[int(data[1])]
                            del roles[int(data[1])]
                        elif data[0] == 't':
                            listmsg.append(joueurs[int(data[1])] + " : " + data[2])  # On ajoute à la liste du chat le pseudo de l'envoyeur et son texte
                        elif data[0] == "O":
                            listmsg.append(joueurs[int(data[1])] + " a trouvé le mot")
                            trouves += 1
                        elif data[0] == "V":
                            easter = 1

               
                px, py = pygame.mouse.get_pos()
                for e in pygame.event.get():
                    if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):  # Si on appuie sur ECHAP
                        tunnelParent.send(("F," + str(monID) + '@').encode())  # On envoie l'info que l'on quitte le serveur
                        fini = True  # On ferme la fenêtre

                    elif e.type == pygame.MOUSEBUTTONDOWN and motChoisi:
                        pygame.draw.circle(fenetre, couleur, e.pos, rayon)      #Si on clique, on fait un cercle à la position du clic
                        draw_on = True
                    elif e.type == pygame.MOUSEBUTTONUP:           #Si on lache, on désactive la boucle suivante
                        draw_on = False
                    elif e.type == pygame.MOUSEMOTION:       #Si la souris bouge et que le clique est enfoncé
                        if draw_on:
                            pygame.display.update(pygame.draw.circle(fenetre, couleur, e.pos, rayon))      #On met à jour la fenêtre avec un nouveau cercle juste à coté de l'ancien
                            dessin(fenetre, couleur, e.pos, lastpos,  rayon)   #On active la fonction dessin
                            tunnelParent.send(('D,' + str(e.pos[0]) + ";" + str(e.pos[1]) + "," + str(lastpos[0]) + ";" + str(lastpos[1]) + "," + str(couleur[0]) + ";" + str(couleur[1]) + ";" + str(couleur[2]) + "," + str(rayon) + '@').encode())    #envoie des infos au serv
                        lastpos = e.pos  #On stocke l'ancienne position

                entete = pygame.draw.rect(fenetre, gris, (400, 0, 1920, 100))

                if easter != 1 or xE > 1520:
                    if idFrame < 20:
                        poslogo = logo1.get_rect(center=(int(largeur / 2), 50))
                        fenetre.blit(logo1, poslogo)
                    else:
                        poslogo = logo2.get_rect(center=(int(largeur / 2), 50))
                        fenetre.blit(logo2, poslogo)
                else:
                    fenetre.blit(imgpeu, (int(xE), yE))
                    xE += 3

                # Placement des boutons sur l'écran
                fenetre.blit(fon, (1820, 500))
                fenetre.blit(fon, (1720, 500))
                fonpal = pygame.draw.rect(fenetre, blanc, (1720, 100, 200, 980))     #Affichage des boutons de couleurs
                btr = pygame.draw.rect(fenetre, rouge, (1820, 100, 100, 100))
                btv = pygame.draw.rect(fenetre, vert, (1720, 100, 100, 100))
                btbl = pygame.draw.rect(fenetre, blanc, (1820, 200, 100, 100))
                btn = pygame.draw.rect(fenetre, noir, (1720, 200, 100, 100))
                btm = pygame.draw.rect(fenetre, marron, (1820, 300, 100, 100))
                btvi = pygame.draw.rect(fenetre, violet, (1720, 300, 100, 100))
                btj = pygame.draw.rect(fenetre, jaune, (1820, 400, 100, 100))
                btbc = pygame.draw.rect(fenetre, bleuc, (1720, 400, 100, 100))
                btcg = pygame.draw.circle(fenetre, noir, (1870, 550), 35)  # bouton circulaire gros rayon
                btcp = pygame.draw.circle(fenetre, noir, (1770, 550), 15)  # bouton circulaire petit rayon
                tab = pygame.draw.rect(fenetre, gris, (0, 0, 390, 1920))     #Affichage des élément de l'interface
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
                fenetre.blit(gomme1, (1830, 220))
                effac = pygame.draw.rect(fenetre, blanc, (1720, 10, 190, 80))  # Création du bouton pour tout effacer
                txteffac = police2.render("Tout effacer", True, (0, 0, 0))
                fenetre.blit(txteffac, (1745, 40))

                if len(joueurs) <= 1:
                    fini = True  # On ferme la fenêtre
                    break

                if not motChoisi:  # Si le mot n'est pas chosi
                    if selectionMot:  # Si trois mot n'ont pas été choisis au hasard
                        mot1 = choice(limots)  # On choisi le premier mot
                        mot2 = choice(limots)  # On choisit le deuxième mot
                        mot3 = choice(limots)  # On chosit le troisième mot
                        selectionMot = False  # On ferme la boucle de la selection de mots

                    fenetre.blit(image, (0, 0))
                    #----Bouton mot 1----#
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

                    #----Bouton mot 2----#
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

                    #----Bouton mot 3----#
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

                    fenetre.blit(borderbtMot1, posborderbtMot1)
                    fenetre.blit(paddingbtMot1, pospaddingbtMot1)
                    fenetre.blit(btMot1, posbtMot1)
                    if posborderbtMot1.collidepoint(px,py):
                        fenetre.blit(paddingbtMot1Ombre, pospaddingbtMot1)
                        fenetre.blit(btMot1, posbtMot1)
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            motChoisi=True
                            motdevin=mot1
                            reini()
        
                    fenetre.blit(borderbtMot2, posborderbtMot2)
                    fenetre.blit(paddingbtMot2, pospaddingbtMot2)
                    fenetre.blit(btMot2, posbtMot2)
                    if posborderbtMot2.collidepoint(px,py):
                        fenetre.blit(paddingbtMot2Ombre, pospaddingbtMot2)
                        fenetre.blit(btMot2, posbtMot2)
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            motChoisi=True
                            motdevin=mot2
                            reini()

                    fenetre.blit(borderbtMot3, posborderbtMot3)
                    fenetre.blit(paddingbtMot3, pospaddingbtMot3)
                    fenetre.blit(btMot3, posbtMot3)
                    if posborderbtMot3.collidepoint(px,py):
                        fenetre.blit(paddingbtMot3Ombre, pospaddingbtMot3)
                        fenetre.blit(btMot3, posbtMot3)
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            motChoisi=True
                            motdevin=mot3
                            reini()

                    if motChoisi:
                        tunnelParent.send(("M" + "," + motdevin + '@').encode())  # On envoie le mot aux autres
                        pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
                        tempsFin = time() + temps
                else:
                    affChrono = police.render(str(int(tempsFin - time())), True, (0, 0, 0))
                    fenetre.blit(affChrono, (1810, 610))
                    if trouves >= len(joueurs)-1 or int(tempsFin - time()) <= 0:
                        idD = int(monID)
                        while int(idD) == int(monID):
                            idD = choice(list(joueurs.keys()))
                        for j in joueurs:
                            if j == idD:
                                roles[j] = "D"
                            else:
                                roles[j] = "L"
                        etat = "L"
                        trouves = 0
                        motdevin = "mot pas choisi"
                        motcache = "mot pas choisi"
                        verif = False
                        pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
                        tunnelParent.send(("R," + str(idD) + '@').encode())

                # Détection du moment quand la souris passe sur les boutons
                if btj.collidepoint(px, py):
                    selection(btj, jaune)
                if btr.collidepoint(px, py):
                    selection(btr, rouge)
                if btv.collidepoint(px, py):
                    selection(btv, vert)
                if btbl.collidepoint(px, py):
                    selection(btbl, blanc)
                if btn.collidepoint(px, py):
                    selection(btn, noir)
                if btm.collidepoint(px, py):
                    selection(btm, marron)
                if btvi.collidepoint(px, py):
                    selection(btvi, violet)
                if btbc.collidepoint(px, py):
                    selection(btbc, bleuc)
                if btcg.collidepoint(px, py):
                    selectioncercle1()
                if btcp.collidepoint(px, py):
                    selectioncercle2()
                if effac.collidepoint(px, py):
                    effacfx()

                affmotdevin = police.render(motdevin, True, (0, 0, 0))
                fenetre.blit(affmotdevin, (1400, 1000))  # on affiche le mot à faire deviner

                i = 0
                for i in range(10):  # Affichage du chat
                    listmsg = listmsg[-10:]
                    textchat = police2.render(listmsg[i], True, (0, 0, 0))
                    fenetre.blit(textchat, (50, 480 + 50 * i))

                textJoueur = police.render('Joueurs en ligne : ', True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textJoueur, (10, 0))
                xJoueur = 0
                for j in joueurs:
                    nomJoueur = police.render(joueurs[j] + " : " + roles[j], True, (0, 0, 0))
                    fenetre.blit(nomJoueur, (10, 60 + xJoueur * 50))
                    xJoueur += 1

                idFrame = (idFrame + 2) % 40  # Animation du logo super-Sketch
                if idFrame < 20:
                    poslogo = logo1.get_rect(center=(int(largeur / 2), 50))
                    fenetre.blit(logo1, poslogo)
                else:
                    poslogo = logo2.get_rect(center=(int(largeur / 2), 50))
                    fenetre.blit(logo2, poslogo)

                # Détection clique gauche pour effectuer le dessin
                
                      # On envoie toutes les données au serveur
                    # "D,875,745,45;75;0,10"
                    ancienpx = px
                    ancienpy = py
                pygame.display.flip()  # Rafraichissement de la fenêtre
                clock.tick(40)
                # --------------------------------------------------------------------------------------------------------------------------------------------
            elif etat == 'L':  # Si on regarde le dessin
                if tunnelParent.poll():  # On get les nouveaux points
                    for raw_data in tunnelParent.recv().decode().split("@"):
                        data = raw_data.split(",")
                        if data[0] == 'D':  # Si c'est un dessin, on décode les infos
                            pos = data[1].split(";")
                            pos = tuple(map(int, pos))
                            last = data[2].split(";")
                            last = tuple(map(int, last))
                            couleur = data[3].split(";")
                            couleur = tuple(map(int, couleur))
                            rayon = int(data[4])
                            pygame.display.update(pygame.draw.circle(fenetre, couleur, pos, rayon))
                            dessin(fenetre, couleur, pos, last,  rayon)
                            
                        elif data[0] == 'F':
                            print(joueurs[int(data[1])] + " est parti")
                            del joueurs[int(data[1])]  # On supprime le joueur
                            del roles[int(data[1])]
                        elif data[0] == 't':
                            listmsg.append(joueurs[int(data[1])] + " : " + data[2])
                        elif data[0] == "E":  # Si on reçoit cette valeur c'est que le joueur a tout effacé
                            pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
                        elif data[0] == "M":  # On décode le mot à deviner
                            motdevin = data[1]
                            tempsFin = time() + temps
                        elif data[0] == "O":
                            listmsg.append(joueurs[int(data[1])] + " a trouvé le mot")
                        elif data[0] == "R":
                            listmsg.append("C'était " + motdevin)
                            for j in joueurs:
                                if j == int(data[1]):
                                    roles[j] = "D"
                                else:
                                    roles[j] = "L"
                            if int(data[1]) == int(monID):
                                etat = "D"
                            trouves = 0
                            motChoisi = False
                            selectionMot = True
                            motdevin = "mot pas choisi"
                            motcache = "mot pas choisi"
                            verif = False
                            pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
                        elif data[0] == "V":
                            easter = 1
                        #elif data[0] == "P":
                            #Faut faire un truc pour les points

                if not verif and motdevin != "mot pas choisi":  # Si le mot n'a pas été trouvé ou qu'il n'a pas été choisi
                    motcache = ['_'] * len(motdevin)
                    motcache = str(' '.join(motcache))
                    affmotcache = police.render(motcache, True, (0, 0, 0))
                elif motdevin == "mot pas choisi":
                    motcache = motdevin
                    affmotcache = police.render(motcache, True, (0, 0, 0))

                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # Si on appuie sur ECHAP
                        tunnelParent.send(("F," + str(monID) + '@').encode())  # On envoie F pour signaler que le joueur est parti au serveur
                        fini = True  # On ferme la fenêtre
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # Si on appuie sur entrée et que le mot n'est pas vide
                            if motEcrit == motdevin and not verif:
                                motcache = motdevin  # On affiche le mot qui devait être deviné au joueur qui l'a trouvé
                                affmotcache = police.render(motcache, True, (0, 0, 0))
                                point = tempsFin - time()
                                listmsg.append("Vous avez trouvé le mot!")
                                tunnelParent.send(("O," + str(monID) + '@').encode())
                                tunnelParent.send(("P," + str(monID) + str(point) + '@').encode())
                                verif = True
                            elif motEcrit == "406SW":
                                easter = 1
                                tunnelParent.send("V@".encode())
                            else:
                                listmsg.append(joueurs[int(monID)] + " : " + motEcrit)  # On ajoute le mot à la liste du chat
                                tunnelParent.send(("t," + str(monID) + "," + motEcrit + '@').encode())  # On envoie le message avec le pseudo au serveur
                            motEcrit = ''  # On réinitialise le mot

                        elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                            motEcrit = motEcrit[:-1]  # du 1er caractère inclus jusqu'au dernier exclu

                        elif len(motEcrit) < 16 and motdevin != "mot pas choisi":  # 16 caractères max
                            motEcrit = motEcrit + event.unicode
                            
                entete = pygame.draw.rect(fenetre, gris, (400, 0, 1920, 100))  # Fond gris de le zone de l'entête
                if easter != 1 or xE > 1520:
        
                    if idFrame < 20:
                        poslogo = logo1.get_rect(center=(int(largeur / 2), 50))
                        fenetre.blit(logo1, poslogo)
                    else:
                        poslogo = logo2.get_rect(center=(int(largeur / 2), 50))
                        fenetre.blit(logo2, poslogo)

                else:
                    xE += 3
                    fenetre.blit(imgpeu, (int(xE), yE))

                fonpal = pygame.draw.rect(fenetre, blanc, (1720, 100, 200, 980))  # Fond de la palette de couleur
                tab = pygame.draw.rect(fenetre, gris, (0, 0, 390, 1920))  # Fond gris de le zone de chat
                ligne = pygame.draw.rect(fenetre, noir, (390, 0, 10, 980))  # Dessin des lignes de la palette
                ligne2 = pygame.draw.rect(fenetre, noir, (0, 970, 1920, 10))
                bas = pygame.draw.rect(fenetre, gris, (0, 980, 1920, 1920))  # Fond gris de le zone de texte
                souligne = pygame.draw.rect(fenetre, noir, (10, 50, 340, 5))
                ligne12 = pygame.draw.rect(fenetre, noir, (390, 100, 1920, 5))
                effac = pygame.draw.rect(fenetre, gris, (1720, 10, 190, 80))
                fenetre.blit(affmotcache, (1400, 1000))

                if motdevin != "mot pas choisi":
                    affChrono = police.render(str(int(tempsFin - time())), True, (0, 0, 0))
                    fenetre.blit(affChrono, (1810, 610))

                idFrame = (idFrame + 0.1) % 40  # Animation su logo Super-Sketch et de la barre de saisie
                if idFrame < 20:
                    poslogo = logo1.get_rect(center=(int(largeur / 2), 50))
                    fenetre.blit(logo1, poslogo)
                    barre = '|'
                else:
                    poslogo = logo2.get_rect(center=(int(largeur / 2), 50))
                    fenetre.blit(logo2, poslogo)
                    barre = ''

                if len(joueurs) <= 1:
                    fini = True  # On ferme la fenêtre
                    break

                textMotEcrit = police.render('Ecrivez un mot : ' + motEcrit + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textMotEcrit, (50, 1000))
                textJoueur = police.render('Joueurs en ligne : ', True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textJoueur, (10, 0))
                xJoueur = 0
                for j in joueurs:
                    nomJoueur = police.render(joueurs[j] + " : " + roles[j], True, (0, 0, 0))
                    fenetre.blit(nomJoueur, (10, 60 + xJoueur*50))
                    xJoueur += 1

                for i in range(10):  # Affichage du texte dans le chat
                    listmsg = listmsg[-10:]  # On garde uniquement les 10 derniers termes de la listes
                    textchat = police2.render(listmsg[i], True, (0, 0, 0))
                    fenetre.blit(textchat, (50, 480 + 50 * i))  # On affiche la liste avec les coord saisie précédemment
                    

                pygame.display.flip()  # raffraichissment de la fenêtre
                clock.tick(200)
    pygame.quit()
    if procClient.is_alive():
        procClient.join()
    if procServeur.is_alive():
        procServeur.terminate()  # ferme le serveur
        procServeur.join()
