import pygame
from pygame.locals import *

pygame.init()
#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((1920, 1080), FULLSCREEN)









#Boucle infinie
continuer = 1
while continuer:
        for event in pygame.event.get():   
                if event.type == QUIT:    
                    pygame.quit()
                    continuer =0



