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
btpal = pygame.image.load("img/palette.png").convert_alpha()
size2 = (100, 500)
palette = pygame.Surface(size2)
 




press = False

#Boucle infinie pour maintenir ou fermer la fenêtre
continuer = 1
while continuer:
        try:
                fenetre.blit(canvas,(400,400))
                fenetre.blit(palette,(1675,200))
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
        



