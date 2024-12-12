import math
import pygame
import fonction_auxiliere as fo_au

class Shot:
    def __init__(self, x, y, speed, angle, distance_max):
        self.x = x
        self.y = y
        self.position_initiale_x = x
        self.position_initiale_y = y
        self.speed = speed
        self.angle = angle
        self.vitesse = 15
        self.distance_max = distance_max

    # le boulet avance
    def avancer(self):
        self.x += self.vitesse * math.cos(math.radians(self.angle - 90))
        self.y += self.vitesse * math.sin(math.radians(self.angle - 90))
    
    # si la distance parcouru par le boulet est trop grande il despawn
    def despawn_distance(self):
        return fo_au.calc_distance(self.x, self.y, self.position_initiale_x, self.position_initiale_y) == self.distance_max
    
    