import re
from constantes import LARGEUR, LONGUEUR
import pygame
import pygame.freetype
from pygame import mixer
import constantes
from constantes import CARRE, DIMENSION, IMAGES, WIN, pieces
from tkinter import *
from tkinter.ttk import *


class Echiquier:

    def __init__(self):
        self.echiquier = [
            ["nT", "nC", "nF", "nR", "nD", "nF", "nC", "nT"],
            ["np", "np", "np", "np", "np", "np", "np", "np"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["bT", "bC", "bF", "bR", "bD", "bF", "bC", "bT"]]
        self.win = WIN
        self.promotion_piece_blanc = 'bp'
        self.promotion_piece_noir = 'np'

    def dessiner_echiquier(self, win):
        '''
        :param win: window
        :return: Aucune valeur
        :complexity: O(n^2)
        cette méthode a pour role de dessiner l'echiquier, et son interface(Joueurs, pieces colléctées...)
        '''
        positionN = 0
        positionB = 0
        win.fill((117, 53, 13))
        colors = [(139, 69, 19), (244, 164, 96)]
        win.blit(pygame.transform.scale(IMAGES["bR"], (48, 48)), pygame.Rect(140, 100, 64, 64))
        win.blit(pygame.transform.scale(IMAGES["nR"], (48, 48)), pygame.Rect(560, 100, 64, 64))
        font1 = pygame.freetype.Font('fonts/Roboto.ttf', 20)

        font1.render_to(win, (190, 120), 'Joueur 1', (255, 255, 255))
        font1.render_to(win, (485, 120), 'Joueur 2', (0, 0, 0))
        # draw pieces on sides
        longueurPieces = len(pieces)
        idx_roi_blanc = 4
        idx_roi_noir = 10
        for piece in range(longueurPieces):
            if piece < (longueurPieces / 2) and piece != idx_roi_blanc:
                win.blit(pygame.transform.scale(IMAGES[pieces[piece]], (48, 48)),
                         pygame.Rect(15, 168 + positionB, 48, 48))
                font1.render_to(win, (68, 190 + positionB), str(constantes.piece_collectee[constantes.pieces[piece]]), (0, 0, 0))
                positionB += 60
            elif piece != idx_roi_noir and piece != idx_roi_blanc:
                win.blit(pygame.transform.scale(IMAGES[pieces[piece]], (48, 48)),
                         pygame.Rect(658, 168 + positionN, 48, 48))
                font1.render_to(win, (715, 190 + positionN), str(constantes.piece_collectee[constantes.pieces[piece]]), (255, 255, 255))
                positionN += 60
            else:
                continue
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                pygame.draw.rect(win, colors[(r + c) % 2], pygame.Rect(c * CARRE + 120, r * CARRE + 168, CARRE, CARRE))

    def dessiner_pieces(self, win, echiquier):
        '''
            :param win: window, echiquier
            :return: Aucune valeur
            :complexity: O(n^2)
            cette méthode a pour role de poser chaque pièce sur sa propre place
        '''
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = echiquier[r][c]
                if piece != "__":
                    win.blit(IMAGES[piece], pygame.Rect(c * CARRE + 120, r * CARRE + 168, CARRE, CARRE))

    def dessiner(self):
        '''
            :param aucun param
            :return: Aucune valeur
            cette méthode a pour role d'appler les méthodes qui sont responsables du dessin
        '''
        self.dessiner_echiquier(self.win)
        self.dessiner_pieces(self.win, self.echiquier)
        self.Cree_Button("  Quitter", LONGUEUR, LARGEUR - 480, 220, 50, (139, 69, 19), (244, 164, 96))
        self.Cree_Button("  Rejouer", LONGUEUR-500, LARGEUR - 480, 220, 50, (139, 69, 19), (244, 164, 96))

    def S_Menu(self, num, color, titre):
        '''
            :param: numéro du menu, couleur, titre
            :return: Aucune valeur
            cette méthode a pour role d'afficher le menu convenable par rapport aux paramètres passées
        '''
        while True:
            if num == 1:
                WIN.fill((54, 23, 4, 255))
                self.Cree_Button("Demarrer le jeu", 215, LARGEUR // 2, 320, 50, (139, 69, 19), (244, 164, 96))
                self.Cree_Button("           Quitter", 215, LARGEUR - 150, 320, 50, (139, 69, 19), (244, 164, 96))
                font1 = pygame.freetype.Font('fonts/BalooTammudu2-Bold.ttf', 70)
                font1.render_to(WIN, (285, 40), "MENU", (244, 144, 46))
            if num == 2:
                WIN.fill((117, 53, 13))
                self.Cree_Button("          Rejouer", 215, LARGEUR // 2, 320, 50, (139, 69, 19), (244, 164, 96))
                self.Cree_Button("           Quitter", 215, LARGEUR - 150, 320, 50, (139, 69, 19), (244, 164, 96))
                font1 = pygame.freetype.Font('fonts/BalooTammudu2-Bold.ttf', 70)
                font1.render_to(WIN, (210, 40), titre, color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()
            pygame.time.Clock().tick(60)
            if constantes.run:
                break

    def Cree_Button(self, msg, x, y, width, height, hoverColor, defaultColor):
        '''
           :param: msg affiché, x, y, width bouton, height bouton, couleur qu'on survole sur un bouton, couleur par défaut
           :return: Aucune valeur
           :complexity: O(1)
           cette méthode a pour role de créer un bouton
        '''
        Souris = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed(3)
        font = pygame.freetype.Font('fonts/BalooTammudu2-Bold.ttf', 30)
        if x + width > Souris[0] > x and y + height > Souris[1] > y:
            pygame.draw.rect(WIN, hoverColor, (x, y, width, height), border_radius=25)
            font.render_to(WIN, (x + 50, y + 12), msg, (244, 164, 96))

            if clique[0] == 1 and msg == "Demarrer le jeu":
                constantes.run = True
                constantes.rejouer = False
                mixer.Sound('audio/audio2.wav').play()
                mixer.music.pause()
            if clique[0] == 1 and re.search(".*Quitter", msg):
                mixer.Sound('audio/audio2.wav').play()
                pygame.time.delay(500) # on a met cette ligne pour entendre le son du boutton quitter
                pygame.quit()
            if clique[0] == 1 and re.search(".*Rejouer", msg):
                constantes.run = True
                constantes.rejouer = True
                mixer.Sound('audio/audio2.wav').play()
                mixer.music.pause()

        else:
            pygame.draw.rect(WIN, defaultColor, (x, y, width, height), border_radius=25)
            font.render_to(WIN, (x + 50, y + 12), msg, (139, 69, 19))

    def promo_pieces(self,role):
        '''
           :param: role (blanc ou noir)
           :return: Aucune valeur
           :complexity: O(n)
           cette méthode a pour role de créer une fenetre lorsque un pion vient de promoter et le permettre de s'échanger avec une autre pièce de son choix qui est plus importante que lui
        '''
        # creating tkinter window
        root = Tk()
        root.title('Choix de pièces')
        root.geometry("370x80")
        root.eval('tk::PlaceWindow . center')
        if role == 'blanc':
            idx = 0
            photos = []
            for piece in constantes.pieces:
                if piece == 'bR' or piece =='bp':
                    continue
                if piece == 'np':
                    break
                photos.append(PhotoImage(file="images/" + piece + ".png"))
                btn = Button(root, image=photos[idx], command=lambda m=f"{piece}": self.clicker(m, role,root))
                btn.grid(row=0, column=idx, padx=10)
                idx += 1

        elif role =='noir':
            idx = 0
            photos = []
            for piece in constantes.pieces:
                if piece[0] == 'b':
                    continue
                if piece == 'nR' or piece == 'np':
                    continue
                else:
                    photos.append(PhotoImage(file="images/" + piece + ".png"))
                    btn = Button(root, image=photos[idx], command=lambda m=f"{piece}": self.clicker(m,role,root))
                    btn.grid(row=0, column=idx, padx=10)
                    idx += 1
        mainloop()

    def clicker(self,piece,role,root):
        '''
           :param: piece choisie, role (blanc ou noir), la fenetre de choix
           :return: Aucune valeur
           :complexity: O(1)
           cette méthode a pour role d'assigner quelle pièce a été choisi quand un pion réalise une promotion aussi de fermer la fenetre du choix
        '''
        if role == 'blanc':
            self.promotion_piece_blanc = piece
        else:
            self.promotion_piece_noir = piece
        root.destroy()

