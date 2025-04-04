# Projet: WRECKED OCEAN
# Auteurs: BELLEC-ESCALERA Elliot, CADEAU--FLAUJAT Gabriel, KELEMEN Thomas, GABRIEL TOM


# IMPORTS

# Imports des librairies
import math
import pygame
import random
import string
import os

# Imports des modules
import shot
import ressources as res

# On crée un évènement pour gérer le tir double
tirDouble = pygame.USEREVENT + 1

# Création de la classe Navire qui gère les fonctionnalités de base du joueur et des ennemis
class Navire:
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height, dt, type):
        """
        Constructeur de la classe Navire
        Prend en argument la vitesse max, l'accélération, la maniabilité, l'image du navire, la taille de l'écran et le type du navire
        """
        # Contrôle du vaisseau
        self.vitesse_max = v_max
        self.acceleration = acceleration

        # La position du navire est aléatoire sur la map
        self.x = random.randint(0, screen_width)
        self.y = random.uniform(0, screen_height)
        self.vitesse = 0
        self.angle = 270

        # Vitesse de rotation du navire
        self.maniabilite = maniabilite

        # Type du navire (0 = Joueur; 1 = Ennemi Basique; 2 = Ennemi Chasseur; 3 = Ennemi Intelligent)
        self.type = type

        # On définit une taille différente pour le joueur et les ennemis
        if type == 0:
            self.width = screen_width*0.022
            self.height = screen_height*0.062
        else:
            self.width = screen_width*0.020
            self.height = screen_height*0.064   

        # On définit la taille de l'écran
        self.screen_width = screen_width
        self.screen_height = screen_height

        # On charge et adapte la taille des images des bateaux
        original_image = pygame.image.load(image).convert_alpha()
        original_image = pygame.transform.scale(original_image, (self.width, self.height)).convert_alpha()

        # Image qui sera affichée
        self.image = original_image

        # Le denier tir fait par le bateau
        self.dernier_tir = 0 

        # Durée minimale entre deux tirs (en ms)
        self.cadence_tir = 1000

        # Génération d'un ID aléatoire pour identifier les navires
        self.ID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        # On définit un nombre de PV différents en fonction du type de navire
        if type == 2:
            self.maxVie = 30
        else:
            self.maxVie = 50
        self.vie = self.maxVie

        # On vérifie si l'île contient un malus
        self.verifIleMalus = False

        # Indique si l'interface de choix des équipements est affichée
        self.afficher_items = False  

        # Indique si l'interface de choix des bénédictions est affichée
        self.afficher_benediction = False

        # On charge l'image de l'interface de choix d'item
        self.ItemsUI = pygame.image.load(os.path.join("data", "images", "Interfaces", "equip_menu_item.png")).convert_alpha()
        self.ItemsUI = pygame.transform.scale(self.ItemsUI, (screen_width*0.4, pygame.display.Info().current_h*0.4)).convert_alpha()

        # On charge l'image de l'interface de choix de bénédiction
        self.benedictionUI = pygame.image.load(os.path.join("data", "images", "Interfaces", "equip_menu_bene.png")).convert_alpha()
        self.benedictionUI = pygame.transform.scale(self.benedictionUI, (screen_width*0.4, pygame.display.Info().current_h*0.4)).convert_alpha()
        
        # On donne un équipement de base différent pour les Ennemis Chasseurs qui ne peuvent pas récupérer d'équipement
        if self.type == 2:
            self.equipement = {
            'canons':    "+2 Canons",
            'voile':    "Voile latine",
            'coque':    "Coque épicéa"
            }
        else:
            self.equipement = {
            'canons':    "Canons de base",
            'voile':    "Voile de base",
            'coque':    "Coque de base"
            }

        #On crée une liste qui contient les bénédictions du bateau
        self.benedictions = [None, None]

        # Stocke la récompense de l'île
        self.recompense = None

        # Variables qui contiennent les modificateurs de vie et de vitesse des coques et des voiles
        self.CoqueMaxVie = 0
        self.CoqueMaxVitesse = 1
        self.VoileMaxVie = 0
        self.VoileMaxVitesse = 1

        # Variables qui contiennent les icones pour chaque type d'équipement
        self.iconCoque = res.CoqueCommun
        self.iconCoque = pygame.image.load(self.iconCoque).convert_alpha()
        self.iconCoque = pygame.transform.scale(self.iconCoque, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.iconVoile = res.VoileCommun
        self.iconVoile = pygame.image.load(self.iconVoile).convert_alpha()
        self.iconVoile = pygame.transform.scale(self.iconVoile, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.iconCanon = res.CanonCommun
        self.iconCanon = pygame.image.load(self.iconCanon).convert_alpha()
        self.iconCanon = pygame.transform.scale(self.iconCanon, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        # Image du boulet de canon
        self.imageBoulet = os.path.join("data", "images", "Textures", "Autres", "boulet_canon.png")


        # Variables qui contiennent les chemins des icones s'affichant sur l'interface de choix d'item
        self.DisplayIconNew = None
        self.DisplayIconPast = None

        # On initialise un timer pour les bénédictions à 0 pour qu'elles puissent être utilisées directement
        self.timer_benediction_1 = res.Timer(1)
        self.timer_benediction_2 = res.Timer(1)

        # On définit un cooldown entre chaque utilisation de bénédiction
        self.timer_dash = 15
        self.timer_sante = 20
        self.timer_aura = 30
        self.timer_rage = 30
        self.timer_godmode = 40
        self.timer_giga_tir = 50

        # On définit des variables qui servent à la bénédiction de rage
        self.inraged = False
        self.rage_timer = None
        self.life_before_rage = 0

        # On définit des variables qui servent à la bénédiction d'aura
        self.has_aura = False
        self.aura_timer = None
        self.aura_damage_timer = res.Timer(1)
        self.aura_degat = 1

        # On définit des variables qui servent à la bénédiction de GodMode
        self.godmode = False
        self.godmode_timer = None

        # On définit des variables qui servent à la bénédiction de Projectiles
        self.giga_tir = False
        self.giga_tir_double = False
        self.timer_giga_tir_duree = res.Timer(1)

        # Stocke l'île qui a ouvert l'interface
        self.ile_actuelle = None

        # Variables contenant le nom et la description de l'équipement actuel
        self.TitleTextPast = None
        self.DescriptionTextPast = None

        # Variables contenant le nom et la description de l'équipement trouvé
        self.TitleTextNew = None
        self.DescriptionTextNew = None

        # On définit des polices différentes poue le nom et la description de l'équipement
        self.TitleFont = pygame.font.Font(res.fontPixel, 28)
        self.DescriptionFont = pygame.font.Font(res.fontPixel, 20)

        # Variable pour vérifier si le texte de l'interface des équipements est chargé
        self.text_loaded = False

        # Variables qui définissent la distance max des projectiles
        self.distance_max = screen_height*0.20
        self.distance_maxFront = self.distance_max * 1.8

        # On définit l'écran qui est utilisé
        self.screen = (self.screen_width, self.screen_height)

        # On stocke le type d'équipement qui a été trouvé sur l'île (Voile, Coque, Canon)
        self.typeRec = None

        # Stocke les icones des bénédiction du joueur
        self.iconBenediction1 = None
        self.iconBenediction2 = None

        # Stocke l'icone de la bénédiction qui a été trouvée par le joueur
        self.newBenedictionIcon = None

        # Variables contenant le nom et la description de la bénédiction trouvée
        self.TitleTexteBeneNew = None
        self.DescriptionTextBeneNew = None

        # Variable pour vérifier si le texte  de l'interface des bénédictions est chargé
        self.text_loaded_bene = False

        # On charge toutes les images et on change leur tailles
        self.loadImages()


    # On fait avancer le bateau en fonction de sa vitesse
    def avancer(self):
        """
        Fait avance le navire
        """

        # Si le joueur a activé la bénédiction de rage, il va plus vite
        if self.inraged:
            self.x += self.vitesse * 1.5 * math.cos(math.radians(self.angle - 90)) # Multiplie la vitesse X par le cosinus de l'angle en fonction de l'inclinaison
            self.y += self.vitesse * 1.5 * math.sin(math.radians(self.angle - 90)) # Multiplie la vitesse Y par le cosinus de l'angle en fonction de l'inclinaison
        else:
            self.x += self.vitesse * math.cos(math.radians(self.angle - 90))
            self.y += self.vitesse * math.sin(math.radians(self.angle - 90))


    #On charge toutes les icones et on les rogne pour éviter des ralentissements pendant le jeu
    def loadImages(self):
        """
        Charge les icones des équipements et des bénédictions
        """

        self.CanonMalus = pygame.image.load(res.CanonMalus).convert_alpha()
        self.CanonMalus = pygame.transform.scale(self.CanonMalus, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileMalus = pygame.image.load(res.VoileMalus).convert_alpha()
        self.VoileMalus = pygame.transform.scale(self.VoileMalus, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueMalus = pygame.image.load(res.CoqueMalus).convert_alpha()
        self.CoqueMalus = pygame.transform.scale(self.CoqueMalus, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CanonCommun = pygame.image.load(res.CanonCommun).convert_alpha()
        self.CanonCommun = pygame.transform.scale(self.CanonCommun, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CanonRare = pygame.image.load(res.CanonRare).convert_alpha()
        self.CanonRare = pygame.transform.scale(self.CanonRare, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CanonMythique = pygame.image.load(res.CanonMythique).convert_alpha()
        self.CanonMythique = pygame.transform.scale(self.CanonMythique, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CanonLegendaire = pygame.image.load(res.CanonLegendaire).convert_alpha()
        self.CanonLegendaire = pygame.transform.scale(self.CanonLegendaire, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileCommun = pygame.image.load(res.VoileCommun).convert_alpha()
        self.VoileCommun = pygame.transform.scale(self.VoileCommun, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileRare = pygame.image.load(res.VoileRare).convert_alpha()
        self.VoileRare = pygame.transform.scale(self.VoileRare, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileMythique = pygame.image.load(res.VoileMythique).convert_alpha()
        self.VoileMythique = pygame.transform.scale(self.VoileMythique, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileLegendaire = pygame.image.load(res.VoileLegendaire).convert_alpha()
        self.VoileLegendaire = pygame.transform.scale(self.VoileLegendaire, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueCommun = pygame.image.load(res.CoqueCommun).convert_alpha()
        self.CoqueCommun = pygame.transform.scale(self.CoqueCommun, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueRare = pygame.image.load(res.CoqueRare).convert_alpha()
        self.CoqueRare = pygame.transform.scale(self.CoqueRare, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueMythique = pygame.image.load(res.CoqueMythique).convert_alpha()
        self.CoqueMythique = pygame.transform.scale(self.CoqueMythique, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueLegendaire = pygame.image.load(res.CoqueLegendaire).convert_alpha()
        self.CoqueLegendaire = pygame.transform.scale(self.CoqueLegendaire, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Dash = pygame.image.load(res.BeneDash).convert_alpha()
        self.Dash = pygame.transform.scale(self.Dash, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Aura = pygame.image.load(res.BeneAura).convert_alpha()
        self.Aura = pygame.transform.scale(self.Aura, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.GodMode = pygame.image.load(res.BeneGodMode).convert_alpha()
        self.GodMode = pygame.transform.scale(self.GodMode, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Projectiles = pygame.image.load(res.BeneProjectiles).convert_alpha()
        self.Projectiles = pygame.transform.scale(self.Projectiles, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Rage = pygame.image.load(res.BeneRage).convert_alpha()
        self.Rage = pygame.transform.scale(self.Rage, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Sante = pygame.image.load(res.BeneSante).convert_alpha()
        self.Sante = pygame.transform.scale(self.Sante, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

    # Augmente la vitessse
    def accelerer(self):
        """
        Augmente la vitesse du navire
        """

        # Accelere tant que la vitesse max n'est pas atteinte
        if self.vitesse < self.vitesse_max:
            self.vitesse += self.acceleration
            
        # Si la vitesse max est atteinte il revient à la vitesse max
        if self.vitesse > self.vitesse_max:
            self.vitesse = self.vitesse_max

    # Si il arrete d'avancer le bateau décelère
    def ralentit(self):
        """
        Diminue la vitesse du navire
        """

        # Ralentit tant que la vitesse n'est pas nulle
        if self.vitesse > 0:
            self.vitesse -= ( 0.15 - self.vitesse_max/100)

        # Revient à 0 si la vitesse est négative
        if self.vitesse < 0:
            self.vitesse = 0

    # On gère la rotation vers la gauche du bateau
    def tourne_gauche(self):
        """
        Fait tourner le navire à gauche
        """
        if self.vitesse > 0:
            self.angle -= self.maniabilite

            # Si l'angle est inférieur à 0, on lui rajoute 360 pour qu'il reste toujours entre 0 et 360
            if self.angle < 0:
                self.angle += 360

    # On gère la rotation vers la droite du bateau
    def tourne_droite(self):
        """
        Fait tourner le navire à droite
        """
        if self.vitesse > 0:
            self.angle += self.maniabilite

            # Si l'angle est superieur à 360, on lui enlève 360 pour qu'il reste toujours entre 0 et 360
            if self.angle >= 360:
                self.angle -= 360

    # Pour que le bateau ne sorte pas de l'ecran et revienne de l'autre côté
    def sortir_ecran(self, longueur_ecran, hauteur_ecran):
        """
        Gère la sortie d'écran des navires
        Arguments: screen_width, screen_height
        """
        if self.x > longueur_ecran:
            self.x = 0
        if self.x < 0:
            self.x = longueur_ecran
        if self.y > hauteur_ecran:
            self.y = 0
        if self.y < 0:
            self.y = hauteur_ecran

    def afficher(self, screen):
        """
        Affiche le bateau à l'écran
        Arguments: screen
        """
        # Appliquer la rotation à l'image d'origine sans la modifier définitivement
        rotated_image = pygame.transform.rotate(self.image, -self.angle).convert_alpha()
        rect = rotated_image.get_rect(center=(self.x, self.y))
        self.rect = rect

        # On affiche le bateau à l'écran
        screen.blit(rotated_image, self.rect)

    def shoot(self):
        """
        Gère les tirs du navire
        """
        # Vérifie si le canon a rechargé
        if pygame.time.get_ticks() - self.dernier_tir >= self.cadence_tir:
            self.dernier_tir = pygame.time.get_ticks()

            # On stocke les tirs du navire
            liste_tirs = []
            
            # Par défaut, le bateau tire à droite et à gauche
            if not self.giga_tir:
                tir_droite = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_droite, self.equipement['canons']))

                tir_gauche = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_gauche, self.equipement['canons']))

            # On ajoute un tir à l'avant du bateau
            if self.equipement['canons'] == '+1 Canon' or self.equipement['canons'] == '+2 Canons' or self.equipement['canons'] == '+4 Canons' or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir):
                if self.vitesse != 0:
                    tir_avant = shot.Shot(self.x, self.y, self.angle, self.distance_maxFront, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                else:
                    tir_avant = shot.Shot(self.x, self.y, self.angle, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_avant, self.equipement['canons']))

            # On ajoute un tir à l'arrière du bateau
            if self.equipement['canons'] == '+2 Canons' or self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons' or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir):
                tir_arriere = shot.Shot(self.x, self.y, self.angle + 180, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_arriere, self.equipement['canons']))

            # On ajoute un tir en diagonale avant droite
            if self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons' or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir):
                tir_diag1 = shot.Shot(self.x, self.y, self.angle + 30, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag1, self.equipement['canons']))

            # On ajoute un tir en diagonale avant gauche
            if self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons' or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir):
                tir_diag2 = shot.Shot(self.x, self.y, self.angle - 30, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag2, self.equipement['canons']))

            # On ajoute une multitude de tirs si la bénédiction projectile est activée
            if "Bénédiction Projectiles" in self.benedictions and self.giga_tir:
                tir_diag3 = shot.Shot(self.x, self.y, self.angle + 225, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag3, self.equipement['canons']))
                tir_diag4 = shot.Shot(self.x, self.y, self.angle - 225, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag4, self.equipement['canons']))
                tir_droite = shot.Shot(self.x, self.y, self.angle + 90, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_droite, self.equipement['canons']))
                tir_gauche = shot.Shot(self.x, self.y, self.angle - 90, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_gauche, self.equipement['canons']))

            # On appelle un timer pour gérer le tir double
            if self.equipement['canons'] == "Canon à tirs doubles" or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir_double): 
                pygame.time.set_timer(tirDouble, 70, loops=1)

            # On renvoie la liste avec tous les tirs du bateau
            return liste_tirs
        
    # On fait un deuxième tir lorsque le timer est fini
    def GererEventTir(self, event, liste_tirs):
        """
        Gère le tir double
        Argument: event, liste_tirs
        """

        if event.type == tirDouble and (self.equipement["canons"] == "Canon à tirs doubles" or self.giga_tir_double):
            
            # Si le navire a un canon à tirs doubles, on fait un deuxième tir à gauche et à droite
            tir_droiteD = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
            liste_tirs.append((tir_droiteD, self.equipement['canons']))

            tir_gaucheD = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
            liste_tirs.append((tir_gaucheD, self.equipement['canons']))

            # Si le navire a la bénédiction projectiles activée, on fait un deuxième tir partout autour
            if ("Bénédiction Projectiles" in self.benedictions and self.giga_tir_double):
                tir_avantD = shot.Shot(self.x, self.y, self.angle, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_avantD, self.equipement['canons']))
                tir_arriereD = shot.Shot(self.x, self.y, self.angle + 180, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_arriereD, self.equipement['canons']))
                tir_diag1D = shot.Shot(self.x, self.y, self.angle + 45, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag1D, self.equipement['canons']))
                tir_diag2D = shot.Shot(self.x, self.y, self.angle - 45, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag2D, self.equipement['canons']))
                tir_diag3D = shot.Shot(self.x, self.y, self.angle + 225, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag3D, self.equipement['canons']))
                tir_diag4D = shot.Shot(self.x, self.y, self.angle - 225, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag4D, self.equipement['canons']))
        
    # On gère les dégats
    def get_damaged(self, damage):
        """
        Fait des dégats au navire touché
        Argument: damage
        """
        r = None

        # Si le navire a la coque en bois magique, il y a 20% de chance de ne pas prendre de dégat
        if self.equipement['coque'] == "Coque en bois magique":
            r = random.randint(1,5)
        
        # On ne prend pas non plus de dégat si la bénédiction godmode est activée
        if r != 1 and not self.godmode:
                self.vie -= damage
    
    # On vérifie si le navire est en vie
    def is_dead(self):
        """
        Vérifie si le navire n'a plus de vie
        """
        if self.vie <= 0:
            return True
        return False

    # On renvoie différentes caractéristiques de la classe

    def position_x(self):
        """
        Renvoie l'ordonnée du navire
        """
        return self.x

    def position_y(self):
        """
        Renvoie l'abscisse du navire
        """
        return self.y

    def get_width(self):
        """
        Renvoie la longueur de l'écran
        """
        return self.width
    
    def get_height(self):
        """
        Renvoie la hauteur de l'écran
        """
        return self.height

    def get_angle(self):
        """
        Renvoie l'angle de rotation du navire
        """
        return self.angle

    def get_ID(self):
        """
        Renvoie l'ID du navire
        """
        return self.ID

    def get_rect(self):
        """
        Renvoie le rect du navire
        """
        return self.rect

    def get_vie(self):
        """
        Renvoie la vie du navire
        """
        return self.vie

    def get_max_vie(self):
        """
        Renvoie la vie max du navire
        """
        return self.maxVie

    def get_speed(self):
        """
        Renvoie la vitesse du navire
        """
        return self.vitesse

    def get_max_speed(self):
        """
        Renvoie la vitesse max du navire
        """
        return self.vitesse_max

    def get_maniabilite(self):
        """
        Renvoie la maniabilité du navire
        """
        return self.maniabilite

    def get_cadence_tir(self):
        """
        Renvoie la cadence de tir du navire
        """
        return self.cadence_tir

    def get_benedictions(self):
        """
        Renvoie la liste des bénédictions du navire
        """
        return self.benedictions

    def getEquipement(self):
        """
        Renvoie le dictionnaire des équipements du navire
        """
        return self.equipement

    def getPastDisplay(self):
        """
        Renvoie l'icone de l'équipement actuel
        """
        return self.DisplayIconPast

    def getNewDisplay(self):
        """
        Renvoie l'icone de l'équipement qui a été trouvé
        """
        return self.DisplayIconNew

    def getItemUI(self):
        """
        Renvoie l'image d'interface de choix d'équipement
        """
        return self.ItemsUI

    def getBenedictionUI(self):
        """
        Renvoie l'image d'interface de choix de bénédiction
        """
        return self.benedictionUI

    def getTitleTextPast(self):
        """
        Renvoie le nom de l'équipement actuel
        """
        return self.TitleTextPast

    def getDescriptionTextPast(self):
        """
        Renvoie la description de l'équipement actuel
        """
        return self.DescriptionTextPast

    def getTitleTextNew(self):
        """
        Renvoie le nom de l'équipement qui a été trouvé
        """
        return self.TitleTextNew

    def getDescriptionTextNew(self):
        """
        Renvoie la description de l'équipement qui a été trouvé
        """
        return self.DescriptionTextNew

    def getImages(self):
        """
        Renvoie les icones de la voile, de la coque, et du canon actuels
        """
        return self.iconCoque, self.iconVoile, self.iconCanon

    def getBenedictionsImages(self):
        """
        Renvoie les icones des bénédicitons à afficher
        """
        return self.newBenedictionIcon, self.iconBenediction1, self.iconBenediction2

    def getBenedictionsTexts(self):
        """
        Renvoie les noms et descriptions des bénédictions à afficher
        """
        return self.benedictions[0], self.benedictions[1], self.TitleTexteBeneNew, self.DescriptionTextBeneNew
    
    def is_giga_tir(self):
        """
        Renvoie l'état de la bénédiction projectiles
        """
        return self.giga_tir
    
    def is_inrage(self):
        """
        Renvoie l'état de la bénédiction de rage
        """
        return self.inraged
    
    def aura_active(self):
        """
        Renvoie l'état de la bénédiction d'aura
        """
        return self.has_aura
    
    def godmode_active(self):
        """
        Renvoie l'état de la bénédiction de GodMode
        """
        return self.godmode
    
    # On charge le texte de l'interface des équipements si ce n'est pas déjà le cas
    def LoadText(self):
        """
        Met à jour les textes à afficher sur l'interface de choix des équipements
        """
        if not isinstance(self.TitleTextPast, pygame.Surface):
            self.TitleTextPast = self.TitleFont.render(self.equipement[self.typeRec], True, (0, 0, 0))
        if not isinstance(self.DescriptionTextPast, pygame.Surface):
            equip = self.equipement[self.typeRec]
            self.DescriptionTextPast = self.DescriptionFont.render(res.dictItemsBuff[equip], True, (0, 0, 0))

        if not isinstance(self.TitleTextNew, pygame.Surface):
            self.TitleTextNew = self.TitleFont.render(self.recompense[0], True, (0, 0, 0))
        if not isinstance(self.DescriptionTextNew, pygame.Surface):
            equip = self.recompense[0]
            self.DescriptionTextNew = self.DescriptionFont.render(res.dictItemsBuff[equip], True, (0, 0, 0))

    # On charge le texte de l'interface des bénédictions
    def LoadTextBene(self):
        """
        Met à jour les textes à afficher sur l'interface de choix des bénédictions
        """
        self.TitleTexteBeneNew = self.TitleFont.render(self.recompense[0], True, (0, 0, 0))
        benediction = self.recompense[0]
        self.DescriptionTextBeneNew = self.DescriptionFont.render(res.dictBenedictionsBuff[benediction], True, (0, 0, 0))

    # On vérifie si l'île existe, sinon on met toutes les variables d'affichage à zéro.
    def verifIleExiste(self, liste_iles):
        """
        Vérifie si l'ile existe encore
        Argument: liste_iles
        """
        if (self.ile_actuelle is not None) and (self.ile_actuelle not in liste_iles):
            self.afficher_benediction = False
            self.afficher_items = False
            self.text_loaded = False
            self.ile_actuelle = None

    # On gère l'affichage de l'interface de choix des équipements
    def equipInterface(self, recompense, xIle, yIle, ile):
        """
        Gère l'affichage de l'interface de choix des équipements
        Arguments: recompense, xIle, yIle, ile
        """
        self.recompense = recompense

        # On change le type d'équipement
        if self.recompense[0] in res.listeCanons:
            self.typeRec = "canons"
        elif self.recompense[0] in res.listeVoiles:
            self.typeRec = "voile"
        elif self.recompense[0] in res.listeCoques:
            self.typeRec = "coque"

        # On vérifie si la navire est dans un rayon de 75 d'une ile
        if res.calc_distance(self.x, self.y, xIle, yIle) <= 75:

            # Si la récompense est un équipement
            if (self.recompense[0] not in res.liste_benedictions) and (self.recompense[0] not in res.liste_malus):

                # Si l'interface n'est pas affichée, ou si on s'approche d'une nouvelle île
                if not self.afficher_items or self.ile_actuelle is None:
                    
                    # Si l'ile qui a ouvert l'interface n'est pas l'ile sur laquelle se trouve le bateau
                    if self.ile_actuelle != ile:
                        self.afficher_items = False
                        self.text_loaded = False
                        self.TitleTextPast = None
                        self.DescriptionTextPast = None
                        self.TitleTextNew = None
                        self.DescriptionTextNew = None
                        self.ile_actuelle = ile
                    
                    # On met à jour les icones et les textes affichés 
                    self.updateDisplayIconItem()
                    self.LoadText()
                    self.text_loaded = True
                    # On mémorise l'île qui a ouvert l'interface
                    self.ile_actuelle = ile

                # On garde en mémoire l'ouverture de l'interface
                self.afficher_items = True

            # Si la récompense est un malus, on met à jour les icones et on équipe directement le malus
            elif self.recompense[0] in res.liste_malus:
                self.updateDisplayIconItem()
                self.equiper()
                self.verifIleMalus = True
        
        # Si on est pas dans le rayon de 75, on oublie les variables liées à l'ile
        elif self.recompense[0] not in res.liste_benedictions and self.recompense[0] not in res.liste_malus and self.ile_actuelle == ile:
                self.afficher_items = False
                self.text_loaded = False
                self.ile_actuelle = None

    # On gère l'affichage de l'interface de choix des bénédictions    
    def beneInterface(self, xIle, yIle, ile):
        """
        Gère l'affichage de l'interface de choix des bénédictions
        Arguments: xIle, yIle, ile
        """

        # On vérifie si la navire est dans un rayon de 75 d'une ile
        if res.calc_distance(self.x, self.y, xIle, yIle) <= 75:
            if self.recompense[0] in res.liste_benedictions:

                # Si l'interface n'est pas affichée, ou si on s'approche d'une nouvelle île
                if not self.afficher_benediction or self.ile_actuelle is None:

                    # Si l'ile qui a ouvert l'interface n'est pas l'ile sur laquelle se trouve le bateau
                    if self.ile_actuelle != ile:
                        self.afficher_benediction = False
                        self.text_loaded_bene = False
                        self.TitleTexteBeneNew = None
                        self.DescriptionTextBeneNew = None
                        self.ile_actuelle = ile

                    # On met à jour les icones et les textes affichés
                    self.updateDisplayIconBene()
                    self.LoadTextBene()
                    self.text_loaded_bene = True
                    # On mémorise l'île qui a ouvert l'interface
                    self.ile_actuelle = ile
                
                # On garde en mémoire l'ouverture de l'interface
                self.afficher_benediction = True

        # Si on est pas dans le rayon de 75, on oublie les variables liées à l'ile
        elif self.recompense[0] in res.liste_benedictions and self.ile_actuelle == ile:
            self.afficher_benediction = False
            self.text_loaded_bene = False
            self.ile_actuelle = None
            

    # On met à jour les icones à afficher en fonction du type d'équipement sur l'ile  
    def updateDisplayIconItem(self):
        """
        Met à jour les icones d'équipement à afficher
        """
        
        # Si l'équipement est un canon, on affiche le canon actuel du joueur
        if self.recompense[0] in res.listeCanons:
            self.DisplayIconPast = self.iconCanon
            if self.recompense[1] == "commun":
                self.DisplayIconNew = self.CanonCommun
            elif self.recompense[1] == "rare":
                self.DisplayIconNew = self.CanonRare
            elif self.recompense[1] == "mythique":
                self.DisplayIconNew = self.CanonMythique
            elif self.recompense[1] == "légendaire":
                self.DisplayIconNew = self.CanonLegendaire
        
        # Si l'équipement est une coque, on affiche la coque actuelle du joueur
        elif self.recompense[0] in res.listeCoques:
            self.DisplayIconPast = self.iconCoque
            if self.recompense[1] == "commun":
                self.DisplayIconNew = self.CoqueCommun
            elif self.recompense[1] == "rare":
                self.DisplayIconNew = self.CoqueRare
            elif self.recompense[1] == "mythique":
                self.DisplayIconNew = self.CoqueMythique
            elif self.recompense[1] == "légendaire":
                self.DisplayIconNew = self.CoqueLegendaire

        # Si l'équipement est une voile, on affiche la voile actuelle du joueur
        elif self.recompense[0] in res.listeVoiles:
            self.DisplayIconPast = self.iconVoile
            if self.recompense[1] == "commun":
                self.DisplayIconNew = self.VoileCommun
            elif self.recompense[1] == "rare":
                self.DisplayIconNew = self.VoileRare
            elif self.recompense[1] == "mythique":
                self.DisplayIconNew = self.VoileMythique
            elif self.recompense[1] == "légendaire":
                self.DisplayIconNew = self.VoileLegendaire
        
        # Si l'équipement est un malus, on met à jour l'icone
        elif self.recompense[0] in res.liste_malus:
            if self.recompense[0] == res.liste_malus[0]:
                self.DisplayIconPast = self.iconCanon
                self.DisplayIconNew = self.CanonMalus
            elif self.recompense[0] == res.liste_malus[1]:
                self.DisplayIconPast = self.iconVoile
                self.DisplayIconNew = self.VoileMalus
            elif self.recompense[0] == res.liste_malus[2]:
                self.DisplayIconPast = self.iconCoque
                self.DisplayIconNew = self.CoqueMalus

    # On met à jour les icones de bénédiction à afficher sur l'interface de choix des bénédictions
    def updateDisplayIconBene(self):
        """
        Met à jour les icones de bénédiction à afficher
        """

        if self.recompense[0] == "Bénédiction Dash":
            self.newBenedictionIcon = self.Dash
        elif self.recompense[0] == "Bénédiction d'aura":
            self.newBenedictionIcon = self.Aura
        elif self.recompense[0] == "Bénédiction GodMode":
            self.newBenedictionIcon = self.GodMode
        elif self.recompense[0] == "Bénédiction Projectiles":
            self.newBenedictionIcon = self.Projectiles
        elif self.recompense[0] == "Bénédiction de rage":
            self.newBenedictionIcon = self.Rage
        elif self.recompense[0] == "Bénédiction Santé":
            self.newBenedictionIcon = self.Sante

    # Mettre à jour l'équipement en fonction de la récompense
    def equiper(self):
        """
        Met à jour l'équipement du type de celui trouvé sur l'ile
        """

        if self.recompense[0] in res.listeCanons or self.recompense[0] == res.liste_malus[0]:
            self.equipement['canons'] = self.recompense[0]
        elif self.recompense[0] in res.listeVoiles or self.recompense[0] == res.liste_malus[1]:
            self.equipement['voile'] = self.recompense[0]
        elif self.recompense[0] in res.listeCoques or self.recompense[0] == res.liste_malus[2]:
            self.equipement['coque'] = self.recompense[0]
        self.effetItem()

    # Equiper une bénédiction dans l'emplacement principal ou secondaire en fonction de la récompense
    def equiper_benediction(self, emplacement):
        """
        Equipe la bénédiction dans l'emplacement spécifié
        Argument: emplacement
        """
        if self.recompense[0] in res.liste_benedictions:
            if emplacement == 0:
                self.benedictions[0] = self.recompense[0]
                self.iconBenediction1 = self.newBenedictionIcon
            elif emplacement == 1:
                self.benedictions[1] = self.recompense[0]
                self.iconBenediction2 = self.newBenedictionIcon
        
    # On met à jour les variables du navire changées par les équipements
    def effetItem(self):
        """
        Applique les modificateurs des équipements
        """

        # On remet la vitesse, la vie max et la maniabilité à zéro pour pouvoir les modifier ensuite
        self.maxVie = 50
        self.vitesse_max = 5
        self.maniabilite = 4

        # Modificateurs des coques
        if self.recompense[0] in res.listeCoques:
            self.iconCoque = self.DisplayIconNew
            self.CoqueMaxVie = 0
            self.CoqueMaxVitesse = 1
            if self.equipement['coque'] == "Coque épicéa":
                self.CoqueMaxVie += 10
                self.vie += 10
            elif self.equipement['coque'] == "Coque en bouleau":
                self.CoqueMaxVie += 10
                self.vie += 10
                self.CoqueMaxVitesse = 1.05
            elif self.equipement['coque'] == "Coque en chêne massif":
                self.CoqueMaxVie += 75
                self.vie += 75
                self.CoqueMaxVitesse = 0.80
            elif self.equipement['coque'] == "Coque chêne":
                self.CoqueMaxVitesse = 1.05
            elif self.equipement['coque'] == "Coque en bois magique":
                self.CoqueMaxVie += 50
                self.vie += 50
                self.CoqueMaxVitesse = 1.2
            elif self.equipement['coque'] == "Coque légendaire":
                self.CoqueMaxVie += 60
                self.vie += 60
                self.CoqueMaxVitesse = 1.3

        # Modificateurs des voiles
        elif self.recompense[0] in res.listeVoiles:
            self.iconVoile = self.DisplayIconNew
            self.VoileMaxVitesse = 1
            self.VoileMaxVie = 0
            if self.equipement['voile'] == "Voile en toile de jute":
                self.VoileMaxVitesse = 1.05
            elif self.equipement['voile'] == "Voile latine":
                self.VoileMaxVitesse = 1.1
            elif self.equipement['voile'] == "Voile enchantée":
                self.VoileMaxVitesse = 1.25
                self.maniabilite = self.maniabilite * 1.02
            elif self.equipement['voile'] == "Voile légendaire":
                self.VoileMaxVitesse = 1.3
                self.maniabilite = self.maniabilite * 1.05

        # Modificateurs des voiles
        elif self.recompense[0] in res.listeCanons:
            self.iconCanon = self.DisplayIconNew
            if (self.equipement['canons'] == "Canon en or") or (self.equipement['canons'] == "Canon légendaire"):
                self.cadence_tir = 600

        # Modificateurs des malus
        elif self.recompense[0] in res.liste_malus:
            if self.recompense[0] == "Voile Trouée":
                self.iconVoile = self.DisplayIconNew
                self.VoileMaxVitesse = 0.75
            elif self.recompense[0] == "Canons Rouillés":
                self.iconCanon = self.DisplayIconNew
            elif self.recompense[0] == "Coque Trouée":
                self.iconCoque = self.DisplayIconNew

        # On ajoute les modificateurs entre eux
        self.maxVie = self.maxVie + self.VoileMaxVie + self.CoqueMaxVie
        self.vitesse_max = self.vitesse_max * self.VoileMaxVitesse * self.CoqueMaxVitesse
        if self.vie > self.maxVie:
            self.vie = self.maxVie

    # Activation de la bénédiction primaire, plus puissante que la bénédiction secondaire
    def use_benediction_1(self):
        """
        Utilise la bénédiction primaire
        """

        if len(self.benedictions) > 0:

            # Fais un dash de 200 pixels si le cooldown est écoulé
            if self.timer_benediction_1.timer_ended_special(self.timer_dash) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction Dash":
                    self.x += 200 * math.cos(math.radians(self.angle - 90))
                    self.y += 200 * math.sin(math.radians(self.angle - 90))
                    self.timer_benediction_1 = res.Timer(50)
            
            # Rend 50% de la vie max si le cooldown est écoulé
            if self.timer_benediction_1.timer_ended_special(self.timer_sante) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction Santé":
                    self.vie += math.floor(self.maxVie*0.5)
                    if self.vie > self.maxVie:
                        self.vie = self.maxVie
                    self.timer_benediction_1 = res.Timer(50)
            
            # Crée une zone de 2 dégats par seconde autour du navire pendant 10 secondes si le cooldown est écoulé
            if self.timer_benediction_1.timer_ended_special(self.timer_aura) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction d'aura":
                    self.aura_timer = res.Timer(10)
                    self.has_aura = True
                    self.timer_benediction_1 = res.Timer(50)
                    self.aura_degat = 2

            # Baisse la vie mais augmente la vitesse et les dégats pendant 15 secondes si le cooldown est écoulé
            if self.timer_benediction_1.timer_ended_special(self.timer_rage) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction de rage":
                    self.rage_timer = res.Timer(15)
                    self.inraged = True
                    self.life_before_rage = self.vie/self.maxVie
                    self.vie = 20
                    self.timer_benediction_1 = res.Timer(50)
                    self.gif_rage = True
            
            # Rend le navire invincible pendant 20 seondes si le cooldown est écoulé
            if self.timer_benediction_1.timer_ended_special(self.timer_godmode) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction GodMode":
                    self.godmode = True
                    self.godmode_timer = res.Timer(20)
                    self.timer_benediction_1 = res.Timer(50)
            
            # Envoie une multitude de projectiles en tir double autour du navire pendant 8 secondes si le cooldown est écoulé
            if self.timer_benediction_1.timer_ended_special(self.timer_giga_tir) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction Projectiles":
                    self.giga_tir = True
                    self.giga_tir_double = True
                    self.timer_giga_tir_duree = res.Timer(8)
                    self.timer_benediction_1 = res.Timer(50)
        
    # Activation de la bénédiction secondaire, moins puissante que la bénédiction primaire
    def use_benediction_2(self):
        """
        Utilise la bénédiction secondaire
        """
        
        if len(self.benedictions) > 1:

            # Fais un dash de 100 pixels si le cooldown est écoulé
            if self.timer_benediction_2.timer_ended_special(self.timer_dash) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction Dash":
                    self.x += 100 * math.cos(math.radians(self.angle - 90))
                    self.y += 100 * math.sin(math.radians(self.angle - 90))
                    self.timer_benediction_2 = res.Timer(50)

            # Rend 25% de la vie max si le cooldown est écoulé
            if self.timer_benediction_2.timer_ended_special(self.timer_sante) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction Santé":
                    self.vie += math.floor(self.maxVie*0.25)
                    if self.vie > self.maxVie:
                        self.vie = self.maxVie
                    self.timer_benediction_2 = res.Timer(50)
            
            # Crée une zone de 1 dégat par seconde autour du navire pendant 10 secondes si le cooldown est écoulé
            if self.timer_benediction_2.timer_ended_special(self.timer_aura) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction d'aura":
                    self.aura_timer = res.Timer(10)
                    self.has_aura = True
                    self.timer_benediction_2 = res.Timer(50)
                    self.aura_degat = 1

            # Baisse la vie mais augmente la vitesse et les dégats pendant 10 secondes si le cooldown est écoulé
            if self.timer_benediction_2.timer_ended_special(self.timer_rage) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction de rage":
                    self.rage_timer = res.Timer(10)
                    self.inraged = True
                    self.life_before_rage = self.vie/self.maxVie
                    self.vie = 20
                    self.timer_benediction_2 = res.Timer(50)
                    self.gif_rage = True
            
            # Rend le navire invincible pendant 10 seondes si le cooldown est écoulé
            if self.timer_benediction_2.timer_ended_special(self.timer_godmode) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction GodMode":
                    self.godmode = True
                    self.godmode_timer = res.Timer(10)
                    self.timer_benediction_2 = res.Timer(50)

             # Envoie une multitude de projectiles en tir simple autour du navire pendant 5 secondes si le cooldown est écoulé
            if self.timer_benediction_2.timer_ended_special(self.timer_giga_tir) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction Projectiles":    
                    self.giga_tir = True
                    self.timer_giga_tir_duree = res.Timer(5)
                    self.timer_benediction_2 = res.Timer(50)

    # On remet la vie que le navire avait avant d'activer la bénédiction de rage, que l'on désactive
    def still_inraged(self):
        """
        Désactive la bénédiciton de rage
        """
        if self.inraged:
            if self.rage_timer != None and self.rage_timer.timer_ended():
                self.inraged = False
                self.vie = int(math.floor(self.maxVie * self.life_before_rage))
                self.rage_timer = None

    # On désactive la bénédiction de projectiles
    def still_giga_tir(self):
        """
        Désactive la bénédiciton d'aura
        """
        if self.giga_tir:
            if self.timer_giga_tir_duree.timer_ended():
                self.giga_tir = False
                self.giga_tir_double = False

    # On désactive la bénédiction de GodMode
    def in_godmode(self):
        """
        Désactive la bénédiciton de GodMode
        """
        if self.godmode:
            if self.godmode_timer.timer_ended():
                self.godmode = False
                self.godmode_timer = None
    
    # On désactive le gif de l'indicateur de rage
    def stop_animation_rage(self):
        """
        Désactive de gif de la bénédiction de rage
        """
        self.gif_rage = False
    
    def aura_activated(self, liste_navires):
        """
        Met à jour les dégats de l'aura en fonctio de la distance
        Argument: liste_navires
        """
        if self.has_aura:
            for n in liste_navires:
                if self.aura_damage_timer.timer_ended() and n.get_ID() != self.ID:

                    # On augmente les dégats de l'aura en fonction de la distance au navire
                    if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 150:
                        n.get_damaged(self.aura_degat)
                        if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 120:
                            n.get_damaged(self.aura_degat)
                            if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 90:
                                n.get_damaged(self.aura_degat)
                                if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 60:
                                    n.get_damaged(self.aura_degat)
                                    if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 30:
                                        n.get_damaged(self.aura_degat)
                        self.aura_damage_timer.reset()
            
            # On désactive la bénédiction d'aura'
            if self.aura_timer.timer_ended():
                self.has_aura = False
                self.aura_timer = None


    # On donne de la vie au joueur à chaque fin de vague
    def heal_par_vague(self):
        """
        Soigne le joueur à la fin de chaque vague
        """
        if self.maxVie - self.vie <= 30:
            self.vie = self.maxVie
        else:
            self.vie += 30