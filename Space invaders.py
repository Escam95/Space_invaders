import pygame as pg
import Constants as c
import random

pg.init()

clock = pg.time.Clock()
window = pg.display.set_mode((c.WIDTH, c.HEIGHT))
pg.display.set_caption('Space Invaders')
pg.display.set_icon(c.GAME_ICON)
bullets = []
enemies = []
game_running = True
shooting_delay = 500
spawning_delay = 2000
ally_shot_event = pg.USEREVENT + 1
pg.time.set_timer(ally_shot_event, shooting_delay)
spawn_basic_enemy = pg.USEREVENT + 2
pg.time.set_timer(spawn_basic_enemy, spawning_delay)


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
            bullet = pg.Rect(space_ship.x + c.IMAGE_SIZE // 2 - c.BULLET_WIDTH // 2,
                             space_ship.y + c.IMAGE_SIZE // 4, c.BULLET_WIDTH, c.BULLET_HEIGHT)
            bullets.append(bullet)
        if event.type == spawn_basic_enemy:
            enemy = pg.Rect(random.randint(c.SCREEN_OFFSET, c.WIDTH - c.IMAGE_SIZE - c.SCREEN_OFFSET), 0,
                            c.IMAGE_SIZE, c.IMAGE_SIZE)
            enemies.append(enemy)
            pg.time.set_timer(spawn_basic_enemy, spawning_delay)


def game_update():
    global space_ship_vel, spawning_delay
    space_ship.x = space_ship.x + space_ship_vel * c.VEL
    if space_ship.x > (c.WIDTH - c.IMAGE_SIZE - c.SCREEN_OFFSET) or space_ship.x < c.SCREEN_OFFSET:
        space_ship_vel = 0
    for enemy in enemies:
        enemy.y += c.ENEMY_VEL
    for bullet in bullets:
        bullet.y -= c.BULLET_VEL
        if bullet.collidelist(enemies) >= 0:
            enemies.pop(bullet.collidelist(enemies))
            bullets.remove(bullet)
    if spawning_delay > 100:
        spawning_delay -= 1


def game_output():
    window.fill(c.SPACE)
    window.blit(c.SPACESHIP_IMAGE, (space_ship.x, space_ship.y))
    for bullet in bullets:
        pg.draw.rect(window, c.BULLET_COLOR, bullet)
    for enemy in enemies:
        window.blit(c.BASIC_ENEMY_IMAGE, enemy)
    pg.display.flip()


space_ship = pg.Rect((c.WIDTH - c.IMAGE_SIZE) // 2, c.HEIGHT - c.HEIGHT // 8,
                     c.IMAGE_SIZE, c.IMAGE_SIZE)
space_ship_vel = 0
while game_running:
    clock.tick(c.FPS)
    game_input()
    game_update()
    game_output()
