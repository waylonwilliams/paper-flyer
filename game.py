import pygame
from sys import exit
from random import randint

# pygame config
pygame.init()
screen = pygame.display.set_mode((1000, 600))
screen_rect = screen.get_rect(topleft = (0, 0))
pygame.display.set_caption("")

# display must be initialized first for these imports to work
from player import *
from enemy import *
from background import *

pygame.display.set_icon(Player.player_surfaces[2])

# restart function would be nice too

def update_score():
    """
    calculates score based on time passed in the game and puts it to the screen
    """
    score_ms = pygame.time.get_ticks() - start_time
    score_surface = font.render("Score: " + str(score_ms // 1000), False, "black")
    score_rect = score_surface.get_rect(center = (500, 30))
    screen.blit(score_surface, score_rect)
    return score_ms

Player.player_group.add(Player())
clock = pygame.time.Clock()
font = pygame.font.Font("fonts/font1.ttf", 30)

# game state variables
game = False # whether game is running or not
intro = True # whether the game should reroute to the start screen or not
start_time = 0 # initializing variable used to calculate how long the game has been running -> score
speed = 8 # initial speed of enemies, increases as game goes on

# start screen surfaces and rects
start_instructions_surface = font.render("Use the vertical arrow keys to avoid the obstacles", False, "black")
start_instructions_rect = start_instructions_surface.get_rect(center = (500, 100))
starttxt_surface = font.render("Press space to start", False, "black")
starttxt_rect = starttxt_surface.get_rect(center = (500, 500))

# game over screen surfaces and rects
restart_surface = font.render("Restart?", False, "black")
restart_rect = restart_surface.get_rect(midtop = (500, 350))
home_surface = font.render("Start Screen", False, "black")
home_rect = home_surface.get_rect(midtop = (500, 450))

# loose sfx
crumble = pygame.mixer.Sound("audio/papersfx.wav")
game_music = pygame.mixer.Sound("audio/spacemusic.wav")
game_music.set_volume(.2)
start_music = pygame.mixer.Sound("audio/title.wav")
start_music.set_volume(.2)

# event timers
enemy_timer = pygame.USEREVENT + 1 # enemy spawn event
pygame.time.set_timer(enemy_timer, Enemy.spawn_speed)
animation_timer = pygame.USEREVENT + 2 # sprite animation timer
pygame.time.set_timer(animation_timer, 400)
stage_timer = pygame.USEREVENT + 3 # stage update timer
stage = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close window event
            pygame.quit()
            exit()

        if event.type == animation_timer: # animates player and enemies
                Player.player_group.sprite.animate_player()
                if game:
                    for spr in Enemy.enemy_group:
                        spr.animate()

        if game: # game events
            if event.type == pygame.KEYDOWN: # if key is pressed, for player movement
                Player.player_group.sprite.key_pressed(event.key)

            if event.type == enemy_timer: # enemy spawn
                Enemy.create()

            if event.type == stage_timer: # new stage in game, new background, enemy type, and adjust speeds
                if stage <= 2:
                    new_background = Background(Enemy.speed)
                    new_background.image = Background.backgrounds[stage + 1]
                    new_background.speed = Enemy.speed
                    Background.background_group.add(new_background)
                Enemy.stage_update(stage)
                pygame.time.set_timer(enemy_timer, Enemy.spawn_speed)
                stage += 1

        else: # not game events
            if intro: # start screen
                if event.type == pygame.KEYDOWN: # space bar to start game
                    if event.key == pygame.K_SPACE:
                        game = True
                        intro = False
                        speed = 8
                        spawn_speed = 1400
                        stage = 0
                        pygame.time.set_timer(enemy_timer, spawn_speed)
                        pygame.time.set_timer(stage_timer, 25000)
                        Enemy.current_type = Enemy.bird_surfaces                      
                        Enemy.enemy_group.empty()
                        Enemy.speed = 8
                        Player.player_group.sprite.start_reset()
                        Background.background_group.empty()
                        Background.background_group.add(Background(Enemy.speed))
                        start_music.fadeout(1000)
                        game_music.play(fade_ms=2700)
                        start_time = pygame.time.get_ticks()
            
            else: # restart screen

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos): # redirect to game
                        game = True
                        intro = False
                        speed = 8
                        spawn_speed = 1400
                        stage = 0
                        pygame.time.set_timer(enemy_timer, spawn_speed)
                        pygame.time.set_timer(stage_timer, 25000)
                        Enemy.current_type = Enemy.bird_surfaces
                        Enemy.enemy_group.empty()
                        Enemy.speed = 8
                        Player.player_group.sprite.reset()
                        Background.background_group.empty()
                        Background.background_group.add(Background(Enemy.speed))
                        start_music.fadeout(1000)
                        game_music.play(fade_ms=2700)
                        start_time = pygame.time.get_ticks()

                    elif home_rect.collidepoint(event.pos): # redirect to start screen
                        intro = True

    if game:
        screen.fill("white")

        for spr in Background.background_group:
            spr.update()
        Background.background_group.draw(screen)

        current_score = update_score()

        Player.player_group.sprite.move_player()
        Player.player_group.draw(screen)

        Enemy.enemy_group.update()
        Enemy.enemy_group.draw(screen)

        for spr in Enemy.enemy_group:
            if spr.rect.colliderect(Player.player_group.sprite.player_collide_rect):
                game = False
                game_music.fadeout(1000)
                crumble.play()
                crumble.fadeout(1000)
                break

    else:

        if intro:
            screen.fill("white")

            Player.player_group.sprite.rect.center = (501, 300)
            Player.player_group.draw(screen)
            screen.blit(start_instructions_surface, start_instructions_rect)
            screen.blit(starttxt_surface, starttxt_rect)

            if start_music.get_num_channels() == 0:
                start_music.play(fade_ms=2300, loops=-1)


        else:
            screen.fill("white") 

            endtxt_surface = font.render("You scored: " + str(current_score // 1000), False, "black")
            endtxt_rect = endtxt_surface.get_rect(center = (500, 300))
            screen.blit(endtxt_surface, endtxt_rect)

            pygame.draw.rect(screen, "grey", restart_rect)
            screen.blit(restart_surface, restart_rect)
            pygame.draw.rect(screen, "grey", home_rect)
            screen.blit(home_surface, home_rect)

            if start_music.get_num_channels() == 0:
                start_music.play(fade_ms=2300, loops=-1)

    pygame.display.update()
    clock.tick(60) # sets max frame rate   