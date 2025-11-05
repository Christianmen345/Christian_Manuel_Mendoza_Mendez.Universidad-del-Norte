import pygame
import constantes
from personaje import Personaje
from weapon import Weapon
import os
from textos import DamageTextos
from items import Item
from mundo import Mundo
import csv

#funciones:
#escalar imagenes
def escalar_img(image,scale):
    w=image.get_width()
    h=image.get_height()
    nueva_imagen=pygame.transform.scale(image,(w*scale,h*scale))
    return nueva_imagen

#funcion para contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))

#funcion listar nombre elementos
def nombre_carpetas(directorio):
    return os.listdir(directorio)
#print(nombre_carpetas("assets/images/characters/enemies"))

pygame.init()
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA,
                                   constantes.ALTO_VENTANA))
pygame.display.set_caption('Mi primer juego')

#variable
posicion_pantalla = [0, 0]
nivel = 1

#fuente
font = pygame.font.Font("assets/fonts/mokoto-mokoto-regular-glitch-mark-outline-400.ttf", 15)
font_game_over = pygame.font.Font("assets/fonts/mokoto-mokoto-regular-glitch-mark-outline-400.ttf", 70)
game_over_text = font_game_over.render("GAME OVER", True, constantes.BLANCO)

# Importar imagenes
# Energia
corazon_vacio = pygame.image.load("assets//images//items//heart_emply.png").convert_alpha()
corazon_vacio = escalar_img(corazon_vacio,constantes.SCALA_CORAZON)
corazon_mitad = pygame.image.load("assets//images//items//heart_haif.png").convert_alpha()
corazon_mitad = escalar_img(corazon_mitad,constantes.SCALA_CORAZON)
corazon_lleno = pygame.image.load("assets//images//items//heart_full.png").convert_alpha()
corazon_lleno = escalar_img(corazon_lleno,constantes.SCALA_CORAZON)


# Personaje
animaciones = []
for i in range(7):
    img =pygame.image.load(f'assets//images//characters//player//Player_{i}.png').convert_alpha()
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones.append(img)

#enemigos
directorio_enemigos = "assets//images//characters//enemies"
tipo_enemigos = nombre_carpetas(directorio_enemigos)
animaciones_enemigos = []
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets//images//characters//enemies/{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    print(f"número de imagenes {num_animaciones}")
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{eni}_{i + 1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo,constantes.SCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    animaciones_enemigos.append(lista_temp)
#print(animaciones_enemigos)


# Arma
imagen_pistola =pygame.image.load(f'assets//images//weapons//gun.png').convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALA_ARMA)

# Balas
imagen_balas =pygame.image.load(f'assets//images//weapons//bullet.png').convert_alpha()
imagen_balas = escalar_img(imagen_balas, constantes.SCALA_ARMA)

#cargar imagenes del mundo
tile_list = []
for x in range(100):
    tile_image = pygame.image.load(f'assets//images//files//file ({x+1}).png').convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constantes.TILE_SIZE, constantes.TILE_SIZE))
    tile_list.append(tile_image)

#cargar imagenes de los items
pocion_roja = pygame.image.load("assets//images//items//potion.png")
pocion_roja = escalar_img(pocion_roja, constantes.SCALA_POCION)
coin_images = []
ruta_img = "assets//images//items//coin"
num_coin_images = contar_elementos(ruta_img)
#print(f"numero de imagenes de moneda: {num_coin_images}")
for i in range(num_coin_images):
    img = pygame.image.load(f"assets//images//items//coin//coin_{i + 1}.png").convert_alpha()
    img = escalar_img(img, constantes.SCALA_MONEDA)
    coin_images.append(img)

item_imagenes = [coin_images, [pocion_roja]]

def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))


def vida_jugador():
    c_mitad_dibujado = False
    for i in range(4):
        if jugador.energia >= ((i+1)*25):
            ventana.blit(corazon_lleno,(5+i*50,5))
        elif jugador.energia % 25 > 0 and c_mitad_dibujado == False:
            ventana.blit(corazon_mitad,(5+i*50,5))
            c_mitad_dibujado = True
        else:
            ventana.blit(corazon_vacio,(5+i*50,5))

world_data = []

for fila in range(constantes.FILAS):
    filas = [5] * constantes.COLUMNA
    world_data.append(filas)

