
import pygame
from pygame.locals import *
import ctypes
from ctypes import windll
import time

#Déclaration de la fonction de sélection de la couleur
def selection (pbt, cbt):
    global couleur    #Définition de variable globale du programme
    global idFrame
    idFrame = (idFrame + 1) % 95    #Animation de l'image 
    if idFrame < 30:
        fenetre.blit(pal1, pbt)
    else:
        fenetre.blit(pal2, pbt)
    if pygame.mouse.get_pressed() == (1,0,0):  #Changement de couleur lors d'un clic
        couleur=cbt
    return

def selectioncercle1 (pbt):
    global rayon    #Définition de variable globale du programme
    global idFrame
    idFrame = (idFrame + 1) % 95    #Animation de l'image 
    if idFrame < 30:
        fenetre.blit(pal1, pbt)
    else:
        fenetre.blit(pal2, pbt)
    if pygame.mouse.get_pressed() == (1,0,0):  #Changement de couleur lors d'un clic
        rayon=rayon+2
    time.sleep ( 1 )
    return

def selectioncercle2 (pbt):
    global rayon    #Définition de variable globale du programme
    global idFrame
    idFrame = (idFrame + 1) % 95    #Animation de l'image 
    if idFrame < 30:
        fenetre.blit(pal1, pbt)
    else:
        fenetre.blit(pal2, pbt)
    if pygame.mouse.get_pressed() == (1,0,0):  #Changement de couleur lors d'un clic
        rayon=rayon-2
    time.sleep ( 1 )
    return

#Ouverture de la fenêtre Pygame en plein écran
pygame.init()
largeur=1080
longueur=1920
ctypes.windll.user32.SetProcessDPIAware()
true_res = (windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1))
fenetre = pygame.display.set_mode(true_res,pygame.FULLSCREEN)
pygame.display.set_caption("Super-sketch")
clock = pygame.time.Clock()
fond = pygame.image.load("img/fond.png").convert()
fenetre.blit(fond, (0,0))

#Initialisation des variables de couleur et des animations
pal1 = pygame.image.load("img/pal1.png").convert_alpha()
pal2 = pygame.image.load("img/pal2.png").convert_alpha()
idFrame=0
rouge=(255,0,0)
prouge=1820,100
vert=(0,255,0)
pvert=(1720,100)
bleuf=(0,0,255)
pbleuf=(1820,400)
blanc=(255,255,255)
pblanc=(1820,200)
noir=(0,0,0)
pnoir=(1720,200)
bleuc=(38, 188, 254)
pbleuc=(1720,400)
violet=(238,130,238)
marron=(88,41,0)

press= False
couleur=noir
rayon=10
#Boucle infinie pour maintenir ou fermer la fenêtre
continuer = 1
while continuer:
        for event in pygame.event.get():                       
                        if event.type == QUIT:                                                             
                                pygame.quit()
                                continuer =0

        #Placement des boutons sur l'écran
        btr=pygame.draw.rect(fenetre, rouge,(1820,100,100,100))
        btv=pygame.draw.rect(fenetre, vert,(1720,100,100,100))
        btbl=pygame.draw.rect(fenetre, blanc,(1820,200,100,100))
        btn=pygame.draw.rect(fenetre, noir,(1720,200,100,100))
        btm=pygame.draw.rect(fenetre, marron,(1820,300,100,100))
        btvi=pygame.draw.rect(fenetre, violet,(1720,300,100,100))
        btbf=pygame.draw.rect(fenetre, bleuf,(1820,400,100,100))
        btbc=pygame.draw.rect(fenetre, bleuc,(1720,400,100,100))
        btcg=pygame.draw.circle(fenetre, noir, (1870,550), 50)   #bouton circulaire gros rayon     
        btcp=pygame.draw.circle(fenetre, noir, (1770,550), 25)   #bouton circulaire petit rayon          
        #Détection de la position de la souris        
        px, py = pygame.mouse.get_pos()

        #Détection du moment quand la souris passe sur les boutons
        if btbf.collidepoint(px, py):
                selection(btbf,bleuf)                                
        if btr.collidepoint(px, py):
                    selection(btr,rouge)
        if btv.collidepoint(px, py):
                selection(btv,vert)
        if btbl.collidepoint(px, py):
                selection(btbl,blanc)
        if btn.collidepoint(px, py):
                selection(btn,noir)
        if btm.collidepoint(px, py):
                selection(btm,marron)
        if btvi.collidepoint(px, py):
                selection(btvi,violet)
        if btbc.collidepoint(px, py):
                selection(btbc,bleuc)
        if btcg.collidepoint(px, py):
                selectioncercle1(btcg)
        if btcp.collidepoint(px, py):
                selectioncercle2(btcp)
            


        #Détection clique gauche pour effectuer le dessin                
        if pygame.mouse.get_pressed() == (1,0,0):
                pygame.draw.circle(fenetre, couleur, (px,py), rayon)
 
        if event.type == pygame.MOUSEBUTTONUP:                        
                press == False

        
        pygame.display.update()
        clock.tick(1000)

              
        
        


pygame.quit()
        



