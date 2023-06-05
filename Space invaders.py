import pygame as pg
import Constants as c
import random

#  WE NEED:
#  Health bars
#  Upgrades -- Tobias
#  Update the dmg dealing
#  End screen
#  Starting screen
#  Bosses
#  Waves

pg.init()

clock = pg.time.Clock()
#  window display
window = pg.display.set_mode((c.WIDTH, c.HEIGHT))
pg.display.set_caption('Space Invaders')
pg.display.set_icon(c.GAME_ICON)

#  basic variables
bullets = []
enemy_bullets = []
enemies = []
enemies_health = []
upgrades = []
game_running = True
score_delay = 0.01 * c.FPS
score_delay_countdown = score_delay
shooting_delay = .5 * c.FPS
shooting_delay_countdown = shooting_delay
spawning_delay = 2 * c.FPS
spawning_delay_countdown = spawning_delay
spawning_upgrade_delay = 20 * c.FPS
spawning_upgrade_countdown = spawning_upgrade_delay
health = c.STARTING_HEALTH
bullet_damage = c.STARTING_BULLET_DMG
basic_enemy_health = c.ENEMY_STARTING_HEALTH
ally_upgrade = 0
space_ship_image = c.SPACESHIP_IMAGE

score = 0

# score text
font_obj = pg.font.Font(None, 32)
score_Surface = font_obj.render(str(score), True, (97, 222, 42), None)
score_Rect = score_Surface.get_rect()
score_Rect.center = (700, 15)


def on_key_down(event):
    global space_ship_vel, bullets
    if event.key == pg.K_d or event.key == pg.K_RIGHT and space_ship.x < c.WIDTH - c.SPACESHIP_WIDTH - c.SCREEN_OFFSET:
        space_ship_vel = 1
    elif event.key == pg.K_a or event.key == pg.K_LEFT and space_ship.x > c.SCREEN_OFFSET:
        space_ship_vel = -1


def on_key_up(event):
    global space_ship_vel
    if event.key == pg.K_d or event.key == pg.K_RIGHT and space_ship_vel == 1:
        space_ship_vel = 0
    elif event.key == pg.K_a or event.key == pg.K_LEFT and space_ship_vel == -1:
        space_ship_vel = 0
    elif event.key == pg.K_SPACE:
        spawn_swarm()


#  spawning an enemy
def spawn_basic(position):
    enemy = pg.Rect(position, 0,
                    c.IMAGE_SIZE, c.IMAGE_SIZE)
    enemies.append(enemy)
    enemies_health.append(basic_enemy_health)


def spawn_swarm():
    for i in range(0, round((c.WIDTH - 2 * c.SCREEN_OFFSET) / 64)):
        spawn_basic(i * 64 + c.SCREEN_OFFSET)


#  spawning an upgrade
def spawn_upgrade(position):
    upgrade = pg.Rect(position, 0, c.IMAGE_SIZE, c.IMAGE_SIZE)
    upgrades.append(upgrade)


def game_input():
    global game_running
    key_input = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or key_input[pg.K_ESCAPE]:
            game_running = False
        elif event.type == pg.KEYDOWN:
            on_key_down(event)
        elif event.type == pg.KEYUP:
            on_key_up(event)


