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
largeur = 1920
hauteur = 1080
bgColor = (118, 188, 194)

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
true_res = (windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1))
fenetre = pygame.display.set_mode(true_res,pygame.FULLSCREEN)
pygame.display.set_caption("Super-sketch")
fenetre.fill(bgColor)

# initialisation cadence
clock = pygame.time.Clock()
idFrame = 0

# chargement du logo au centre de l'écran
logo1 = pygame.image.load("img/lobby/logo1.png")
logo2 = pygame.image.load("img/lobby/logo2.png")
xLogo = int(largeur/2 - logo2.get_rect().size[0]/2)
fenetre.blit(logo1, (xLogo, 50))

nuage = pygame.image.load("img/lobby/nuage.png")
# info nuage Gauche
xNuageG = randint(-600, 1500)
vxNuageG = random() / 3 + .15
yNuageG = randint(0, 250)
# info nuage Droite
xNuageD = randint(400, 2000)
vxNuageD = -(random() / 3 + .15)
yNuageD = randint(0, 250)

soleil = pygame.image.load("img/lobby/soleil.png")
fenetre.blit(soleil, (1645, 22))

padding = 10  # espace autour du texte des btn
police = pygame.font.SysFont("roboto-bold", 65)

# Btn d'hébergement
btnHost = police.render('Héberger Une Partie', True, (0, 0, 0))  # Rendu du texte avec (antialiasing, noir)
posbtnHost = btnHost.get_rect()  # Trouve le rectangle de la surface (x=0, y=0, largeur, hauteur) pour le plaçage au centre

# Rectangle noir plus grand qui sert de bordure
borderbtnHost = pygame.Surface((posbtnHost[2] + 2 * padding, posbtnHost[3] + 2 * padding))
borderbtnHost.fill((0, 0, 0))
posborderbtnHost = borderbtnHost.get_rect()  # Trouve le rectangle de la surface (x=0, y=0, largeur, hauteur) pour le plaçage au centre

# Rectangle bleu plus petit
paddingbtnHost = pygame.Surface((posbtnHost[2] + padding, posbtnHost[3] + padding))
paddingbtnHost.fill(bgColor)
paddingbtnHostOmbre = pygame.Surface((posbtnHost[2] + padding, posbtnHost[3] + padding))  # Pour le survol
paddingbtnHostOmbre.set_alpha(100)
paddingbtnHostOmbre.fill((0, 0, 0))
pospaddingbtnHost = paddingbtnHost.get_rect()  # Trouve le rectangle de la surface (x=0, y=0, largeur, hauteur) pour le plaçage au centre

# On centre tout les rectangles de surfaces pour la pose, ceci optimise le programme car on les calcule 1 seule fois
posbtnHost.center = posborderbtnHost.center = pospaddingbtnHost.center = (int(largeur / 2), 510)

# Idem pour le btn rejoindre :
btnJoin = police.render('Rejoindre Une Partie', True, (0, 0, 0))
# Trouve le rectangle de la surface
posbtnJoin = btnJoin.get_rect()

borderbtnJoin = pygame.Surface((posbtnJoin[2] + 2 * padding, posbtnJoin[3] + 2 * padding))
borderbtnJoin.fill((0, 0, 0))
posborderbtnJoin = borderbtnJoin.get_rect()

paddingbtnJoin = pygame.Surface((btnJoin.get_rect()[2] + padding, posbtnJoin[3] + padding))
paddingbtnJoin.fill(bgColor)
paddingbtnJoinOmbre = pygame.Surface((posbtnJoin[2] + padding, posbtnJoin[3] + padding))
paddingbtnJoinOmbre.set_alpha(100)
paddingbtnJoinOmbre.fill((0, 0, 0))
pospaddingbtnJoin = paddingbtnJoin.get_rect()

posbtnJoin.center = posborderbtnJoin.center = pospaddingbtnJoin.center = (int(largeur / 2), 680)

textPseudo = police.render('Entrez votre pseudo : ', True, (0, 0, 0))  # Rendu du texte avec (antialiasing, noir)
pseudo = ''

while continuer:  # Boucle tant que le joueur reste dans le menu
    fenetre.fill(bgColor)  # Retour à zéro

    fenetre.blit(soleil, (1645, 22))

    xNuageG += vxNuageG  # On ajoute la vitesse a la pos du nuage
    if xNuageG > 1930:  # Si sort de l'écran
        xNuageG = randint(-600, -300)  # Retourne au départ
    fenetre.blit(nuage, (int(xNuageG), yNuageG))

    xNuageD += vxNuageD  # On ajoute la vitesse a la pos du nuage
    if xNuageD < - 200:  # Si sort de l'écran
        xNuageD = randint(1930, 2100)  # Retourne au départ
    fenetre.blit(nuage, (int(xNuageD), yNuageD))

    idFrame = (idFrame + 1) % 40  # logo qui bouge tout les 1/4s ou 20images car 80fps
    if idFrame < 20:
        fenetre.blit(logo1, (xLogo, 50))
    else:
        fenetre.blit(logo2, (xLogo, 50))

    if not host and not join:  # menu sans avoir cliquer
        fenetre.blit(borderbtnHost, posborderbtnHost)  # Bordure
        fenetre.blit(paddingbtnHost, pospaddingbtnHost)  # Fond bleu

        pos = pygame.mouse.get_pos()
        if posborderbtnHost.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:  # Si clique sur le btn
                host = True
            else:  # si il le survole => fond sombre
                fenetre.blit(paddingbtnHostOmbre, pospaddingbtnHost)
        fenetre.blit(btnHost, posbtnHost)  # Affichage du texte

        fenetre.blit(borderbtnJoin, posborderbtnJoin)  # Bordure
        fenetre.blit(paddingbtnJoin, pospaddingbtnJoin)  # Fond bleu
        if posborderbtnJoin.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:  # Si clique sur le btn
                join = True
            else:  # si il le survole => fond sombre
                fenetre.blit(paddingbtnJoinOmbre, pospaddingbtnJoin)
        fenetre.blit(btnJoin, posbtnJoin)  # Affichage du texte

    if host or join:
        if idFrame < 24:  # barre du pseudo
            barre = '|'
        else:
            barre = ''
        textPseudo = police.render('Entrez votre pseudo : '+pseudo+barre, True, (0, 0, 0))  # Rendu du texte avec (antialiasing, noir)
        fenetre.blit(textPseudo, (400, 530))

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # si il quitte avec la croix ou echap
            continuer = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(pseudo)
                pseudo = ''
            elif event.key == pygame.K_BACKSPACE:  # On enlève un carartère
                pseudo = pseudo[:-1]  # du 1er caractère inclus jusqu'au dernier exclu
            elif len(pseudo) < 16:  # 16 caractères max
                pseudo += event.unicode

    clock.tick(80)  # limite 80fps
    pygame.display.flip()  # Rafraichissement écran
pygame.quit()
