import pygame
from pygame.locals import *

pygame.init()
#Ouverture de la fenêtre Pygame en plein écran
fenetre = pygame.display.set_mode((1366, 768), FULLSCREEN)
pygame.display.set_caption("Super-sketch")
clock = pygame.time.Clock()

pygame.init()
fond = pygame.image.load("img/fond.png").convert()
fenetre.blit(fond, (0,0))       


rouge=(255,0,0)
vert=(0,255,0)
bleuf=(0,0,255)



press = False

#Boucle infinie pour maintenir ou fermer la fenêtre
continuer = 1
while continuer:
        try:
                
                pygame.draw.rect(fenetre, rouge,(1316,100,50,50))
                pygame.draw.rect(fenetre, vert,(1266,100,50,50))
                pygame.draw.rect(fenetre, rouge,(1316,150,50,50))
                pygame.draw.rect(fenetre, vert,(1266,150,50,50))
                pygame.draw.rect(fenetre, rouge,(1316,200,50,50))
                pygame.draw.rect(fenetre, vert,(1266,200,50,50))
                pygame.draw.rect(fenetre, rouge,(1316,250,50,50))
                pygame.draw.rect(fenetre, vert,(1266,250,50,50))
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
        



