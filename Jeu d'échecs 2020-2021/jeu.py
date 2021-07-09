
from interface import Echiquier
import constantes
class Jeu:
    def __init__(self):
        self.echiquier = Echiquier() # instancier l'echiquier
        self.role_du_blanc = True # pour le role du joueur, au depart blanc qui va commencer
        self.mvmnts_valides = [] # les mouvements valides de tous les pieces
        self.mvmnts_historique = []  # un tableau qui contient tout les movements effuctues
        # un dictionnaire qui regroupe tous les fonctions qui generent les mouvements valides selon la cle qui indique le type de la piece
        # pour simplifier l'appel fonctionnel dans  generer_mvmnt_possibles()
        self.fonction_m = {'p': self.pion_mvmnts, 'C': self.cavalier_mvmnts, 'D': self.dame_mvmnts,
                           'F': self.fou_mvmnts, 'T': self.tour_mvmnts, 'R': self.roi_mvmnts}
        # les place actuelle du roi blanc et noir
        self.roi_noir = (0, 3) # position du roi noir
        self.roi_blanc = (7, 3) # position du roi blanc
        self.echecmat = False # si il y echec-mat
        self.vectoire = False # si qlq un gagne la partie
        self.blanc_promotion=False # si un pion blanc peut faire la promotion
        self.noir_promotion=False # si un pion noir peut faire la promotion


    def mettre_a_jour_echiquier(self): # faire l'appelle a la fonction dessiner
        self.echiquier.dessiner()


    def effectuer_mvmnt(self, mvmnt): # effectuer le mouvement en effectant le changement dans la matrice de l'echiquier
        self.echiquier.echiquier[mvmnt.ligne_dep][mvmnt.colonne_dep] = "__"
        self.echiquier.echiquier[mvmnt.ligne_arv][mvmnt.colonne_arv] = mvmnt.piece_boujee
        self.mvmnts_historique.append(mvmnt)
        self.role_du_blanc = not self.role_du_blanc  # permutter les roles
        # la nouvelle place du roi
        if (mvmnt.piece_boujee == "nR"):
            self.roi_noir = (mvmnt.ligne_arv, mvmnt.colonne_arv)
        elif (mvmnt.piece_boujee == "bR"):
            self.roi_blanc = (mvmnt.ligne_arv, mvmnt.colonne_arv)

    def seulement_mvmnts_valides(self):# les movement pouvent effuctuer en traitent les cas partuculier
        mvmnt = self.generer_mvmnts_possibles()
        for i in range(len(mvmnt) - 1, -1, -1): # filtrer les mouvements sauf ceux qui vont faire sortir le roi de l'echec
            self.effectuer_mvmnt(mvmnt[i])
            if self.dans_l_echec():
                mvmnt.remove(mvmnt[i])
            self.annuller_mvmnt()
        return mvmnt

    def dans_l_echec(self): # tester si le roi est attaque
        if (not self.role_du_blanc):
            return self.carre_sous_attack(self.roi_blanc[0], self.roi_blanc[1])
        elif self.role_du_blanc:
            return self.carre_sous_attack(self.roi_noir[0], self.roi_noir[1])

    def vainqueur(self): # determiner si un joueur gagne la partie
        mvmnt = self.seulement_mvmnts_valides()
        if len(mvmnt) == 0 :
            self.vectoire = True

    def carre_sous_attack(self, l, c): # tester si une case est attaquee
        adv_mvmnts = self.generer_mvmnts_possibles()
        for mvmnt in adv_mvmnts:
            if (mvmnt.ligne_arv == l and mvmnt.colonne_arv == c):
                return True
        return False

    def annuller_mvmnt(self): # revenir au mouvement précedent en supprimant le mouvement actuelle de la liste mvmnt_historique
        if len(self.mvmnts_historique) != 0:
            mvmnt = self.mvmnts_historique.pop()
            self.echiquier.echiquier[mvmnt.ligne_dep][mvmnt.colonne_dep] = mvmnt.piece_boujee
            self.echiquier.echiquier[mvmnt.ligne_arv][mvmnt.colonne_arv] = mvmnt.piece_capturee
            if (mvmnt.piece_boujee == "nR"):
                self.roi_noir = (mvmnt.ligne_dep, mvmnt.colonne_dep)
            elif (mvmnt.piece_boujee == "bR"):
                self.roi_blanc = (mvmnt.ligne_dep, mvmnt.colonne_dep)
            self.role_du_blanc = not self.role_du_blanc
            return mvmnt
        else:
            return 0

    def generer_mvmnts_possibles(self):  # les mouvements possibles
        self.mvmnts_valides = []
        for r in range(len(self.echiquier.echiquier)):  #
            for c in range(len(self.echiquier.echiquier[r])):  #
                role = self.echiquier.echiquier[r][c][0]
                if (role == 'b' and self.role_du_blanc) or (role == 'n' and not self.role_du_blanc):
                    piece = self.echiquier.echiquier[r][c][1]
                    self.fonction_m[piece](r, c, self.mvmnts_valides)
        return self.mvmnts_valides

    def pion_mvmnts(self, l, c, mvmnts):
        if self.role_du_blanc:  # pion blanc mouvements
            if l > 0 and self.echiquier.echiquier[l - 1][c] == "__":  # 1 case en avant
                mvmnts.append(Mouvement((l, c), (l - 1, c), self.echiquier.echiquier))
                if l == 6 and self.echiquier.echiquier[l - 2][c] == "__":  # 2 cases en avant
                    mvmnts.append(Mouvement((l, c), (l - 2, c), self.echiquier.echiquier))

            if c > 0 and l > 0:  # capturer une piece à gauche
                if self.echiquier.echiquier[l - 1][c - 1][0] == 'n':  # piece adverse à capturer
                    mvmnts.append(Mouvement((l, c), (l - 1, c - 1), self.echiquier.echiquier))

            if c < 7 and l > 0:  # capturer une piece à droite
                if self.echiquier.echiquier[l - 1][c + 1][0] == 'n':
                    mvmnts.append(Mouvement((l, c), (l - 1, c + 1), self.echiquier.echiquier))

        else:  # pion noir mouvements
            if l < 7 and self.echiquier.echiquier[l + 1][c] == "__":  # 1 case en avant
                mvmnts.append(Mouvement((l, c), (l + 1, c), self.echiquier.echiquier))
                if l == 1 and self.echiquier.echiquier[l + 2][c] == "__":  # 2 cases en avant
                    mvmnts.append(Mouvement((l, c), (l + 2, c), self.echiquier.echiquier))
            if c > 0 and l < 7:  # capturer une piece à gauche
                if self.echiquier.echiquier[l + 1][c - 1][0] == 'b':  # piece ennemie à capturer
                    mvmnts.append(Mouvement((l, c), (l + 1, c - 1), self.echiquier.echiquier))
            if c < 7 and l < 7:  # capturer une piece à droite
                if self.echiquier.echiquier[l + 1][c + 1][0] == 'b':
                    mvmnts.append(Mouvement((l, c), (l + 1, c + 1), self.echiquier.echiquier))

    def cavalier_mvmnts(self, l, c, mvmnts):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        amie = 'b' if self.role_du_blanc else 'n'
        for direction in directions:
            ligne_arv = l + direction[0]
            colonne_arv = c + direction[1]
            if 0 <= ligne_arv < 8 and 0 <= colonne_arv < 8:
                case_arv = self.echiquier.echiquier[ligne_arv][colonne_arv]
                if case_arv[0] != amie:  # n'est pas une piece amie (case vide ou piece ennemie)
                    mvmnts.append(Mouvement((l, c), (ligne_arv, colonne_arv), self.echiquier.echiquier))

    def fou_mvmnts(self, l, c, mvmnts):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        ennemie = 'n' if self.role_du_blanc else 'b'
        for direction in directions:
            for i in range(1, 8):
                ligne_arv = l + direction[0] * i
                colonne_arv = c + direction[1] * i
                if 0 <= ligne_arv < 8 and 0 <= colonne_arv < 8:
                    case_arv = self.echiquier.echiquier[ligne_arv][colonne_arv]
                    if case_arv == "__":  # case vide
                        mvmnts.append(Mouvement((l, c), (ligne_arv, colonne_arv), self.echiquier.echiquier))
                    elif case_arv[0] == ennemie:  # piece ennemie
                        mvmnts.append(Mouvement((l, c), (ligne_arv, colonne_arv), self.echiquier.echiquier))
                        break
                    else:  # piece amie
                        break
                else:  # hors echiquier
                    break

    def tour_mvmnts(self, l, c, mvmnts):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        ennemie = "n" if self.role_du_blanc else "b"
        for direction in directions:
            for i in range(1, 8):
                ligne_arv = l + direction[0] * i
                colonne_arv = c + direction[1] * i
                if 0 <= ligne_arv < 8 and 0 <= colonne_arv < 8:
                    case_arv = self.echiquier.echiquier[ligne_arv][colonne_arv]
                    if case_arv == "__":  # case vide
                        mvmnts.append(Mouvement((l, c), (ligne_arv, colonne_arv), self.echiquier.echiquier))
                    elif case_arv[0] == ennemie:  # piece ennemie
                        mvmnts.append(Mouvement((l, c), (ligne_arv, colonne_arv), self.echiquier.echiquier))
                        break
                    else:  # piece amie
                        break
                else:  # hors echiquier
                    break

    def dame_mvmnts(self, l, c, mvmnts):
        # les mouvements de la dame = ceux de la tour + ceux du fou
        self.fou_mvmnts(l, c, mvmnts)
        self.tour_mvmnts(l, c, mvmnts)

    def roi_mvmnts(self, l, c, mvmnts):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        amie = 'b' if self.role_du_blanc else 'n'
        for direction in directions:
            ligne_arv = l + direction[0]
            colonne_arv = c + direction[1]
            if 0 <= ligne_arv < 8 and 0 <= colonne_arv < 8:
                case_arv = self.echiquier.echiquier[ligne_arv][colonne_arv]
                if case_arv[0] != amie:  # n'est pas une piece amie (case vide ou piece ennemie)
                    mvmnts.append(Mouvement((l, c), (ligne_arv, colonne_arv), self.echiquier.echiquier))

    def initialiser_mvmnt(self):
        for i in range(len(self.mvmnts_historique)):
            self.annuller_mvmnt()


    def piece_colectee(self,mvmnt): # determiner le type de la piece collectée et augmenter sa valeur.
        if(self.echiquier.echiquier[mvmnt.ligne_arv][mvmnt.colonne_arv] in constantes.piece_collectee):
            constantes.piece_collectee[self.echiquier.echiquier[mvmnt.ligne_arv][mvmnt.colonne_arv]]+=1
            print(constantes.piece_collectee, self.echiquier.echiquier[mvmnt.ligne_arv][mvmnt.colonne_arv])

    def verifier_promotion(self): # verefier que un pion est promoter ou pas
        for i in range(0,8,7):
            for j in range(len(self.echiquier.echiquier[i])):
                if (i==0 and self.echiquier.echiquier[i][j]=='bp'):
                        self.blanc_promotion=True
                        self.obtenir_piece_prom()
                        self.echiquier.echiquier[i][j] = self.echiquier.promotion_piece_blanc

                if (i==7 and self.echiquier.echiquier[i][j]=='np'):
                        self.noir_promotion=True
                        self.obtenir_piece_prom()
                        self.echiquier.echiquier[i][j]= self.echiquier.promotion_piece_noir

    def obtenir_piece_prom(self): # determiner la type de piece que l’utilisateur chiosie l’hors de la promotion
        if self.blanc_promotion:
            self.blanc_promotion=False
            self.echiquier.promo_pieces('blanc')

        if self.noir_promotion:
            self.noir_promotion=False
            self.echiquier.promo_pieces('noir')



class Mouvement:

        def __init__(self, case_init, case_fin, echiquier):
            # extraire la ligne et la colonne de départ
            self.ligne_dep = case_init[0]
            self.colonne_dep = case_init[1]
            # extraire la ligne et la colonne d'arrivee
            self.ligne_arv = case_fin[0]
            self.colonne_arv = case_fin[1]
            # la piece qui est dans la case initiale ex: 'bR'
            self.piece_boujee = echiquier[self.ligne_dep][self.colonne_dep]
            # la piece qui est dans la case finale, elle peut être '__' lorsque la case finale est vide
            self.piece_capturee = echiquier[self.ligne_arv][self.colonne_arv]
            # l'id du mouvement: combinaison des quatre premiers attrributs
            self.mvmnt_id = self.ligne_dep * 1000 + self.colonne_dep * 100 + self.ligne_arv * 10 + self.colonne_arv

        def __eq__(self, autre): # surcharger l'operateur == pour la classe Mouvement, pour que la comparaison se fait par les ids des mouvements
            if isinstance(autre, Mouvement):
                return self.mvmnt_id == autre.mvmnt_id
            return False
