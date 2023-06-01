import pygame as pg
import os

pg.init()

# coordinates of the images in the tilesheet
images = [
    (0, 0),
    (7, 4),
    (5, 4),
    (5, 5),
    (3, 0),
    (2, 0),
    (5, 0),
    (6, 0)
]


# a function for getting an image out of the tilesheet - you need to input the parameters of your image and add its
# position in the images list above. Please add them below the others.
def get_image(sheet, width, height, image_id, scale, colour, rotation):
    image = pg.Surface((width, height))
    image.blit(sheet, (0, 0), (images[image_id][0] * IMAGE_SIZE, images[image_id][1] * IMAGE_SIZE, width, height))
    image = pg.transform.rotate(pg.transform.scale(image, (width * scale, height * scale)), rotation)
    image.set_colorkey(colour)

    return image


score = 0
score_increment = 1
score_a = 1

# basic constants
GAME_ICON = pg.image.load('Images/spaceShips_007.png')
WIDTH, HEIGHT = 1400, 800
SCREEN_OFFSET = 75
SPACE = (60, 63, 65)
BLACK = (0, 0, 0)
BULLET_COLOR = (255, 255, 255)
ENEMY_BULLET_COLOR = (255, 0, 0)
FPS = 60
VEL = 5
BULLET_VEL = 9
ENEMY_BULLET_VEL = 5
BULLET_WIDTH = 5
BULLET_HEIGHT = 12
ENEMY_Y_VEL = 2
IMAGE_SIZE = 64
STARTING_HEALTH = 500
ENEMY_STARTING_HEALTH = 20
tile_sheet_image = pg.image.load(os.path.join('Images', 'simpleSpace_tilesheet.png'))
BASIC_ENEMY_IMAGE = get_image(tile_sheet_image, IMAGE_SIZE, IMAGE_SIZE, 1, 1, BLACK, 180)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 80, 60
SPACESHIP_IMAGE = get_image(tile_sheet_image, IMAGE_SIZE, IMAGE_SIZE, 0, 1, BLACK, 0)
UPGRADE_ICON_IMAGE = get_image(tile_sheet_image, IMAGE_SIZE, IMAGE_SIZE, 3, 1, BLACK, 0)

# creating a list of the upgrade images for the allied ship
ALLY_UPGRADES = []
UPGRADE_IMAGES = 4
for upgrade_image_id in range(0, UPGRADE_IMAGES):
    upgrade_image = get_image(tile_sheet_image, IMAGE_SIZE, IMAGE_SIZE, upgrade_image_id + 4, 1, BLACK, 0)
    ALLY_UPGRADES.append(upgrade_image)

