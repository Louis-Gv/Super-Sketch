import pygame
from pygame.locals import *
from random import *
import ctypes
from ctypes import windll

# Etat du menu
continuer = True
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
poslogo = logo1.get_rect(center=(int(largeur/2), 100))
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
poscroix = croix.get_rect(topright=(largeur-15, 15))
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

textPseudo = police.render('Entrez votre pseudo : ', True, (0, 0, 0))  # Rendu du texte avec (texte, antialiasing, noir)
pseudo = ''

while continuer:  # Boucle tant que le joueur reste dans le menu
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
        textPseudo = police.render('Entrez votre pseudo : ' + pseudo + barre, True, (0, 0, 0))  # txt,antialiasing,coul
        fenetre.blit(textPseudo, (400, 530))

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == MOUSEBUTTONDOWN and poscroix.collidepoint(pos)):
            # si il ferme ou quitte avec la croix // (event.type == KEYDOWN and event.key == K_ESCAPE)
            continuer = 0
        if event.type == pygame.KEYDOWN and (host or join):  # Si une touche est pressée
            if event.key == pygame.K_RETURN:  # si entrer
                print(pseudo)
                pseudo = ''
            elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                pseudo = pseudo[:-1]  # du 1er caractère inclus jusqu'au dernier exclu
            elif len(pseudo) < 16:  # 16 caractères max
                pseudo += event.unicode

    clock.tick(80)  # limite 80fps
    pygame.display.flip()  # Rafraichissement écran avec toutes nos modifs
pygame.quit()
