import pygame
from pygame.locals import *

pygame.init()
#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((1920, 1080), FULLSCREEN)
pygame.display.set_caption("Super-sketch")

        
Bouton_1 = pygame.image.load("img/bouton.png").convert_alpha()
Bouton_1_pos = (100, 100)
fenetre.blit(Bouton_1, Bouton_1_pos)





#Boucle infinie
continuer = 1
while continuer:
        for event in pygame.event.get():   
                if event.type == QUIT:    
                    pygame.quit()
                    continuer =0
        pygame.display.flip()



        



