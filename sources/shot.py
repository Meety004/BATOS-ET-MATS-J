import math
import pygame
import ressources as res

class Shot:
    def __init__(self, x, y, angle, distance_max, img, tireur, canons, inraged, tupleScreen):
        self.x = x
        self.y = y
        self.position_initiale_x = x
        self.position_initiale_y = y
        self.width = 32
        self.height = 32
        self.angle = angle
        self.vitesse = 9
        self.distance_max = distance_max
        image = pygame.image.load(img)
        self.image = pygame.transform.scale(image, (self.width, self.height)).convert_alpha()
        self.ID_tireur = tireur
        self.canons = canons
        self.screen_width = tupleScreen[0]
        self.screen_height = tupleScreen[1]

        #On change les caractéristiques des canons en fonction de l'équipement

        if self.canons == "Canon en argent":
            self.vitesse = self.vitesse * 1.05
        elif self.canons == "Canon en or":
            self.vitesse = self.vitesse * 1.1
        elif self.canons == "Canon ballistique":
            self.distance_max = self.distance_max * 2
        elif self.canons == "Canon légendaire":
            self.vitesse = self.vitesse * 1.15
        elif self.canons == "Canons Rouillés":
            self.vitesse = self.vitesse * 0.85

        self.inraged = inraged

    # le boulet avance
    def avancer(self, liste_navire):
        bateaux_in_range = []
        bateau_proche = None
        for i in range(len(liste_navire)):
            if res.calc_distance(self.x, self.y, liste_navire[i].position_x(), liste_navire[i].position_y()) <= 40 and self.ID_tireur != liste_navire[i].ID:
                bateaux_in_range.append((liste_navire[i], res.calc_distance(self.x, self.y, liste_navire[i].position_x(), liste_navire[i].position_y())))
        if len(bateaux_in_range) > 0:
            bateau_proche = bateaux_in_range[0]
        if bateau_proche is not None:
            for i in range(len(bateaux_in_range)):
                if bateaux_in_range[i][1] > bateau_proche[1]:
                    bateau_proche = bateaux_in_range[i]

        if bateau_proche is not None:
            if self.x > bateau_proche[0].x:
                self.x -= self.vitesse
            else:
                self.x += self.vitesse
            if self.y > bateau_proche[0].y:
                self.y -= self.vitesse
            else:
                self.y += self.vitesse
        else:
            self.x += self.vitesse * math.cos(math.radians(self.angle - 90))
            self.y += self.vitesse * math.sin(math.radians(self.angle - 90))


    
    def collision(self, cible_x, cible_y, cible_ID):
        # verifie si le boulet de canon est dans le bateau pour les x (on calcule par rapport a l'inclinaison du bateau aussi)
        if cible_ID != self.ID_tireur:
            if (cible_x - 15) < self.x < (cible_x + 15) and (cible_y - 15) < self.y < (cible_y + 15):
                return True
        return False
    
    # si la distance parcouru par le boulet est trop grande il despawn    
    def despawn_distance(self):
        return res.calc_distance(self.x, self.y, self.position_initiale_x, self.position_initiale_y) >= self.distance_max
    
    
    # affiche le boulet
    def afficher(self, screen):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)

    def getIDTireur(self):
        return self.ID_tireur

    def is_inraged(self):
        return self.inraged
    

    def sortir_ecran(self):
        if self.x > self.screen_width:
            self.x = 0
        if self.x < 0:
            self.x = self.screen_width
        if self.y > self.screen_height + 20:
            self.y = 0
        if self.y < 0:
            self.y = self.screen_height