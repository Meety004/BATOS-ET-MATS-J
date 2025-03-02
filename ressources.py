import math, pygame

def calc_distance(x1, y1, x2, y2):
    # fonction pour calculer une distance
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

liste_benedictions = [
    "Bénédiction Dash", 
    "Bénédiction Santé",
    "Bénédiction d'aura", 
    "Bénédiciton de rage",
    "Bénédiction GodMode", 
    "Bénédiction Projectile"
        ]

liste_malus = [
    "Canons Rouillés",
    "Voile Trouée",
    "Coque Trouée"
        ]

listeCanons = [
    "+1 Canon",
    "Canon en bronze",
    "+2 Canons", 
    "Canon en argent", 
    "Canon Ballistique",
    "+3 Canons", 
    "Canon en or", 
    "Canon à tirs doubles",
    "+4 Canons", 
    "Canon légendaire"
        ]

listeCoques = [
    "Coque épicéa",
    "Coque chêne",
    "Coque en bouleau", 
    "Coque en chêne massif",
    "Coque en bois magique",
    "Coque légendaire"
        ]

listeVoiles = [
    "Voile en toile de jute",
    "Voile Latine",
    "Voile Enchantée", 
    "Voile légendaire"
        ]

listeEquipementStart = [
    "Canon de base",
    "Voile de base",
    "Coque de base"
]

CoqueCommun = "images/Icons/Coques/coque_commun.png"
CoqueRare = "images/Icons/Coques/coque_rare.png"
CoqueMythique = "images/Icons/Coques/coque_mythique.png"
CoqueLegendaire = "images/Icons/Coques/coque_legendaire.png"

VoileCommun = "images/Icons/Voiles/voile_commun.png"
VoileRare = "images/Icons/Voiles/voile_rare.png"
VoileMythique = "images/Icons/Voiles/voile_mythique.png"
VoileLegendaire = "images/Icons/Voiles/voile_legendaire.png"

CanonCommun = "images/Icons/Canons/canon_commun.png"
CanonRare = "images/Icons/Canons/canon_rare.png"
CanonMythique = "images/Icons/Canons/canon_mythique.png"
CanonLegendaire = "images/Icons/Canons/canon_legendaire.png"

VoileMalus = "images/Icons/Voiles/voile_trouee.png"
CanonMalus = "images/Icons/Canons/canon_rouille.png"
CoqueMalus = "images/Icons/Coques/coque_trouee.png"

keyBindList =  [
    pygame.K_UP,
    pygame.K_LEFT,
    pygame.K_RIGHT
]

keyBindCursedList =  [
    pygame.K_DOWN,
    pygame.K_RIGHT,
    pygame.K_LEFT
]