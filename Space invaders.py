import pygame as pg
import Constants as c
clock = pg.time.Clock()
window = pg.display.set_mode((c.WIDTH, c.HEIGHT))
pg.display.set_caption('Space Invaders')


def game_input():
    ...


def game_update():
    ...


def game_output():
    ...


game_running = True
while game_running:
    clock.tick(c.FPS)
    game_input()
    game_update()
    game_output()