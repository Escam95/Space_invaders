import pygame as pg
import os
import pygame.image

images = [
    (5, 4)
]


def get_image(sheet, width, height, image_id, scale, colour):
    image = pg.Surface((width, height))
    image.blit(sheet, (0, 0), (images[image_id][0] * IMAGE_SIZE, images[image_id][1] * IMAGE_SIZE, width, height))
    image = pg.transform.rotate(pg.transform.scale(image, (width * scale, height * scale)), 180)
    image.set_colorkey(colour)

    return image


GAME_ICON = pygame.image.load('Images/spaceShips_007.png')
WIDTH, HEIGHT = 1200, 800
SCREEN_OFFSET = 75
SPACE = (60, 63, 65)
BLACK = (0, 0, 0)
BULLET_COLOR = (255, 255, 255)
FPS = 60
VEL = 5
BULLET_VEL = 9
BULLET_WIDTH = 5
BULLET_HEIGHT = 12
IMAGE_SIZE = 64
tile_sheet_image = pg.image.load(os.path.join('Images', 'simpleSpace_tilesheet.png'))
BASIC_ENEMY_IMAGE = get_image(tile_sheet_image, IMAGE_SIZE, IMAGE_SIZE, 0, 1, BLACK)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 80, 60
SPACESHIP_IMAGE = pg.image.load(os.path.join('Images', 'spaceShips_007.png'))
SPACESHIP = pg.transform.rotate(pg.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

