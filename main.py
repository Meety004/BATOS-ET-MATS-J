import pygame
from Navire import *
from IA_ennemis import *
import shot as module_shot

# Initialisation de Pygame
pygame.init()
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))

# initialisation du delta time pour avoir la même vitesse sur tout les ordi
clock = pygame.time.Clock()

# listes avec le joueur
liste_joueur = [Navire(7, 0.2, 5, "images/bato.png", screen_width, screen_height)] #vitesse_max, acceleration, maniabilité, image
# liste avec les ennemis
liste_ennemis = [IA_ennemis(5, 0.2, 5, "images/bato.png", screen_width, screen_height), IA_ennemis(5, 0.2, 5, "images/bato.png", screen_width, screen_height)]
# liste de tout les tire a l'ecran
liste_shot = []
# liste avec les joueur et les ennemis (contenant donc tout les Navire a l'ecran)
liste_navire = liste_joueur + liste_ennemis

# Définition de la couleur de fond (noir)
BLACK = (0, 0, 0)

# Boucle principale du jeu
running = True


# Boucle de jeu
while running:


    # UPDATE


    # Gestion des événements (quitter le jeu)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer l'état des touches
    keys = pygame.key.get_pressed()

    # Gestion des touches du premier navire (pour l'instant impossible de rajouter d'autre joueurs ils ont tous les même touches)
    for navire_i in liste_joueur:
        if keys[pygame.K_UP]: # fleche du haut
            navire_i.accelerer()
        else:
            navire_i.ralentit()

        if keys[pygame.K_LEFT]: # fleche gauche
            navire_i.tourne_gauche()

        if keys[pygame.K_RIGHT]: # fleche droite
            navire_i.tourne_droite()
        
        if keys[pygame.K_SPACE]: # espace
            tire_du_navire = navire_i.shoot()
            if tire_du_navire is not None:
                liste_shot.extend(tire_du_navire)

        # Mettre à jour la position des navires
        navire_i.avancer()

        # verifie qu'ils ne sortent pas de l'ecran
        navire_i.sortir_ecran(screen_width, screen_height)
    

    # fait les deplacement de l'ennemi
    
    for ennemis in liste_ennemis:
        # a besoin de la position des joueurs pour incliner le deplacement
        for joueur in liste_joueur:
            ennemis.bouger(joueur.position_x(), joueur.position_y())

            # gere le tire de l'ennemi. return None si le joueur n'est pas a porté de l'ennemi
            tire_ennemi = ennemis.tirer(joueur.position_x(), joueur.position_y())
            if tire_ennemi != None: # si ca return none alors il l'efface
                liste_shot.extend(tire_ennemi) # la fonction de tire return une liste. il faut donc extend pour fusionner les liste et pas append

        ennemis.sortir_ecran(screen_width, screen_height)

    for shot_i in liste_shot:
        if shot_i is not None: # deuxieme verification pour voir si il n'y a pas de None dans les tire car ca casse tout
            shot_i.avancer()
            if shot_i.despawn_distance():
                liste_shot.remove(shot_i)
        else:
            liste_shot.remove(shot_i) # si il y a un None ca le detruit



    # DRAW


    #Remplir l'écran avec une couleur de fond
    screen.fill(BLACK)

    # affichage de l'ocean en fond
    ocean = pygame.image.load("images/ocean background.jpg").convert_alpha()
    ocean = pygame.transform.scale(ocean, (screen_width, screen_height)).convert_alpha()
    screen.blit(ocean, (0, 0))

    # Dessine les navires
    for navire_i in liste_navire:
        navire_i.afficher(screen)

    # dessine les tires
    for shot_i in liste_shot:
        shot_i.afficher(screen)

    # Rafraîchir l'écran
    pygame.display.flip()
    

    

    # pour quitter le jeux
    if keys[pygame.K_TAB]: # si on appuie sur tab ca quitte le jeu
        running = False

    # Limiter la boucle à 60 images par seconde
    clock.tick(60) # CA MARCHE PAS !!!!!!

# Quitter Pygame proprement
pygame.quit()