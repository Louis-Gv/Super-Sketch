import pygame
from pygame.locals import *

pygame.init()
#Ouverture de la fenêtre Pygame en plein écran
fenetre = pygame.display.set_mode((1920, 1080), FULLSCREEN)
pygame.display.set_caption("Super-sketch")
clock = pygame.time.Clock()

pygame.init()
fond = pygame.image.load("img/fond.png").convert()
fenetre.blit(fond, (0,0))       
fond2 = pygame.image.load("img/fond2.png").convert()
size = width, height = (100,100)
canvas = pygame.Surface(size)



#Chargement et collage du bouton bleu clair
btbleu = pygame.image.load("img/bleuc.png").convert_alpha()
btbleu_pos = (1675, 200)
fenetre.blit(btbleu, btbleu_pos)
 
#Chargement et collage du bouton rouge
btrouge = pygame.image.load("img/rouge.png").convert_alpha()
btrouge_pos = (1625,200)
fenetre.blit(btrouge, btrouge_pos)

#Chargement et collage du bouton blanc
btblanc = pygame.image.load("img/blanc.png").convert_alpha()
btblanc_pos = (1675,250)
fenetre.blit(btblanc, btblanc_pos)

#Chargement et collage du bouton jaune
btjaune = pygame.image.load("img/jaune.png").convert_alpha()
btjaune_pos = (1625,250)
fenetre.blit(btjaune, btjaune_pos)

#Chargement et collage du bouton marron
btmarron = pygame.image.load("img/marron.png").convert_alpha()
btmarron_pos = (1675,300)
fenetre.blit(btmarron, btmarron_pos)

#Chargement et collage du bouton noir
btnoir = pygame.image.load("img/noir.png").convert_alpha()
btnoir_pos = (1625,300)
fenetre.blit(btnoir, btnoir_pos)

#Chargement et collage du bouton orange
btorange = pygame.image.load("img/orange.png").convert_alpha()
btorange_pos = (1675,350)
fenetre.blit(btorange, btorange_pos)

#Chargement et collage du bouton vert
btvert = pygame.image.load("img/vert.png").convert_alpha()
btvert_pos = (1625,350)
fenetre.blit(btvert, btvert_pos)

#Chargement et collage du bouton violet
btviolet = pygame.image.load("img/violet.png").convert_alpha()
btviolet_pos = (1675,400)
fenetre.blit(btviolet, btviolet_pos)

#Chargement et collage du bouton bleu foncé
btbleuf = pygame.image.load("img/bleuf.png").convert_alpha()
btbleuf_pos = (1625,400)
fenetre.blit(btbleuf, btbleuf_pos)

#Chargement et collage du bouton up
btup = pygame.image.load("img/up.png").convert_alpha()
btup_pos = (1625,470)
fenetre.blit(btup, btup_pos)

#Chargement et collage du bouton down
btdown = pygame.image.load("img/down.png").convert_alpha()
btdown_pos = (1625,570)
fenetre.blit(btdown, btdown_pos)



press = False

#Boucle infinie pour maintenir ou fermer la fenêtre
continuer = 1
while continuer:
        try:
                fenetre.blit(canvas,(400,400))
                pygame.init()
                for event in pygame.event.get():                       
                        if event.type == QUIT:                                                             
                                pygame.quit()
                                continuer =0

                pygame.init()
                px, py = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1,0,0):
                        pygame.draw.rect(fenetre, (128,128,128), (px,py,10,10))
 
                if event.type == pygame.MOUSEBUTTONUP:                        
                        press == False
                pygame.display.update()
                clock.tick(1000)
                
        
        except Exception as e:
            print(e)
            pygame.quit()


pygame.quit()
        



