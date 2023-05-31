import pygame as pg
import Constants as c
import random

pg.init()

clock = pg.time.Clock()
window = pg.display.set_mode((c.WIDTH, c.HEIGHT))
pg.display.set_caption('Space Invaders')
pg.display.set_icon(c.GAME_ICON)
bullets = []
enemy_bullets = []
enemies = []
game_running = True
score_delay = 0.5 * c.FPS
score_delay_countdown = score_delay
shooting_delay = .5 * c.FPS
shooting_delay_countdown = shooting_delay
spawning_delay = 2 * c.FPS
spawning_delay_countdown = spawning_delay
health = c.STARTING_HEALTH

font_obj = pg.font.Font(None, 32)
score_Surface = font_obj.render(str(c.score), True, (97, 222, 42), None)
score_Rect = score_Surface.get_rect()
score_Rect.center = (400, 30)


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
    elif event.key == pg.K_SPACE:
        spawn_swarm()


def spawn_basic(position):
    enemy = pg.Rect(position, 0,
                    c.IMAGE_SIZE, c.IMAGE_SIZE)
    enemies.append(enemy)


def spawn_swarm():
    for i in range(0, round((c.WIDTH - 2 * c.SCREEN_OFFSET) / 64)):
        spawn_basic(i * 64 + c.SCREEN_OFFSET)


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
    global space_ship_vel, spawning_delay_countdown, shooting_delay_countdown, game_running, health, score_Rect, \
        score_Surface, score_delay_countdown

    if health <= 0:
        game_running = False

    score_delay_countdown -= 1
    if score_delay_countdown == 0:
        score_Surface = font_obj.render(str(c.score // c.score_a), True, (97, 222, 42), None)
        score_Rect = score_Surface.get_rect()
        score_Rect.center = (400, 30)
        c.score += c.score_increment
        score_delay_countdown = score_delay

    shooting_delay_countdown -= 1
    if shooting_delay_countdown == 0:
        bullet = pg.Rect(space_ship.x + c.IMAGE_SIZE // 2 - c.BULLET_WIDTH // 2,
                         space_ship.y + c.IMAGE_SIZE // 4, c.BULLET_WIDTH, c.BULLET_HEIGHT)
        bullets.append(bullet)
        shooting_delay_countdown = shooting_delay
    spawning_delay_countdown -= 1
    if spawning_delay_countdown == 0:
        spawn_basic(random.randint(c.SCREEN_OFFSET, c.WIDTH - c.IMAGE_SIZE - c.SCREEN_OFFSET))
        spawning_delay_countdown = spawning_delay

    space_ship.x = space_ship.x + space_ship_vel * c.VEL

    if space_ship.x > (c.WIDTH - c.IMAGE_SIZE - c.SCREEN_OFFSET) or space_ship.x < c.SCREEN_OFFSET:
        space_ship_vel = 0

    for enemy in enemies:
        enemy.y += c.ENEMY_Y_VEL
        if random.randint(0, 100) == 100:
            enemy_bullet = pg.Rect(enemy.x + c.IMAGE_SIZE // 2 - c.BULLET_WIDTH // 2,
                                   enemy.y + c.IMAGE_SIZE // 2, c.BULLET_WIDTH, c.BULLET_HEIGHT)
            enemy_bullets.append(enemy_bullet)
        if enemy.y >= c.HEIGHT:
            enemies.remove(enemy)
        elif enemy.colliderect(space_ship):
            game_running = False
    for bullet in bullets:
        bullet.y -= c.BULLET_VEL
        if bullet.collidelist(enemies) >= 0:
            enemies.pop(bullet.collidelist(enemies))
            bullets.remove(bullet)
        elif bullet.y < 0:
            bullets.remove(bullet)
    for enemy_bullet in enemy_bullets:
        enemy_bullet.y += c.ENEMY_BULLET_VEL
        if enemy_bullet.colliderect(space_ship):
            enemy_bullets.remove(enemy_bullet)
            health -= 50


def game_output():
    window.fill(c.SPACE)
    window.blit(c.SPACESHIP_IMAGE, (space_ship.x, space_ship.y))
    window.blit(score_Surface, score_Rect)
    pg.draw.rect(window, c.ENEMY_BULLET_COLOR, (0, 0, 500, 10))
    for bullet in bullets:
        pg.draw.rect(window, c.BULLET_COLOR, bullet)
    for enemy_bullet in enemy_bullets:
        pg.draw.rect(window, c.ENEMY_BULLET_COLOR, enemy_bullet)
    for enemy in enemies:
        window.blit(c.BASIC_ENEMY_IMAGE, enemy)
    pg.display.flip()


space_ship = pg.Rect((c.WIDTH - c.IMAGE_SIZE) // 2, c.HEIGHT - c.HEIGHT // 8,
                     c.IMAGE_SIZE, c.IMAGE_SIZE)
space_ship_mask = pg.mask.from_surface(c.SPACESHIP_IMAGE)
space_ship_mask_image = space_ship_mask.to_surface()
space_ship_vel = 0
while game_running:
    clock.tick(c.FPS)
    game_input()
    game_update()
    game_output()
game_running = True
while game_running:
    game_input()
    pg.draw.rect(window, c.BLACK, (c.WIDTH // 2, c.HEIGHT // 2, 200, 100))
    pg.display.flip()
