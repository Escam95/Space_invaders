import pygame as pg
import Constants as c
import random

#  WE NEED:
#  Upgrades
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

wave_1 = [
    [3, 0, 0],
    [2, 2, 0],
    [5, 2, 0]
]

#  basic variables
while True:

    level = wave_1

    wave_beaten = True
    min_wave_beaten = True

    bullets = []
    enemy_bullets = []
    basic_enemies = []
    fast_enemies = []
    heavy_enemies = []
    basic_enemies_health = []
    fast_enemies_health = []
    heavy_enemies_health = []
    enemies = [basic_enemies, fast_enemies, heavy_enemies]
    enemies_health = [basic_enemies_health, fast_enemies_health, heavy_enemies_health]
    upgrades = []
    game_running = True
    game_stopped = False
    score_delay = 0.1 * c.FPS
    score_delay_countdown = score_delay
    shooting_delay = .5 * c.FPS
    shooting_delay_countdown = shooting_delay
    basic_spawning_delay = 2 * c.FPS
    basic_spawning_delay_countdown = basic_spawning_delay
    fast_spawning_delay = 3 * c.FPS
    fast_spawning_delay_countdown = fast_spawning_delay
    heavy_spawning_delay = 5 * c.FPS
    heavy_spawning_delay_countdown = heavy_spawning_delay
    swarm_spawning_delay = 10 * c.FPS
    swarm_spawning_countdown = swarm_spawning_delay
    spawning_upgrade_delay = 5 * c.FPS
    spawning_upgrade_countdown = spawning_upgrade_delay
    health = c.STARTING_HEALTH
    max_health = health
    health_inc = 0
    enemy_damage_inc = 0
    bullet_damage_inc = 0
    bullet_damage = c.STARTING_BULLET_DMG
    basic_enemy_health = c.ENEMY_STARTING_HEALTH
    fast_enemy_health = c.ENEMY_STARTING_HEALTH - 10
    heavy_enemy_health = c.ENEMY_STARTING_HEALTH + 100
    basic_enemy_max_health = basic_enemy_health
    fast_enemy_max_health = fast_enemy_health
    heavy_enemy_max_health = heavy_enemy_health
    enemies_max_health = [basic_enemy_max_health, fast_enemy_max_health, heavy_enemy_max_health]
    ally_upgrade = 0
    space_ship_image = c.SPACESHIP_IMAGE
    score = 0

    # score text
    font_obj = pg.font.Font("Fonts/thin.ttf", 64)
    score_Surface = font_obj.render(str(score), True, (97, 222, 42), None)
    score_Rect = score_Surface.get_rect()
    score_Rect.center = (c.WIDTH // 2, c.HEIGHT // 12)

    end_screen_Surface = font_obj.render(str('GAME OVER'), True, (255, 255, 255), c.SPACE)
    end_screen_Rect = end_screen_Surface.get_rect()
    end_screen_Rect.center = (c.WIDTH // 2, c.HEIGHT // 2)


    def random_screen():
        return random.randint(c.SCREEN_OFFSET, c.WIDTH - c.IMAGE_SIZE - c.SCREEN_OFFSET)


    def on_key_down(event):
        global space_ship_vel, bullets, game_running, end_screen
        if event.key == pg.K_d or event.key == pg.K_RIGHT and \
                space_ship.x < c.WIDTH - c.SPACESHIP_WIDTH - c.SCREEN_OFFSET:
            space_ship_vel = 1
        elif event.key == pg.K_a or event.key == pg.K_LEFT and space_ship.x > c.SCREEN_OFFSET:
            space_ship_vel = -1
        elif event.key == pg.K_r:
            game_running = True
            end_screen = False


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
        basic_enemies.append(enemy)
        basic_enemies_health.append(basic_enemy_health)


    def spawn_fast(position):
        enemy = pg.Rect(position, 0,
                        c.IMAGE_SIZE, c.IMAGE_SIZE)
        fast_enemies.append(enemy)
        fast_enemies_health.append(fast_enemy_health)


    def spawn_heavy(position):
        enemy = pg.Rect(position, 0,
                        c.IMAGE_SIZE, c.IMAGE_SIZE)
        heavy_enemies.append(enemy)
        heavy_enemies_health.append(heavy_enemy_health)


    def spawn_boss(position):
        ...


    def spawn_swarm():
        for i in range(0, round((c.WIDTH - 2 * c.SCREEN_OFFSET) / 64)):
            spawn_basic(i * 64 + c.SCREEN_OFFSET)


    def spawn_wave():
        for wave in level:
            for enemy_num in wave:
                for enemy in range(0, enemy_num):
                    if wave[0] == enemy_num:
                        spawn_basic(random_screen())
                    elif wave[1] == enemy_num:
                        spawn_fast(random_screen())
                    elif wave[2] == enemy_num:
                        spawn_heavy(random_screen())


    #  spawning an upgrade
    def spawn_upgrade(position):
        upgrade = pg.Rect(position, 0, c.IMAGE_SIZE, c.IMAGE_SIZE)
        upgrades.append(upgrade)


    def game_input():
        global game_running
        key_input = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT or key_input[pg.K_ESCAPE]:
                on_exit()
            elif event.type == pg.KEYDOWN:
                on_key_down(event)
            elif event.type == pg.KEYUP:
                on_key_up(event)


    # do you really want to exit menu
    def on_exit():
        global game_running, game_stopped
        game_stopped = True
        while game_stopped:
            exit_surface = font_obj.render('ESC to leave', True, (255, 255, 255), c.SPACE)
            exit_2_surface = font_obj.render('L-CLICK to continue', True, (255, 255, 255), c.SPACE)
            exit_2_rect = exit_2_surface.get_rect()
            exit_rect = exit_surface.get_rect()
            exit_rect.center = (c.WIDTH // 2, c.HEIGHT // 2)
            exit_2_rect.center = (c.WIDTH // 2, c.HEIGHT // 2 + exit_rect.height)
            window.blit(exit_surface, exit_rect)
            window.blit(exit_2_surface, exit_2_rect)
            pg.display.flip()
            key_input = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT or key_input[pg.K_ESCAPE]:
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == c.LEFT:
                    game_stopped = False


    def game_update():
        global space_ship_vel, basic_spawning_delay_countdown, \
            shooting_delay_countdown, score_Surface, score_delay_countdown, spawning_upgrade_countdown, game_running, \
            health, score_Rect, score, shooting_delay, max_health, swarm_spawning_countdown, \
            fast_spawning_delay_countdown, heavy_spawning_delay_countdown, enemy_damage_inc, bullet_damage_inc, wave_beaten

        if health <= 0:
            game_running = False

        if wave_beaten:
            wave_beaten = False
            spawn_wave()

        if enemies[0] == [] and enemies[1] == [] and enemies[2] == []:
            wave_beaten = True

        # timers
        score_delay_countdown -= 1
        if score_delay_countdown <= 0:
            score_Surface = font_obj.render(str(score // c.SCORE_A), True, (97, 222, 42), None)
            score_Rect = score_Surface.get_rect()
            score_Rect.center = (c.WIDTH // 2, c.HEIGHT // 12)
            score += c.SCORE_INCREMENT
            score_delay_countdown = score_delay
            enemy_damage_inc += 2
            bullet_damage_inc += 1
        shooting_delay_countdown -= 1
        if shooting_delay_countdown <= 0:
            bullet = pg.Rect(space_ship.x + c.IMAGE_SIZE // 2 - c.BULLET_WIDTH // 2,
                             space_ship.y + c.IMAGE_SIZE // 4, c.BULLET_WIDTH, c.BULLET_HEIGHT)
            bullets.append(bullet)
            shooting_delay_countdown = shooting_delay

        basic_spawning_delay_countdown -= 1
        if basic_spawning_delay_countdown <= 0:
            spawn_basic(random_screen())
            basic_spawning_delay_countdown = basic_spawning_delay

        fast_spawning_delay_countdown -= 1
        if fast_spawning_delay_countdown <= 0:
            spawn_fast(random_screen())
            fast_spawning_delay_countdown = fast_spawning_delay

        heavy_spawning_delay_countdown -= 1
        if heavy_spawning_delay_countdown <= 0:
            spawn_heavy(random_screen())
            heavy_spawning_delay_countdown = heavy_spawning_delay

        swarm_spawning_countdown -= 1
        if swarm_spawning_countdown <= 0:
            spawn_swarm()
            swarm_spawning_countdown = swarm_spawning_delay

        spawning_upgrade_countdown -= 1
        if spawning_upgrade_countdown <= 0:
            spawn_upgrade(random.randint(c.SCREEN_OFFSET, c.WIDTH - c.IMAGE_SIZE - c.SCREEN_OFFSET))
            spawning_upgrade_countdown = spawning_upgrade_delay

        #  updating the allied ship position
        space_ship.x = space_ship.x + space_ship_vel * c.VEL

        if space_ship.x > (c.WIDTH - c.IMAGE_SIZE - c.SCREEN_OFFSET) or space_ship.x < c.SCREEN_OFFSET:
            space_ship_vel = 0

        #  updating the lists
        for upgrade in upgrades:
            global ally_upgrade, space_ship_image, bullet_damage, health_inc
            upgrade.y += c.ENEMY_Y_VEL
            if upgrade.colliderect(space_ship):
                ally_upgrade += 1
                upgrades.remove(upgrade)
                health += 200 + health_inc
                max_health += 200
                bullet_damage += 5
                health_inc += 50
                if shooting_delay > 5:
                    shooting_delay -= 5
                if ally_upgrade < c.UPGRADE_IMAGES:
                    space_ship_image = c.ALLY_UPGRADES[ally_upgrade]
                if health > max_health:
                    health = max_health

        for enemy_list in enemies:
            for enemy in enemy_list:
                if enemy_list == basic_enemies:
                    enemy.y += c.ENEMY_Y_VEL
                elif enemy_list == fast_enemies:
                    enemy.y += c.ENEMY_Y_VEL + 2
                elif enemy_list == heavy_enemies:
                    enemy.y += c.ENEMY_Y_VEL - 1
                # checking if an enemy health is 0
                # basic_enemies_health[basic_enemies.index(enemy)]
                if enemies_health[enemies.index(enemy_list)][enemy_list.index(enemy)] <= 0:
                    enemies_health[enemies.index(enemy_list)].pop(enemy_list.index(enemy))
                    enemy_list.pop(enemy_list.index(enemy))
                # shooting - 1 in 100 frames
                if random.randint(0, 100) == 100:
                    enemy_bullet = pg.Rect(enemy.x + c.IMAGE_SIZE // 2 - c.BULLET_WIDTH // 2,
                                           enemy.y + c.IMAGE_SIZE // 2, c.BULLET_WIDTH, c.BULLET_HEIGHT)
                    enemy_bullets.append(enemy_bullet)
                if enemy.y >= c.HEIGHT:
                    # enemies_health[enemies.index(enemy_list)].pop(enemy_list.index(enemy))
                    enemy.y = -c.IMAGE_SIZE
                elif enemy.colliderect(space_ship):
                    enemy_list.remove(enemy)
                    health -= 200 + enemy_damage_inc
            for bullet in bullets:
                if bullet.collidelist(enemy_list) >= 0:
                    enemies_health[enemies.index(enemy_list)][bullet.collidelist(enemy_list)] -= bullet_damage
                    bullets.remove(bullet)
                elif bullet.y < 0:
                    bullets.remove(bullet)
        for bullet in bullets:
            bullet.y -= c.BULLET_VEL
        for enemy_bullet in enemy_bullets:
            enemy_bullet.y += c.ENEMY_BULLET_VEL
            # enemy_bullet_mask = pg.mask.from_surface(enemy_bullet)
            # if space_ship_mask.overlap(enemy_bullet_mask,
            # (enemy_bullet.x - space_ship.x, enemy_bullet.y - space_ship.y)):
            # enemy_bullets.remove(enemy_bullet)
            # health -= 50
            if enemy_bullet.colliderect(space_ship):
                enemy_bullets.remove(enemy_bullet)
                health -= 50 + bullet_damage_inc


    def game_output():
        global space_ship_image
        window.fill(c.SPACE)
        #  drawing the lists of objects
        for bullet in bullets:
            pg.draw.rect(window, c.BULLET_COLOR, bullet)
        for enemy_bullet in enemy_bullets:
            pg.draw.rect(window, c.ENEMY_BULLET_COLOR, enemy_bullet)
        for enemy_list in enemies:
            for enemy in enemy_list:
                if enemy_list == basic_enemies:
                    window.blit(c.BASIC_ENEMY_IMAGE, enemy)
                elif enemy_list == fast_enemies:
                    window.blit(c.FAST_ENEMY_IMAGE, enemy)
                elif enemy_list == heavy_enemies:
                    window.blit(c.HEAVY_ENEMY_IMAGE, enemy)

                # enemy health bars
                pg.draw.rect(window, (255, 0, 0), (enemy.x + 10, enemy.y - 20, c.IMAGE_SIZE - 20, 5))
                pg.draw.rect(window, (0, 255, 0), (enemy.x + 10, enemy.y - 20,
                                                   enemies_health[enemies.index(enemy_list)][enemy_list.index(enemy)]
                                                   / enemies_max_health[enemies.index(enemy_list)] *
                                                   (c.IMAGE_SIZE - 20), 5))
        for upgrade in upgrades:
            window.blit(c.UPGRADE_ICON_IMAGE, upgrade)

        #  drawing the allied ship
        window.blit(space_ship_image, (space_ship.x, space_ship.y))

        #  drawing the score
        window.blit(score_Surface, score_Rect)

        #  health bar
        pg.draw.rect(window, (255, 0, 0), (c.SCREEN_OFFSET, c.HEIGHT - 30, c.WIDTH - 2 * c.SCREEN_OFFSET, 10))
        pg.draw.rect(window, (0, 230, 20), (c.SCREEN_OFFSET, c.HEIGHT - 30, health / max_health *
                                            (c.WIDTH - 2 * c.SCREEN_OFFSET), 10))
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
    end_screen = True
    while end_screen:
        game_input()
        window.blit(end_screen_Surface, end_screen_Rect)
        pg.display.flip()
