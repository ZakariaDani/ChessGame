
import pygame
LONGUEUR = LARGEUR = 512
DIMENSION = 8
run = False
CARRE = LARGEUR // DIMENSION
MAX_FPS = 60
WIN = pygame.display.set_mode((752, 800))
IMAGES = {}
i = 0
pieces = ['bp', 'bT', 'bC', 'bF', 'bR', 'bD','np', 'nT', 'nC', 'nF', 'nR', 'nD']
rejouer = False
piece_collectee = {'bp': 0, 'bT': 0, 'bC': 0, 'bF': 0,
                         'bD': 0, 'bK': 0, 'np': 0, 'nT': 0, 'nC': 0, 'nF': 0, 'nD': 0, 'nK': 0}
def load_imagges():
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"),(CARRE,CARRE))
load_imagges()
