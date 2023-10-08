# https://www.youtube.com/watch?v=AY9MnQ4x3zk

# high scoresf
# if __name__ == "__main__":
#   everything that i currently have outside of a fxn
# enemy size consistency / increasing across stages


import pygame
from sys import exit
from random import randint

# initializing pygame stuff
pygame.init()

# creates the base display
screen = pygame.display.set_mode((1000, 600))
screen_rect = screen.get_rect(topleft = (0, 0))
pygame.display.set_caption("")

from player import *
from enemy import *
from background import *


# restart function would be nice too


def update_score():
    """
    function that increments the score by 1 every second
    """


    # calculate score
    score_ms = pygame.time.get_ticks() - start_time


    # update score on screen
    score_surface = test_font.render("Score: " + str(score_ms // 1000), False, "black")
    score_rect = score_surface.get_rect(center = (500, 30))
    screen.blit(score_surface, score_rect)


    # return score so it saves across fromes
    return score_ms


############################ PYGAME SETUP #############################


player_object = Player()
#background_object = Background()
clock = pygame.time.Clock()

# importing font
test_font = pygame.font.Font("fonts/font1.ttf", 30)

# game state variables
game = False # whether game is running or not
intro = True # whether the game should reroute to the start screen or not
start_time = 0 # initializing variable used to calculate how long the game has been running -> score
speed = 8 # initial speed of enemies, increases as game goes on

# start screen surfaces and rects
start_instructions_surface = test_font.render("Use the vertical arrow keys to avoid the obstacles", False, "black")
start_instructions_rect = start_instructions_surface.get_rect(center = (500, 100))
starttxt_surface = test_font.render("Press space to start", False, "black")
starttxt_rect = starttxt_surface.get_rect(center = (500, 500))

# game over screen surfaces and rects
restart_surface = test_font.render("Restart?", False, "black")
restart_rect = restart_surface.get_rect(midtop = (500, 350))
home_surface = test_font.render("Start Screen", False, "black")
home_rect = home_surface.get_rect(midtop = (500, 450))

# enemy spawn event
enemy_timer = pygame.USEREVENT + 1 # creating a custom pygame event
pygame.time.set_timer(enemy_timer, Enemy.spawn_speed) # creating a timer that ticks every 1.6 seconds, triggers new enemy creation

# animation event
animation_timer = pygame.USEREVENT + 2 # not sure if + 2 or + 1
pygame.time.set_timer(animation_timer, 400)

# stage change timer
stage_timer = pygame.USEREVENT + 3
stage = 0


##################### GAME LOOP ############################


while True:


    for event in pygame.event.get(): # loop through all pygame events

        if event.type == pygame.QUIT: # close window button
            pygame.quit() # opposite of pygame.init()
            exit() # closes the game eloquently rather than just breaking from the while loop


        if event.type == animation_timer: # every 400 ms

                player_object.animate_player()

                if game:

                    for spr in Enemy.enemy_group:
                        spr.animate()


        # these events should only be checked when in game mode
        if game:


            if event.type == pygame.KEYDOWN: # if key is pressed

                if event.key == pygame.K_UP: # up arrow key
                    if player_object.rect.centery != 100: # can't move up if at the top
                        if player_object.player_moving == 0: # not currently moving
                            player_object.player_moving = 1 # player moving state is now up
                            player_object.player_collide_rect.update(player_object.player_collide_rect.left, player_object.player_collide_rect.top + 5, player_object.player_collide_rect.width - 15, player_object.player_collide_rect.height - 10)

                if event.key == pygame.K_DOWN: # down arrow key
                    if player_object.rect.centery !=  500: # can't move down if at the bottom
                        if player_object.player_moving == 0: # not currently moving
                            player_object.player_moving = 2 # player moving state is now down
                            player_object.player_collide_rect.update(player_object.player_collide_rect.left, player_object.player_collide_rect.top + 5, player_object.player_collide_rect.width - 15, player_object.player_collide_rect.height - 10)

            if event.type == enemy_timer: # spawns new enemy

                Enemy.rand = randint(0, 1)
                Enemy.create()

            if event.type == stage_timer:

                # i shouldn't reset the background rect
                if stage <= 2:
                    new_background = Background(Enemy.speed)
                    new_background.image = Background.backgrounds[stage + 1]
                    new_background.speed = Enemy.speed
                    Background.background_group.add(new_background)

                #background_object.rect.left = 0

                Enemy.stage_update(stage)
                pygame.time.set_timer(enemy_timer, Enemy.spawn_speed)
                # add background to group


                #background_object.stage_update(stage)

                stage += 1


        # checked when not in game mode, start / restart screens
        else:


            if not intro:

                # restart button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):


                        # game state updates
                        game = True
                        intro = False
                        speed = 8
                        spawn_speed = 1400
                        pygame.time.set_timer(enemy_timer, spawn_speed)
                        pygame.time.set_timer(stage_timer, 25000)
                        Enemy.current_type = Enemy.bird_surfaces
                        stage = 0
                        # empty background group, or just have bird background inside of it

                        # character position updates, could modularize
                        Enemy.enemy_group.empty()
                        Enemy.speed = 8
                        player_object.reset()
                        Background.background_group.empty()
                        Background.background_group.add(Background(Enemy.speed))


                        # sets a new start time to keep track of score
                        start_time = pygame.time.get_ticks()


                    # start screen button
                    elif home_rect.collidepoint(event.pos):


                        # game state
                        intro = True
            

            else:


                # space bar pressed to start game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        # game states
                        game = True
                        intro = False
                        speed = 8
                        spawn_speed = 1400
                        pygame.time.set_timer(enemy_timer, spawn_speed)
                        pygame.time.set_timer(stage_timer, 25000)
                        Enemy.current_type = Enemy.bird_surfaces
                        stage = 0
                        # empty background group, or just have bird background inside of it
                        
                        #background_object.reset()



                        # reset positions, can modularize, i guess i won't even need to reset in the future though, clear enemies list ig
                        Enemy.enemy_group.empty()
                        Enemy.speed = 8
                        player_object.start_reset()
                        Background.background_group.empty()
                        Background.background_group.add(Background(Enemy.speed))


                        # sets new start time to keep track of score
                        start_time = pygame.time.get_ticks()



    ############# GAME SCREEN ##################


    if game:

        screen.fill("white")


        # background

        #background_object.update()

        for spr in Background.background_group:
            spr.update()
            screen.blit(spr.image, spr.rect)
        # move every item in background 
        # remove when the new one covers whole screen?


        # updates score on screen, stores in variable so it can be displayed when game ends
        current_score = update_score()


        # updates player location
        player_object.move_player()
        screen.blit(player_object.image, player_object.rect)

        # moves enemies and saves their new rects for the next iteration
        Enemy.enemy_group.update()


        
        # checks if player hit an enemy and if so ends the game
        for spr in Enemy.enemy_group:
            screen.blit(spr.image, spr.rect)
            if spr.rect.colliderect(player_object.player_collide_rect):
                game = False
                break


    ############## START / RESTART SCREENS #####################


    else:


        ############## INTRO SCREEN ##################


        if intro:

            # background
            screen.fill("white")


            # other start screen content
            player_object.rect.center = (501, 300)
            screen.blit(player_object.image, player_object.rect)
            screen.blit(start_instructions_surface, start_instructions_rect)
            screen.blit(starttxt_surface, starttxt_rect)


        ############## RESTART SCREEN ####################


        else:


            # background
            screen.fill("white") 


            # text with score
            endtxt_surface = test_font.render("You scored: " + str(current_score // 1000), False, "black")
            endtxt_rect = endtxt_surface.get_rect(center = (500, 300))
            screen.blit(endtxt_surface, endtxt_rect)


            # buttons to restart or go home
            pygame.draw.rect(screen, "grey", restart_rect)
            screen.blit(restart_surface, restart_rect)
            pygame.draw.rect(screen, "grey", home_rect)
            screen.blit(home_surface, home_rect)


    # updates display and caps fps
    pygame.display.update()
    clock.tick(60) # minimum frame rate is not really necessary for a simple 2d game    