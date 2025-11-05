import pygame
import math
import constantes
import random

from mundo import obstaculos


#from Juego import imagen_balas


class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.image_original = image
        self.angulo = 0
        self.image = pygame.transform.rotate(self.image_original,self.angulo)
        self.forma = self.image.get_rect()
        self.dispara = False
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self, personaje):
            disparo_cooldowm = constantes.COOLDOWN_BALAS
            bala = None
            self.forma.center = personaje.forma.center
            if personaje.flip == False:
                self.forma.x = self.forma.x + personaje.forma.width/5
                self.rotar_arma(False)
            if personaje.flip == True:
                self.forma.x = self.forma.x - personaje.forma.width/5
                self.rotar_arma(True)
