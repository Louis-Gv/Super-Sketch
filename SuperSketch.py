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

    procServeur = Process()  # on initialise les process pour pouvoir les fermer
    procDiffu = Process()
    procClient = Process()
    tunnelParent, tunnelEnfant = Pipe()  # Tunnel de données entre le Process principal et le Process client
    init = True
    start = False
    joueurs = {}
    monID = 0
    roles = {}
    etat = 0

    play = pygame.image.load("img/lobby/play.png")
    posplay = play.get_rect(topright=(largeur - 15, 15))
    txtAttente = police.render("En attente de l'hote", True, (0, 0, 0))

    px = 5000
    py = 5000

    # - Partie dessin
    # Déclaration de la fonction de sélection de la couleur
    def selection(pbt, cbt):
        global couleur  # Définition de variable globale du programme
        global idFrame # Animation de l'image
        if idFrame < 30:
            fenetre.blit(pal1, pbt)
        else:
            fenetre.blit(pal2, pbt)
        if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de couleur lors d'un clic gauche
            couleur = cbt
        return


    def selectioncercle1():
        global rayon  # Définition de variable globale du programme
        if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de rayon lors d'un clic
            rayon = rayon + 5
        pygame.time.wait(100)
        return


    def selectioncercle2():
        global rayon  # Définition de variable globale du programme

        if pygame.mouse.get_pressed() == (1, 0, 0):  # Changement de rayon lors d'un clic
            rayon = rayon - 5
            if rayon < 5:
                rayon = rayon + 10
        pygame.time.wait(100)
        return
    
    def effacfx():
        global eff
        pygame.draw.rect(fenetre, noir, (1720, 10, 190, 5))
        pygame.draw.rect(fenetre, noir, (1720, 10, 5, 80))
        pygame.draw.rect(fenetre, noir, (1910, 10, 5, 80))
        pygame.draw.rect(fenetre, noir, (1720, 85, 190, 5))
        if pygame.mouse.get_pressed() == (1, 0, 0):  # Detection du clic
            pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
            eff=1
            tunnelParent.send("E".encode())



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
    gris= (192, 192, 192)
    police2 = pygame.font.SysFont("roboto-bold", 35)
    motEcrit = ''
    listmsg = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']     #Initialisation de la liste du chat vide
    couleur = noir
    rayon = 10
    ancienpx = 2500  # hors écran
    ancienpy = 2500
    gomme1= pygame.image.load("img/gomme1.png").convert_alpha()
    choixmot='Z'
    cache = "R"
    motdevin="mot pas choisi"
    motcache="mot pas choisi"
    verif='F'

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
                                procServeur = Process(target=serveur.serveur)
                                procServeur.start()  # lancement du serveur dans un processus parallèle
                            acceuil = False  # fin de l'acceuil
                        elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                            pseudo = pseudo[:-1]  # du 1er caractère inclus jusqu'au dernier exclu
                        elif len(pseudo) < 16:  # 16 caractères max
                            pseudo += event.unicode

            clock.tick(80)  # limite 80fps
            pygame.display.flip()  # Rafraichissement écran acceuil avec toutes nos modifs
        else:  # pas dans l'acceuil
            if init:
                if host:
                    procClient = Process(target=client.client, args=(0, tunnelEnfant, pseudo))
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
                                        tableauJoueur = tableauJoueur + "," + str(idTableauJoueur) + ";" + joueurs[
                                            idTableauJoueur] + ";"
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
                        clock.tick(10)
                    fenetre.fill((255, 255, 255))
                else:
                    procClient = Process(target=client.client, args=(1, tunnelEnfant, pseudo))
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
                                print(joueurs, roles, etat)
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
            if etat == 'D':  # Si on dessine
                px, py = pygame.mouse.get_pos()                   # Détection de la position de la souris
                   
                # ---------------------------------------------------------------------------------------------------------------------------------------
                if tunnelParent.poll():  # On get les nouveaux points
                    data = tunnelParent.recv().decode().split(",")
                    if data[0] == 'F':
                        print(joueurs[int(data[1])] + " est parti")
                        del joueurs[int(data[1])]
                        del roles[int(data[1])]
                    elif data[0] == 't':
                        listmsg.append(joueurs[int(data[1])] + " : " + data[2])            #On ajoute à la liste du chat le pseudo de l'envoyeur et son texte
                
                # Lancement du dessin:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):    #Si on appuie sur ECHAP
                        tunnelParent.send(("F," + str(monID)).encode())                         #On envoie l'info que l'on quitte le serveur
                        fini = True                 #On ferme la fenêtre
                # Placement des boutons sur l'écran
                fenetre.blit(fon, (1820, 500))
                fenetre.blit(fon, (1720, 500))
                fonpal = pygame.draw.rect(fenetre, blanc, (1720,100, 200 ,980))
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
                tab = pygame.draw.rect(fenetre, gris, (0, 0, 390, 1920))
                ligne = pygame.draw.rect(fenetre, noir, (390, 0, 10, 980))
                ligne2 = pygame.draw.rect(fenetre, noir, (0, 970, 1920, 10))
                bas = pygame.draw.rect(fenetre, gris, (0, 980, 1920, 1920))
                ligne3 = pygame.draw.rect(fenetre, noir, (1720, 100, 1000, 5))
                ligne4 = pygame.draw.rect(fenetre, noir, (1720, 200, 1000, 5))
                ligne5 = pygame.draw.rect(fenetre, noir, (1720, 300, 1000, 5))
                ligne6 = pygame.draw.rect(fenetre, noir, (1720, 400, 1000, 5))
                ligne7 = pygame.draw.rect(fenetre, noir, (1720, 500, 1000, 5))
                ligne8 = pygame.draw.rect(fenetre, noir, (1720, 600, 1000, 5))
                ligne9 = pygame.draw.rect(fenetre, noir, (1720, 100, 5, 500))
                ligne10 = pygame.draw.rect(fenetre, noir, (1820, 100, 5, 500))
                ligne11 = pygame.draw.rect(fenetre, noir, (1915, 100, 5, 500))
                souligne = pygame.draw.rect(fenetre, noir,(10, 50, 340, 5))
                ligne12 = pygame.draw.rect(fenetre, noir, (390, 100, 1920, 5))
                entete = pygame.draw.rect(fenetre, gris, (400,0,1920,100))
                fenetre.blit(gomme1, (1830,220))
                effac = pygame.draw.rect(fenetre, blanc, (1720,10,190,80))     #Création du bouton pour tout effacer
                txteffac = police2.render("Tout effacer", True, (0, 0, 0))
                fenetre.blit(txteffac,(1745, 40))

                if choixmot != 'C':         #Si le mot n'est pas chosi
                    if cache != "K":        #Si trois mot n'ont pas été choisis au hasard
                        limots = [word.strip() for word in open("dico.txt", encoding="utf-8")]   #On créer une liste à partir d'un document texte
                        mot1= choice(limots)        #On choisi le premier mot
                        mot2= choice(limots)        #On choisit le deuxième mot
                        mot3= choice(limots)        #On chosit le troisième mot
                        affmot1 = police.render(mot1, True, (0, 0, 0))    
                        affmot2 = police.render(mot2, True, (0, 0, 0))
                        affmot3 = police.render(mot3, True, (0, 0, 0))
                        cache = "K"                 #On ferme la boucle de la selection de mots
                       
                    bt1 = pygame.draw.rect(fenetre, blanc, (460, 450, 380,75))     #on affiche les trois mots et leurs boutons
                    bt2 = pygame.draw.rect(fenetre, blanc, (850, 450, 380,75))
                    bt3 = pygame.draw.rect(fenetre, blanc, (1240, 450, 380,75))
                    fenetre.blit(affmot1, (460, 450))
                    fenetre.blit(affmot2, (850, 450))
                    fenetre.blit(affmot3, (1240, 450))
                    if bt1.collidepoint(px,py):
                        if pygame.mouse.get_pressed()[0] == 1:          #Si on clique sur le premier bouton
                            choixmot='C'                                #On ferme la boucle pour choisir le mot
                            motdevin=mot1                               #On initialise le mot à deviner
                            tunnelParent.send(("M" + "," + mot1).encode())    #On envoie le mot au serv
                            pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))      #Onefface les mots
                    if bt2.collidepoint(px,py):
                        if pygame.mouse.get_pressed()[0] == 1:                              #idem
                            motdevin=mot2
                            choixmot='C'
                            tunnelParent.send(("M" + "," + mot2).encode())
                            pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
                    if bt3.collidepoint(px,py):
                        if pygame.mouse.get_pressed()[0] == 1:                              #idem
                            motdevin=mot3 
                            choixmot='C'
                            tunnelParent.send(("M" + "," + mot3).encode())
                            pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
                        
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
                if effac.collidepoint(px,py):
                    effacfx()

                affmotdevin= police.render(motdevin, True, (0, 0, 0))
                fenetre.blit(affmotdevin, (1400, 1000))                      #on affiche le mot à faire deviner
                
                i = 0
                for i in range(10):                      #Affichage du chat
                    listmsg = listmsg[-10:]
                    textchat = police2.render(listmsg[i], True, (0, 0, 0))
                    fenetre.blit(textchat, (50,480+50*i))

                textJoueur = police.render('Joueurs en ligne : ', True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textJoueur, (10, 0))
  
                idFrame = (idFrame + 0.1) % 40      #Animation du logo super-Sketch
                if idFrame < 20:
                   poslogo = logo1.get_rect(center=(int(largeur / 2), 50))
                   fenetre.blit(logo1, poslogo)
                else:
                   poslogo = logo2.get_rect(center=(int(largeur / 2), 50))
                   fenetre.blit(logo2, poslogo)

               # Détection clique gauche pour effectuer le dessin
                if pygame.mouse.get_pressed()[0] == 1 and (px != ancienpx or py != ancienpy):          #Si on clique le dessin s'affiche
                    pygame.draw.circle(fenetre, couleur, (px, py), rayon)
                    tunnelParent.send(('D,' + str(px) + "," + str(py) + "," + str(couleur[0]) + ";" + str(
                        couleur[1]) + ";" + str(couleur[2]) + "," + str(rayon) + ",").encode())  #On envoie toutes les données au serveur
                    # "D,875,745,45;75;0,10,0,"
                    ancienpx = px
                    ancienpy = py

                   
                pygame.display.flip()    #Rafraichissement de la fenêtre
                clock.tick(200)
                # --------------------------------------------------------------------------------------------------------------------------------------------
            elif etat == 'L':  # Si on regarde le dessin
                if tunnelParent.poll():  # On get les nouveaux points
                    data = tunnelParent.recv().decode().split(",")
                    if data[0] == 'D':  # Si c'est un dessin, on décode les infos
                        px = int(data[1])
                        py = int(data[2])
                        couleur = data[3].split(";")
                        couleur = tuple(map(int, couleur))
                        rayon = int(data[4])                  
                    elif data[0] == 'F':
                        print(joueurs[int(data[1])] + " est parti")
                        del joueurs[int(data[1])]  # On supprime le joueur
                        del roles[int(data[1])]

                    elif data[0] == 't':
                        print(data)
                        listmsg.append(joueurs[int(data[1])] + " : " + data[2])

                    elif data[0] == "E":           #Si on reçoit cette valeur c'est que le joueur a tout effacé 
                        pygame.draw.rect(fenetre, blanc, (400, 105, 1320, 865))
                    elif data[0] == "M":           #On décode le mot à deviner
                        motdevin = data[1]

                if verif != 'V' and motdevin!="mot pas choisi":     #Si le mot n'a pas été trouvé ou qu'il n'a pas été choisi
                    motcache=['_']*len(motdevin)
                    motcache=str(' '.join(motcache))
                    affmotcache = police.render(motcache, True, (0, 0, 0))
                elif motdevin == "mot pas choisi":
                    motcache = motdevin
                    affmotcache = police.render(motcache, True, (0, 0, 0))

                
                    


                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):   #Si on appuie sur ECHAP
                        tunnelParent.send(("F," + str(monID)).encode())                         # On envoie F pour signaler que le joueur est parti au serveur
                        fini = True                             #On ferme la fenêtre
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:         #Si on appuie sur entrée
                            if motEcrit == motdevin:
                                tunnelParent.send(("t," + str(monID) + "," + "a trouvé le mot").encode())         #On envoie au chat le joueur a trouvé
                                motcache = motdevin                                                         #On affiche le mot qui devait être deviné au joueur qui l'a trouvé
                                affmotcache = police.render(motcache, True, (0, 0, 0))
                                listmsg.append(joueurs[int(monID)] + " : " + motEcrit)    #On ajoute le mot à la liste du chat
                                verif='V'                                
                            if motEcrit != '' and motEcrit!= motdevin:                  #On vérifie que le mot n'est pas vide
                                listmsg.append(joueurs[int(monID)] + " : " + motEcrit)    #On ajoute le mot à la liste du chat
                                tunnelParent.send(("t," + str(monID) + "," + motEcrit).encode())     #On envoie le message avec le pseudo au serveur
                            motEcrit = ''     #On réinitialise le mot

                        elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                            motEcrit = motEcrit[:-1]  # du 1er caractère inclus jusqu'au dernier exclu

                        elif len(motEcrit) < 16:  # 16 caractères max
                            motEcrit = motEcrit + event.unicode                



                pygame.draw.circle(fenetre, couleur, (px, py), rayon)  #affichage du dessin avec les infos reçus par le serveur

                    
                fonpal = pygame.draw.rect(fenetre, blanc, (1720,100, 200 ,980))    #Fond de la palette de couleur
                tab = pygame.draw.rect(fenetre, gris, (0, 0, 390, 1920))           #Fond gris de le zone de chat
                ligne = pygame.draw.rect(fenetre, noir, (390, 0, 10, 980))         #Dessin des lignes de la palette
                ligne2 = pygame.draw.rect(fenetre, noir, (0, 970, 1920, 10))   
                bas = pygame.draw.rect(fenetre, gris, (0, 980, 1920, 1920))        #Fond gris de le zone de texte
                souligne = pygame.draw.rect(fenetre, noir,(10, 50, 340, 5))
                ligne12 = pygame.draw.rect(fenetre, noir, (390, 100, 1920, 5))
                entete = pygame.draw.rect(fenetre, gris, (400,0,1920,100))         #Fond gris de le zone de l'entête
                effac = pygame.draw.rect(fenetre, gris, (1720,10,190,80))
                textMotEcrit = police.render('Ecrivez un mot : ' + motEcrit + barre, True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textMotEcrit, (50, 1000))
                textJoueur = police.render('Joueurs en ligne : ', True, (0, 0, 0))  # txt,antialiasing,coul
                fenetre.blit(textJoueur, (10, 0))
                fenetre.blit(affmotcache, (1400,1000))
  
                idFrame = (idFrame + 0.1) % 40           #Animation su logo Super-Sketch et de ka barre de saisie
                if idFrame < 20:
                   poslogo = logo1.get_rect(center=(int(largeur / 2), 50))
                   fenetre.blit(logo1, poslogo)
                   barre='|'                               
                else:
                   poslogo = logo2.get_rect(center=(int(largeur / 2), 50))
                   fenetre.blit(logo2, poslogo)
                   barre=''

                i = 0
                for i in range(10):                   #Affichage du texte dans le chat
                    listmsg = listmsg[-10:]           #On garde uniquement les 10 derniers termes de la listes
                    textchat = police2.render(listmsg[i], True, (0, 0, 0))
                    fenetre.blit(textchat, (50,480+50*i))        #On affiche la liste avec les coord saisie précédemment
                
                pygame.display.flip()       #raffraichissment de la fenêtre
                clock.tick(400)
    pygame.quit()
    procClient.join()
    if procServeur.is_alive():
        procServeur.terminate()  # ferme le serveur
        procServeur.join()
