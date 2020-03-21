import pygame
from pygame.locals import *
from random import *
import ctypes
from ctypes import windll
from multiprocessing import Process, Queue, Value, Array, Lock
import time
import serveur
import client

# FAUT FERMER AVEC ECHAP

if __name__ == '__main__':  # Si c'est le programme pricipal / obligatoire pour multiprocessing
    # Etat du menu
    fini = False
    acceuil = True
    host = False
    join = False

    # Style fenetre
    bgColor = (118, 188, 194)

    pygame.init()

    # caractéristiques de l'écran
    ctypes.windll.user32.SetProcessDPIAware()
    largeur = windll.user32.GetSystemMetrics(0)
    hauteur = windll.user32.GetSystemMetrics(1)
    fenetre = pygame.display.set_mode((largeur, hauteur), pygame.FULLSCREEN)

    pygame.display.set_caption("Super-sketch")
    fenetre.fill(bgColor)

    # initialisation cadence
    clock = pygame.time.Clock()
    idFrame = 0

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

    # Btn d'hébergement
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

    # Idem pour le btn rejoindre :
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

    textPseudo = police.render('Entrez votre pseudo : ', True,
                               (0, 0, 0))  # Rendu du texte avec (texte, antialiasing, noir)
    pseudo = ''

    procServeur = Process()  # on initialise le process pour pouvoir le fermer
    procDiffu = Process()
    procClient = Process()
    dessin = Queue()
    init = True
    start = False
    clients = Array('c', 68)
    lockServ = Lock()
    nbClient = Value('i', 0)
    etat = 0
    px = 5000
    py = 5000


    # Déclaration de la fonction de sélection de la couleur
    def selection(pbt, cbt):
        global couleur  # Définition de variable globale du programme
        global idFrame
        idFrame = (idFrame + 1) % 95  # Animation de l'image
        if idFrame < 30:
            fenetre.blit(pal1, pbt)
        else:
            fenetre.blit(pal2, pbt)
        if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de couleur lors d'un clic
            couleur = cbt
        return


    def selectioncercle1():
        global rayon  # Définition de variable globale du programme
        if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de rayon lors d'un clic
            rayon = rayon + 5
        time.sleep(0.1)
        return


    def selectioncercle2():
        global rayon  # Définition de variable globale du programme

        if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de rayon lors d'un clic
            rayon = rayon - 5
        time.sleep(0.1)
        return


    fond = pygame.image.load("img/fond.png").convert()
    fenetre.blit(fond, (0, 0))

    # Initialisation des variables de couleur et des animations
    pal1 = pygame.pal1 = pygame.image.load("img/pal1.png").convert_alpha()
    pal2 = pygame.image.load("img/pal2.png").convert_alpha()
    fon = pygame.image.load("img/pal4.png").convert_alpha()
    rouge = (255, 0, 0)
    vert = (0, 255, 0)
    bleuf = (0, 0, 255)
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    bleuc = (38, 188, 254)
    violet = (238, 130, 238)
    marron = (88, 41, 0)

    couleur = noir
    rayon = 10
    ancienpx = 2000  # hors écran
    ancienpy = 2000

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

            if not host and not join:  # menu sans avoir cliquer
                fenetre.blit(borderbtnHost, posborderbtnHost)  # Bordure
                fenetre.blit(paddingbtnHost, pospaddingbtnHost)  # Fond bleu

                if posborderbtnHost.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:  # Si clique sur le btn
                        host = True
                    else:  # si il le survole => fond sombre
                        fenetre.blit(paddingbtnHostOmbre, pospaddingbtnHost)
                fenetre.blit(btnHost, posbtnHost)  # Affichage du texte

                fenetre.blit(borderbtnJoin, posborderbtnJoin)  # Bordure
                fenetre.blit(paddingbtnJoin, pospaddingbtnJoin)  # Fond bleu
                if posborderbtnJoin.collidepoint(pos):  # si pos souris est sur le btn rejoindre
                    if pygame.mouse.get_pressed()[0] == 1:  # Si clique sur le btn
                        join = True
                    else:  # si il le survole => fond sombre
                        fenetre.blit(paddingbtnJoinOmbre, pospaddingbtnJoin)
                fenetre.blit(btnJoin, posbtnJoin)  # Affichage du texte

            if host or join:
                if idFrame < 24:  # barre qui clignotte du pseudo
                    barre = '|'
                else:
                    barre = ''
                textPseudo = police.render('Entrez votre pseudo : ' + pseudo + barre, True,
                                           (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textPseudo, (400, 530))

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == MOUSEBUTTONDOWN and poscroix.collidepoint(pos)):
                    acceuil = False
                    fini = True

                if event.type == pygame.KEYDOWN:
                    if host or join:  # Si une touche est pressée
                        if event.key == pygame.K_RETURN:  # si entrer
                            if host:
                                procDiffu = Process(target=serveur.diffuIpHote)
                                procDiffu.daemon = True
                                procDiffu.start()  # Lancement du processus de la diffusion de l'ip
                                procServeur = Process(target=serveur.serveur, args=(nbClient, clients, lockServ))  # lancement du serveur dans un processus parallèle
                                procServeur.start()
                            acceuil = False  # fin de l'acceuil
                        elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                            pseudo = pseudo[:-1]  # du 1er caractère inclus jusqu'au dernier exclu
                        elif len(pseudo) < 16:  # 16 caractères max
                            pseudo += event.unicode

            clock.tick(80)  # limite 80fps
            pygame.display.flip()  # Rafraichissement écran acceuil avec toutes nos modifs
        else:
            if init:
                if host:
                    procClient = Process(target=client.client, args=(0, dessin, pseudo))
                    procClient.start()
                    while not start and not fini:
                        pos = pygame.mouse.get_pos()

                        fenetre.fill((255, 255, 255))  # fond blanc
                        texteConn = police.render(str(nbClient.value) + ' connectés', True, (0, 0, 0))
                        fenetre.blit(texteConn, (0, 0))

                        fenetre.blit(croix, poscroix)

                        for event in pygame.event.get():
                            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                                nbClient.value = -2
                                fini = True
                            if event.type == MOUSEBUTTONDOWN and poscroix.collidepoint(pos):
                                if nbClient.value >= 2:
                                    if procDiffu.is_alive():
                                        procDiffu.terminate()
                                        procDiffu.join()
                                    dessin.put(b'\x11')
                                    etat = b'D'
                                    start = True
                        for i in range(nbClient.value):
                            print(clients[:])
                            txtJoueurs = police.render(clients[i * 17 + 1: (i + 1) * 17].strip(b'\0').decode() + ' connecté', True, (0, 0, 0))
                            fenetre.blit(txtJoueurs, (50 * (i + 1), 50 * (i + 1)))
                        pygame.display.flip()
                        clock.tick(1)
                    fenetre.fill((255, 255, 255))
                else:
                    procClient = Process(target=client.client, args=(1, dessin, pseudo))
                    procClient.start()
                    fenetre.fill((255, 255, 255))
                    txtAttente = police.render('On le attend le départ Les Filles', True, (0, 0, 0))  # A remmetre en haut mais plus tard
                    fenetre.blit(txtAttente, (500, 500))
                    pygame.display.flip()
                    while dessin.empty():
                        fenetre.fill((255, 255, 255))
                        fenetre.blit(txtAttente, (500, 500))
                        for event in pygame.event.get():  # Pour pas que ca freeze durant le get
                            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                                fini = True
                        pygame.display.flip()
                        clock.tick(30)
                    etat = dessin.get()
                    while dessin.empty():
                        fenetre.fill((255, 255, 255))
                        fenetre.blit(txtAttente, (500, 500))
                        for event in pygame.event.get():  # Pour pas que ca freeze durant le get
                            if event.type == QUIT:
                                fini = True
                        pygame.display.flip()
                        clock.tick(30)
                    dessin.get()
                init = False
            elif etat == b'D':
                # Lancement du dessin:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        if host:
                            dessin.put(b'\xff\xff\xff\xff')  # 00000000 = fin de la conn
                        fini = True

                # Placement des boutons sur l'écran
                fenetre.blit(fon, (1820, 500))
                fenetre.blit(fon, (1720, 500))
                btr = pygame.draw.rect(fenetre, rouge, (1820, 100, 100, 100))
                btv = pygame.draw.rect(fenetre, vert, (1720, 100, 100, 100))
                btbl = pygame.draw.rect(fenetre, blanc, (1820, 200, 100, 100))
                btn = pygame.draw.rect(fenetre, noir, (1720, 200, 100, 100))
                btm = pygame.draw.rect(fenetre, marron, (1820, 300, 100, 100))
                btvi = pygame.draw.rect(fenetre, violet, (1720, 300, 100, 100))
                btbf = pygame.draw.rect(fenetre, bleuf, (1820, 400, 100, 100))
                btbc = pygame.draw.rect(fenetre, bleuc, (1720, 400, 100, 100))
                btcg = pygame.draw.circle(fenetre, noir, (1870, 550), 35)  # bouton circulaire gros rayon
                btcp = pygame.draw.circle(fenetre, noir, (1770, 550), 15)  # bouton circulaire petit rayon
                # Détection de la position de la souris
                px, py = pygame.mouse.get_pos()

                # Détection du moment quand la souris passe sur les boutons
                if btbf.collidepoint(px, py):
                    selection(btbf, bleuf)
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

                # Détection clique gauche pour effectuer le dessin

                # --> Va falloir faire des segments ou ajouter des cercles entre chaques points car 100fps max pour serv

                if pygame.mouse.get_pressed()[0] == 1 and (px != ancienpx or py != ancienpy):
                    pygame.draw.circle(fenetre, couleur, (px, py), rayon)
                    if host:  # On envoie les données au process
                        dessin.put(px.to_bytes(2, byteorder='big', signed=False) + py.to_bytes(2, byteorder='big', signed=False))
                    ancienpx = px
                    ancienpy = py
                pygame.display.flip()
                clock.tick(100)
            elif etat == b'L':
                if not dessin.empty():
                    data = dessin.get()  # Blocant
                    px = int.from_bytes(data[0:2], 'big', signed=False)
                    py = int.from_bytes(data[2:4], 'big', signed=False)
                    if data == b'\xff\xff\xff\xff':
                        print("fermeture")
                        fini = True

                fenetre.fill((255, 255, 255))

                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        fini = True

                # Faire dessin a partir de px/py

                txtPos = police.render('px: ' + str(px) + "  py : " + str(py), True, (0, 0, 0))  # A remmetre en haut mais plus tard
                fenetre.blit(txtPos, (500, 500))
                pygame.display.flip()
                clock.tick(400)
            else:
                print(etat)

    pygame.quit()
    if procClient.is_alive():
        procClient.terminate()
        procClient.join()
    if procServeur.is_alive():
        procServeur.terminate()  # ferme le serveur
        procServeur.join()
