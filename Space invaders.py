import pygame
import pygame as pg
import Constants as c

pygame.init()

clock = pg.time.Clock()
window = pg.display.set_mode((c.WIDTH, c.HEIGHT))
pg.display.set_caption('Space Invaders')
pg.display.set_icon(c.GAME_ICON)
bullets = []
game_running = True
shooting_delay = 500
ally_shot_event = pygame.USEREVENT + 1
pygame.time.set_timer(ally_shot_event, shooting_delay)


def on_key_down(event):
    global space_ship_vel, bullets
    if event.key == pg.K_d and space_ship.x < c.WIDTH - c.SPACESHIP_WIDTH - c.SCREEN_OFFSET:
        space_ship_vel = 1
    elif event.key == pg.K_a and space_ship.x > c.SCREEN_OFFSET:
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
        if event.type == ally_shot_event:
            bullet = pygame.Rect(space_ship.x + c.SPACESHIP_WIDTH // 2 - c.BULLET_WIDTH // 2,
                                 space_ship.y + c.SPACESHIP_HEIGHT // 3, c.BULLET_WIDTH, c.BULLET_HEIGHT)
            bullets.append(bullet)


def game_update():
    global space_ship_vel
    space_ship.x = space_ship.x + space_ship_vel * c.VEL
    if space_ship.x > (c.WIDTH - c.SPACESHIP_WIDTH - c.SCREEN_OFFSET) or space_ship.x < c.SCREEN_OFFSET:
        space_ship_vel = 0
    for bullet in bullets:
        bullet.y -= c.BULLET_VEL


def game_output():
    window.fill(c.SPACE)
    window.blit(c.SPACESHIP, (space_ship.x, space_ship.y))
    for bullet in bullets:
        pygame.draw.rect(window, c.BULLET_COLOR, bullet)
    window.blit(c.BASIC_ENEMY_IMAGE, (0, 0))
    pg.display.flip()


space_ship = pygame.Rect((c.WIDTH - c.SPACESHIP_WIDTH) // 2, c.HEIGHT - c.HEIGHT // 8,
                         c.SPACESHIP_WIDTH, c.SPACESHIP_HEIGHT)
space_ship_vel = 0
while game_running:
    clock.tick(c.FPS)
    game_input()
    game_update()
    game_output()