# cargar el archivo con el nivel
with open("assets//niveles//Juego.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for x, fila in enumerate(reader):
        for y , columna in enumerate(fila):
            world_data[x][y] = int(columna)
print(filas)

world: Mundo = Mundo()
world.process_data(world_data, tile_list,item_imagenes, animaciones_enemigos)


def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana,constantes.BLANCO,(x*constantes.TILE_SIZE,0),(x*constantes.TILE_SIZE,constantes.ALTO_VENTANA))
        pygame.draw.line(ventana,constantes.BLANCO,(0,x * constantes.TILE_SIZE),(constantes.ANCHO_VENTANA,x*constantes.TILE_SIZE))



# Crear un jugador de la clase personaje
jugador=Personaje(50,50,animaciones, constantes.VIDA_PERSONAJE,1)

#crear una lista de enemigos
lista_enemigos = []
for ene in world.lista_enemigo:
    lista_enemigos.append(ene)

#print(lista_enemigos)

# Crear un arma de la clase weapon
pistola = Weapon(imagen_pistola, imagen_balas)

#crear un grupo de sprites
grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()
#anadir items desde la data del nivel
for item in world.lista_item:
    grupo_items.add(item)

#definir la variable de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

# Controlar el frame rate
reloj = pygame.time.Clock()

run = True
while run:

    #que vaya a 60 fps
    reloj.tick(constantes.FPS)
    ventana.fill(constantes.COLOR_BG)
    dibujar_grid()


    if jugador.vivo == True:
        #Calcular el movimiento del jugador
        delta_x = 0
        delta_y = 0

        if mover_derecha == True:
            delta_x = constantes.VELOCIDAD
        if mover_izquierda == True:
            delta_x = -constantes.VELOCIDAD
        if mover_arriba == True:
            delta_y = -constantes.VELOCIDAD
        if mover_abajo == True:
            delta_y = constantes.VELOCIDAD

        #mover al jugador
        posicion_pantalla, nivel_completado = jugador.movimiento(delta_x, delta_y,world.obstaculos_tiles,
                                               world.exit_tile)

        #actualizar mapa
        world.update(posicion_pantalla)

        # actualiza estado del jugador
        jugador.update()

        # actualizar estado del enemigos
        for ene in lista_enemigos:
            ene.update()
            print(ene.energia)

        # actualiza el estado del arma
        bala = pistola.update(jugador)
        if bala:
            grupo_balas.add(bala)
        for bala in grupo_balas:
            damage, pos_damage = bala.update(lista_enemigos,world.obstaculos_tiles)
            if damage :
                damage_text = DamageTextos(pos_damage.centerx, pos_damage.centery, str(damage), font,constantes.ROJO)
                grupo_damage_text.add(damage_text)
            #print(grupo_balas)

    #Actualizar dano
        grupo_damage_text.update(posicion_pantalla)

    # Actualizar items
        grupo_items.update(posicion_pantalla,jugador)

    #dibujar mundo
    world.draw(ventana)

    # dibujar al jugador
    jugador.dibujar(ventana)

    # dibujar al enemigo
    for ene in lista_enemigos:
        if ene.energia == 0:
            lista_enemigos.remove(ene)
        if ene.energia > 0:
            ene.enemigos(jugador,world.obstaculos_tiles,posicion_pantalla,
                         world.exit_tile)
            ene.dibujar(ventana)

    # dibujar el arma
    pistola.dibujar(ventana)

    # dibujar balas
    for bala in grupo_balas:
        bala.dibujar(ventana)

    # dibujar los corazones
    vida_jugador()

    #dibujar textos
    grupo_damage_text.draw(ventana)
    dibujar_texto(f"Score: {jugador.score}",font,(255,255,0),700,5)
    #nivel
    dibujar_texto(f"Nivel" + str(nivel),font,constantes.BLANCO,constantes.ANCHO_VENTANA/2, 5)


    #dibujar items
    grupo_items.draw(ventana)

    if nivel_completado == True:
        nivel += 1

    if jugador.vivo == False:
        ventana.fill(constantes.ROJO_OSCURO)
        text_rect = game_over_text.get_rect(center=(constantes.ANCHO_VENTANA /2,
                                            constantes.ALTO_VENTANA /2))
        ventana.blit(game_over_text, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True


            #Para cuando se suelta la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False
    pygame.display.update()
pygame.quit()