def game_update():
    global space_ship_vel, spawning_delay_countdown, \
        shooting_delay_countdown, score_Surface, score_delay_countdown, spawning_upgrade_countdown, game_running,\
        health, score_Rect, score

    if health <= 0:
        game_running = False

    #  timers
    score_delay_countdown -= 1
    if score_delay_countdown <= 0:
        score_Surface = font_obj.render(str(score), True, (97, 222, 42), None)
        score_Rect = score_Surface.get_rect()
        score_Rect.center = (700, 15)
        score += c.SCORE_INCREMENT
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

    spawning_upgrade_countdown -= 1
    if spawning_upgrade_countdown == 0:
        spawn_upgrade(random.randint(c.SCREEN_OFFSET, c.WIDTH - c.IMAGE_SIZE - c.SCREEN_OFFSET))
        spawning_upgrade_countdown = spawning_upgrade_delay

    #  updating the allied ship position
    space_ship.x = space_ship.x + space_ship_vel * c.VEL

    if space_ship.x > (c.WIDTH - c.IMAGE_SIZE - c.SCREEN_OFFSET) or space_ship.x < c.SCREEN_OFFSET:
        space_ship_vel = 0

    #  updating the lists
    for upgrade in upgrades:
        global ally_upgrade, space_ship_image, bullet_damage
        upgrade.y += c.ENEMY_Y_VEL
        if upgrade.colliderect(space_ship):
            ally_upgrade += 1
            upgrades.remove(upgrade)
            health += 200
            bullet_damage += 5
            if ally_upgrade < c.UPGRADE_IMAGES:
                space_ship_image = c.ALLY_UPGRADES[ally_upgrade]

    for enemy in enemies:
        enemy.y += c.ENEMY_Y_VEL
        # checking if an enemy health is 0
        if enemies_health[enemies.index(enemy)] <= 0:
            enemies_health.pop(enemies.index(enemy))
            enemies.pop(enemies.index(enemy))
        # shooting - 1 in 100 frames
        if random.randint(0, 100) == 100:
            enemy_bullet = pg.Rect(enemy.x + c.IMAGE_SIZE // 2 - c.BULLET_WIDTH // 2,
                                   enemy.y + c.IMAGE_SIZE // 2, c.BULLET_WIDTH, c.BULLET_HEIGHT)
            enemy_bullets.append(enemy_bullet)
        if enemy.y >= c.HEIGHT:
            enemies_health.pop(enemies.index(enemy))
            enemies.remove(enemy)
        elif enemy.colliderect(space_ship):
            health -= 200
    for bullet in bullets:
        bullet.y -= c.BULLET_VEL
        if bullet.collidelist(enemies) >= 0:
            enemies_health[bullet.collidelist(enemies)] -= bullet_damage
            bullets.remove(bullet)
        elif bullet.y < 0:
            bullets.remove(bullet)
    for enemy_bullet in enemy_bullets:
        enemy_bullet.y += c.ENEMY_BULLET_VEL
        if enemy_bullet.colliderect(space_ship):
            enemy_bullets.remove(enemy_bullet)
            health -= 50


def game_output():
    global space_ship_image
    window.fill(c.SPACE)

    #  drawing the allied ship
    window.blit(space_ship_image, (space_ship.x, space_ship.y))

    #  drawing the score
    window.blit(score_Surface, score_Rect)

    #  healthbar
    pg.draw.rect(window, c.ENEMY_BULLET_COLOR, (0, 0, 500, 10))

    #  drawing the lists of objects
    for bullet in bullets:
        pg.draw.rect(window, c.BULLET_COLOR, bullet)
    for enemy_bullet in enemy_bullets:
        pg.draw.rect(window, c.ENEMY_BULLET_COLOR, enemy_bullet)
    for enemy in enemies:
        window.blit(c.BASIC_ENEMY_IMAGE, enemy)
        pg.draw.rect(window, (255, 0, 0), (enemy.x + c.IMAGE_SIZE//2 - basic_enemy_health//2, enemy.y - 20,
                                           basic_enemy_health, 5))
        pg.draw.rect(window, (0, 255, 0), (enemy.x + c.IMAGE_SIZE//2 - basic_enemy_health//2, enemy.y - 20,
                                           enemies_health[enemies.index(enemy)], 5))
    for upgrade in upgrades:
        window.blit(c.UPGRADE_ICON_IMAGE, upgrade)
    pg.display.flip()


space_ship = pg.Rect((c.WIDTH - c.IMAGE_SIZE) // 2, c.HEIGHT - c.HEIGHT // 8,
                     c.IMAGE_SIZE, c.IMAGE_SIZE)
space_ship_mask = pg.mask.from_surface(space_ship_image)
space_ship_mask_image = space_ship_mask.to_surface()
space_ship_vel = 0

#  main game loop
while game_running:
    clock.tick(c.FPS)
    game_input()
    game_update()
    game_output()
game_running = True

#  temporary exit screen
while game_running:
    game_input()
    pg.draw.rect(window, c.BLACK, (c.WIDTH // 2, c.HEIGHT // 2, 200, 100))
    pg.display.flip()
