import pygame as pg
import os

import pygame.image

GAME_ICON = pygame.image.load('Images/spaceShips_007.png')
WIDTH, HEIGHT = 800, 600
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SPACE = (60, 63, 65)
FPS = 60
VEL = 5
BULLET_VEL = 9
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 80, 60
SPACESHIP_IMAGE = pg.image.load(os.path.join('Images', 'spaceShips_007.png'))
SPACESHIP = pg.transform.rotate(pg.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)
