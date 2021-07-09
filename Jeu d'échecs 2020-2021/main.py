import pygame
import sys
from pygame import mixer
import constantes
from interface import Echiquier
from constantes import MAX_FPS, CARRE, WIN
from jeu import Jeu
from jeu import Mouvement
pygame.display.set_caption('Jeu d\'échecs')

def main():
    pygame.init()
    clock = pygame.time.Clock()
    jeu = Jeu()
    echiquier = Echiquier()
    jeu.generer_mvmnts_possibles()
    mixer.music.load('audio/Charlie Chaplin - Chess Music.wav')
    mixer.music.play(-1)
    mvmnt_effectue = False
    case_selectionnee = () # (ligne, colonne) les coordonnees de la case selectionnee dans l'echiquier. Aucune case n'est selectionnee au depart
    cliques_joueur = [] # [ coord. 1ere clique, coord. 2eme clique ] exp: [src:(6,3), dest:(4,3) ]
    echiquier.S_Menu(1,(244, 144, 46),"MENU")
    def highlight():
        if case_selectionnee != ():
            (l,c) = case_selectionnee
            if (jeu.echiquier.echiquier[l][c][0] == 'b' and jeu.role_du_blanc) or (jeu.echiquier.echiquier[l][c][0] == 'n' and not jeu.role_du_blanc) :
                s = pygame.Surface((CARRE,CARRE))
                s.set_alpha(100) # l'eclairage
                s.fill(pygame.Color('blue'))
                WIN.blit(s,(c*CARRE++120,l*CARRE+168))
                s.fill(pygame.Color('yellow'))
                for move in jeu.seulement_mvmnts_valides():
                    if move.ligne_dep == l and move.colonne_dep == c :
                        WIN.blit(s,(move.colonne_arv*CARRE+120,move.ligne_arv*CARRE+168))
    while constantes.run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                constantes.run = False
        #cliques de la souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()  # coordonees de la clique sur la fenetre du jeu
                # determiner la coord de la case (de l'echiquier) selectionnee a partir de position
                if (120 <= position[0] <= 512 + 120) and (168 <= position[1] <= 512 + 168):
                    colonne = (position[0] - 120) // CARRE
                    ligne = (position[1] - 168) // CARRE

                    if case_selectionnee == (
                    ligne, colonne):  # deselectionner, si le joueur clique sur la meme case 2 fois
                        case_selectionnee = ()
                        cliques_joueur = []
                    else:
                        case_selectionnee = (ligne, colonne)
                        cliques_joueur.append(case_selectionnee)  # ajouter la 1ere et la 2eme clique a cliques_jouer
                    if len(cliques_joueur) == 2:  # apres la 2eme clique
                        case_init = cliques_joueur[0]
                        case_fin = cliques_joueur[1]
                        mvmnt = Mouvement(case_init, case_fin, jeu.echiquier.echiquier)
                        if mvmnt in jeu.seulement_mvmnts_valides():  # la condition qu'on va mettre ici va donner true si le mouvement est valid, c-a-d si la liste des cliques appartient a les mouvements valides
                            # reinitialiser les cliques apres avoir effectuer le movement
                            jeu.piece_colectee(mvmnt)
                            jeu.effectuer_mvmnt(mvmnt)
                            mvmnt_effectue = True
                            jeu.verifier_promotion()
                            jeu.vainqueur()
                            if jeu.vectoire == True:
                                mixer.Sound("audio/audio3.wav").play()
                                if not jeu.role_du_blanc:
                                    print("white")
                                    constantes.run = False
                                    echiquier.S_Menu(2, (255, 255, 255), "Blanc gagne !")
                                else:
                                    print("black")
                                    constantes.run = False
                                    echiquier.S_Menu(2, (0, 0, 0), "Noir gagne !")
                                jeu.vectoire = False
                            case_selectionnee = ()
                            cliques_joueur = []
                            son_de_deplacement = mixer.Sound('audio/audio1.wav')
                            son_de_deplacement.play()
                        else:
                            cliques_joueur = [case_selectionnee]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    last_move = jeu.annuller_mvmnt()
                    if(last_move!=0):
                        if (last_move.piece_capturee != '__'):
                            constantes.piece_collectee[last_move.piece_capturee] -= 1
                        mvmnt_effectue = True
        if mvmnt_effectue:
            jeu.generer_mvmnts_possibles()
            mvmnt_effectue = False
        jeu.mettre_a_jour_echiquier()  # redessiner l'echiquier apres avoir effectuer un mouvement
        if constantes.rejouer:
            jeu.initialiser_mvmnt()
            constantes.piece_collectee = {'bp': 0, 'bT': 0, 'bC': 0, 'bF': 0,
                                'bD': 0, 'bK': 0, 'np': 0, 'nT': 0, 'nC': 0, 'nF': 0, 'nD': 0, 'nK': 0}
            constantes.rejouer = False
        highlight()
        clock.tick(MAX_FPS)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


main()
