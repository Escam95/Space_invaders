import pygame
import pygame as pg
import Constants as c

clock = pg.time.Clock()
window = pg.display.set_mode((c.WIDTH, c.HEIGHT))
pg.display.set_caption('Space Invaders')
pg.display.set_icon(c.GAME_ICON)
game_running = True


def on_key_down(event):
    global space_ship_vel
    if event.key == pg.K_d and space_ship.x < c.WIDTH - c.SPACESHIP_WIDTH - 20:
        space_ship_vel = 1
    elif event.key == pg.K_a and space_ship.x > 20:
        space_ship_vel = -1


def on_key_up(event):
    global space_ship_vel
    if event.key == pg.K_d and space_ship_vel == 1:
        space_ship_vel = 0
    elif event.key == pg.K_a and space_ship_vel == -1:
        space_ship_vel = 0


def game_input():
    global game_running
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_running = False
        elif event.type == pg.KEYDOWN:
            on_key_down(event)
        elif event.type == pg.KEYUP:
            on_key_up(event)


def game_update():
    space_ship.x = space_ship.x + space_ship_vel * c.VEL


def game_output():
    window.fill(c.SPACE)
    window.blit(c.SPACESHIP, (space_ship.x, space_ship.y))
    pg.display.flip()


space_ship = pygame.Rect((c.WIDTH - c.SPACESHIP_WIDTH) // 2, c.HEIGHT - c.HEIGHT // 8,
                         c.SPACESHIP_WIDTH, c.SPACESHIP_HEIGHT)
space_ship_vel = 0
while game_running:
    clock.tick(c.FPS)
    game_input()
    game_update()
    game_output()
