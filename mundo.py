import constantes
from items import Item
from personaje import Personaje

obstaculos = [1, 2, 3, 4, 5, 0, 10, 15, 20, 25, 30, 35, 41, 42, 43, 44, 45, 40, 51, 52, 53, 54, 55, 50]

class Mundo():
    def __init__(self) -> None:
        self.map_tiles = []
        self.obstaculos_tiles = []
        self.exit_tile = None
        self.lista_item = []
        self.lista_enemigo = []

    def process_data(self, data, tile_list,item_imagenes,animacion_enemigos):
        self.level_length = len(data)
        for y , row in enumerate(data):
            for x , tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constantes.TILE_SIZE
                image_y = y * constantes.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]
                #agregar tiles a obstaculos
                if tile in obstaculos:
                    self.obstaculos_tiles.append(tile_data)
                #tile de salida
                elif tile == 12:
                    self.exit_tile = tile_data
                    #crear monedas
                elif tile == 86:
                    moneda = Item(image_x, image_y,0,item_imagenes[0])
                    self.lista_item.append(moneda)
                    tile_data[0] = tile_list[22]
                    #crear pociones
                elif tile == 89:
                    pocion = Item(image_x, image_y,1,item_imagenes[1])
                    self.lista_item.append(pocion)
                    tile_data[0] = tile_list[22]
                    #crear diablo
                elif tile == 74:
                    diablito = Personaje(image_x, image_y,animacion_enemigos[0],150,2)
                    self.lista_enemigo.append(diablito)
                    tile_data[0] = tile_list[22]
                elif tile == 77:
                    oso = Personaje(image_x, image_y,animacion_enemigos[1],350,2)
                    self.lista_enemigo.append(oso)
                    tile_data[0] = tile_list[22]



                self.map_tiles.append(tile_data)

    def update(self, posicion_pantalla):
        for tile in self.map_tiles:
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
