import math
from operator import truediv

import pygame
import constantes


class Personaje():
    def __init__(self,x,y,animaciones, energia, tipo):
        self.score = 0
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        #Imagen de la animacion se esta mostrando actualmente
        self.frame_index = 0
        # Aqui se almacena la hora actual(en milisegundo desde que se inició 'pygame')
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma= self.image.get_rect()
        self.forma.center =(x,y)
        self.tipo = tipo
        self.ultimo_golpe = pygame.time.get_ticks()
        self.golpe = False
        self.ultimo_golpe = pygame.time.get_ticks()

    def movimiento(self, delta_x, delta_y,obstaculos_tiles,exit_tile):
        posicion_pantalla = [0, 0]
        nivel_completado = False
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        self.forma.x += delta_x
        for obstaculo in obstaculos_tiles:
            if obstaculo[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = obstaculo[1].left
                if delta_x < 0:
                    self.forma.left = obstaculo[1].right

        self.forma.y += delta_y
        for obstaculo in obstaculos_tiles:
            if obstaculo[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = obstaculo[1].top
                if delta_y < 0:
                    self.forma.top = obstaculo[1].bottom

        #logica solo aplica al jugador y no  enemigos
        if self.tipo == 1:
            #chequear colision con el tile de salida
            if exit_tile[1].colliderect(self.forma):
                nivel_completado = True
                print("Nivel completado")

            if self.forma.right > (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA):
                posicion_pantalla[0] = (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA) - self.forma.right
                self.forma.right = constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA
            if self.forma.left < constantes.LIMITE_PANTALLA:
                posicion_pantalla[0] = constantes.LIMITE_PANTALLA - self.forma.left
                self.forma.left = constantes.LIMITE_PANTALLA

            if self.forma.bottom > (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA):
                posicion_pantalla[1] = (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA) - self.forma.bottom
                self.forma.bottom = constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA
            if self.forma.top < constantes.LIMITE_PANTALLA:
                posicion_pantalla[1] = constantes.LIMITE_PANTALLA - self.forma.top
                self.forma.top = constantes.LIMITE_PANTALLA

            return posicion_pantalla, nivel_completado

        return posicion_pantalla

    def enemigos(self,jugador, obstaculos_tiles,posicion_pantalla,exit_tile):
        clipped_line = ()
        ene_dx = 0
        ene_dy = 0
        #resposición de enemigos basado en la posicion de la pantalla o camara
        self.forma.x += posicion_pantalla[0]
        self.forma.y += posicion_pantalla[1]

        #crear una linea de vision
        linea_de_vision = ((self.forma.centerx,self.forma.centery),
                           (jugador.forma.centerx,jugador.forma.centery))

        #chequear si hay obstaculos en la linea de vision del enemigo
        for obs in obstaculos_tiles:
            if obs[1].clipline(linea_de_vision):
                clipped_line = obs[1].clipline(linea_de_vision)

    #Distancia con el jugador
        distancia = math.sqrt(((self.forma.centerx - jugador.forma.centerx)**2)+
                              ((self.forma.centery - jugador.forma.centery)**2))

        if not clipped_line and  distancia < constantes.RANGO:
            if self.forma.centerx > jugador.forma.centerx:
                ene_dx = -constantes.VELOCIDAD_ENEMIGO
            if self.forma.centerx < jugador.forma.centerx:
                ene_dx = constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery > jugador.forma.centery:
                ene_dy = -constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery < jugador.forma.centery:
                ene_dy = constantes.VELOCIDAD_ENEMIGO

        self.movimiento(ene_dx, ene_dy, obstaculos_tiles, exit_tile)

        #atacar al jugador
        if distancia < constantes.RANGO_ATAQUE and jugador.golpe == False:
            jugador.energia -= 10
            jugador.golpe = True
            jugador.ultimo_golpe = pygame.time.get_ticks()

    def update(self):
        #comprobar si el personaje ha muerto
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False

        #timer para volver a recibir dano
        golpe_cooldown = 1000
        if self.tipo == 1:
            if self.golpe == True:
                if pygame.time.get_ticks() - self.ultimo_golpe > golpe_cooldown:
                    self.golpe = False



        cooldown_animacion = 200
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image,self.flip,False)
        interfaz.blit(imagen_flip, self.forma)
