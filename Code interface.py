import pygame
from pygame.locals import *
import ctypes
from ctypes import windll
pygame.init()
#Ouverture de la fenêtre Pygame en plein écran

idFrame = 0
largeur=1080
longueur=1920
ctypes.windll.user32.SetProcessDPIAware()
true_res = (windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1))
fenetre = pygame.display.set_mode(true_res,pygame.FULLSCREEN)
pygame.display.set_caption("Super-sketch")
clock = pygame.time.Clock()

pygame.init()
fond = pygame.image.load("img/fond.png").convert()
fenetre.blit(fond, (0,0))
pal1 = pygame.image.load("img/pal1.png").convert_alpha()
pal2 = pygame.image.load("img/pal2.png").convert_alpha()
xLogo = int(largeur/2 - pal2.get_rect().size[0]/2)
rouge=(255,0,0)
vert=(0,255,0)
bleuf=(0,0,255)
blanc=(255,255,255)
noir=(0,0,0)
bleuc=(38, 188, 254)
violet=(238,130,238)
marron=(88,41,0)
press= False

#Boucle infinie pour maintenir ou fermer la fenêtre
continuer = 1
while continuer:
        try:
                
                btr=pygame.draw.rect(fenetre, rouge,(1820,100,100,100))
                btv=pygame.draw.rect(fenetre, vert,(1720,100,100,100))
                btbl=pygame.draw.rect(fenetre, blanc,(1820,200,100,100))
                btn=pygame.draw.rect(fenetre, noir,(1720,200,100,100))
                btm=pygame.draw.rect(fenetre, marron,(1820,300,100,100))
                btvi=pygame.draw.rect(fenetre, violet,(1720,300,100,100))
                btbf=pygame.draw.rect(fenetre, bleuf,(1820,400,100,100))
                btbc=pygame.draw.rect(fenetre, bleuc,(1720,400,100,100))
                pygame.init()
                for event in pygame.event.get():                       
                        if event.type == QUIT:                                                             
                                pygame.quit()
                                continuer =0

                pygame.init()
                px, py = pygame.mouse.get_pos()
                if btbf.collidepoint(px, py):
                        idFrame = (idFrame + 1) % 40  # logo qui bouge tout les 1/4s ou 20images car 80fps
                        if idFrame < 20:
                                fenetre.blit(pal1, (xLogo, 50))
                        else:
                                fenetre.blit(pal2, (xLogo, 50))
                        
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
        



