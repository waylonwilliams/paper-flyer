# https://www.youtube.com/watch?v=AY9MnQ4x3zk

# intro animation
# high scoresf
# clean background and enemy design transition will be tough, i can do that functionality while waiting for new designs
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


class Player(pygame.sprite.Sprite):
    # straight player images
    player_straight_1 = pygame.image.load("graphics/p1.png").convert_alpha()
    player_straight_2 = pygame.image.load("graphics/p2.png").convert_alpha()

    # player moving images
    player_up = pygame.image.load("graphics/plane1up.PNG").convert_alpha()
    player_down = pygame.image.load("graphics/plane2down.PNG").convert_alpha()

    # all player images, 0 and 1 are animated straight, 2 is up, 3 is down
    player_surfaces = [player_straight_1, player_straight_2, player_up, player_down]

    def __init__(self):
        super().__init__()

        self.player_moving = 0 # 0 not moving, 1 up, 2 down
        self.player_animation = 0 # 0 or 1

        # initializes actual player
        self.image = Player.player_surfaces[self.player_animation] # image is the current surface of the sprite
        self.rect = self.image.get_rect(midleft = (10, 300)) # rect is the rect which image will be displayed on
        self.player_collide_rect = self.rect.copy()
        self.player_collide_rect.update(self.rect.left, self.rect.top + 10, self.rect.width - 30, self.rect.height - 20) # i use this rect for checking if player has collided, otherwise the player box is too large

    def move_player(self):
        # just puts player to screen if its not moving
        if self.player_moving != 0:

            # if up
            if self.player_moving == 1:
                self.rect.y -= 5
                self.player_collide_rect.y -= 5
                self.image = Player.player_surfaces[2]
            # if down
            elif self.player_moving == 2:
                self.rect.y += 5
                self.player_collide_rect.y += 5
                self.image = Player.player_surfaces[3]
            
            # if it reaches one of the 3 rows
            if self.rect.centery == 100 or self.rect.centery == 300 or self.rect.centery == 500:
                self.player_moving = 0
                self.player_collide_rect.update((self.player_collide_rect.left, self.player_collide_rect.top - 5, self.player_collide_rect.width + 15, self.player_collide_rect.height + 10))
                self.image = Player.player_surfaces[self.player_animation]

        # put player to screen
        screen.blit(self.image, self.rect)

    def animate_player(self):
        # switches between animation, timing is done by event loop
        if self.player_animation == 0:
            self.image = Player.player_surfaces[self.player_animation]
            self.player_animation = 1
        else:
            self.image = Player.player_surfaces[self.player_animation]
            self.player_animation = 0

    def reset(self):
        # resets all player values when start or restart button is pressed
        self.rect.midleft = (10, 300)
        self.player_collide_rect.midleft = (10, 300)
        self.image = Player.player_surfaces[self.player_animation]
        if self.player_moving != 0:
            self.player_moving = 0
            self.player_collide_rect.update(self.player_collide_rect.left, self.player_collide_rect.top - 5, self.player_collide_rect.width + 15, self.player_collide_rect.height + 10)


class Enemy(pygame.sprite.Sprite):
    # birds
    bird_1 = pygame.image.load("graphics/bird2.PNG").convert_alpha()
    bird_2 = pygame.image.load("graphics/bird1.PNG").convert_alpha()
    bird_surfaces = [bird_1, bird_2]

    #planes
    plane_1 = pygame.image.load("graphics/temp_plane.png").convert_alpha()
    plane_2 = plane_1
    plane_surfaces = [plane_1, plane_2]

    # rockets
    rocket_1 = pygame.image.load("graphics/rocket1.PNG").convert_alpha()
    rocket_2 = pygame.image.load("graphics/rocket2.PNG").convert_alpha()
    rocket_surfaces = [rocket_1, rocket_2]

    # aliens
    alien_1 = pygame.image.load("graphics/ufo1.PNG").convert_alpha()
    alien_2 = pygame.image.load("graphics/ufo2.PNG").convert_alpha()
    alien_surfaces = [alien_1, alien_2]

    enemy_animation = 0
    spawn_speed = 1400
    speed = 8
    possible_rows = [0, 1]
    prev_row = 2
    current_type = bird_surfaces

    def __init__(self):
        super().__init__()
        
        self.animation = 0
        self.type = Enemy.bird_surfaces
        self.image = Enemy.current_type[self.animation]
        self.rect = self.image.get_rect(midleft = (1200, 100))

        # different surfaces and enemy configs
        # method to move enemies, should be treated as a method for self and by running that on the group it will apply to all
        #   removes them if too far
        # class not self method to create a new enemy and add it to the group?
        # animation for all, switch between current set surfaces list
        # i can have a global variable for the list of surfaces i want to use when producing new enemies and ill change that at the stage event
        # collide checker, checks if self collides with input
        # reset

    def create():

        new_enemy = Enemy()
        new_enemy.type = Enemy.current_type
        new_enemy.image = new_enemy.type[0]
        rand = randint(0, 1)
        new_enemy.rect.midleft = ((1100 + (Enemy.possible_rows[rand] * 200 + 100)), (Enemy.possible_rows[rand] * 200 + 100))
        enemy_group.add(new_enemy)
        Enemy.possible_rows.append(Enemy.prev_row)
        Enemy.prev_row = Enemy.possible_rows.pop(rand)

    def stage_update(stage):

        if stage == 0:
            Enemy.current_type = Enemy.plane_surfaces
        elif stage == 1:        
            Enemy.current_type = Enemy.rocket_surfaces
        elif stage == 2:
            Enemy.current_type = Enemy.alien_surfaces
        # add more types

        if Enemy.spawn_speed > 400:
            Enemy.spawn_speed -= 200
            pygame.time.set_timer(enemy_timer, Enemy.spawn_speed)
        Enemy.speed += 1.5

    def update(self):

        self.rect.left -= Enemy.speed
        screen.blit(self.image, self.rect)
        if self.rect.left < -200:
            enemy_group.remove(self)

    def animate(self):

        if self.animation == 0:
            self.image = self.type[self.animation]
            self.animation = 1
        elif self.animation == 1:
            self.image = self.type[self.animation]
            self.animation = 0


class Background(pygame.sprite.Sprite):
    bird_background = pygame.image.load("graphics/bird_background.png").convert()
    plane_background = pygame.image.load("graphics/plane_background.png").convert()
    rocket_background = pygame.image.load("graphics/rocket_background.png").convert()
    alien_background = pygame.image.load("graphics/alien_background.png").convert()

    def __init__(self):
        super().__init__()
        self.image = Background.bird_background
        self.rect = self.image.get_rect(topleft = (0, 0))

    def stage_update(self, stage):
        if stage == 0:
            self.image = Background.plane_background
        elif stage == 1:
            self.image = Background.rocket_background
        elif stage == 2:
            self.image = Background.alien_background

    def reset(self):
        self.image = Background.bird_background
        self.rect.left = 0

    def update(self):

        screen.blit(self.image, self.rect)
        self.rect.left -= 2
        if self.rect.left <= -1000:
            self.rect.left = 0


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
background_object = Background()
enemy_group = pygame.sprite.Group()
clock = pygame.time.Clock()

# importing font
test_font = pygame.font.Font("fonts/font1.ttf", 30)

# game state variables
game = False # whether game is running or not
intro = True # whether the game should reroute to the start screen or not
start_time = 0 # initializing variable used to calculate how long the game has been running -> score
speed = 8 # initial speed of enemies, increases as game goes on

# start screen surfaces and rects
man_surface = pygame.image.load("graphics/man.jpeg").convert_alpha()
man_rect = man_surface.get_rect(center = (500, 300))
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

            if event.type == animation_timer: # every 400 ms

                player_object.animate_player()
                for spr in enemy_group:
                    spr.animate()

            if event.type == stage_timer:

                background_object.rect.left = 0
                Enemy.stage_update(stage)
                background_object.stage_update(stage)
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
                        background_object.reset()


                        # character position updates, could modularize
                        enemy_group.empty()
                        player_object.reset()


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
                        background_object.reset()


                        # reset positions, can modularize, i guess i won't even need to reset in the future though, clear enemies list ig
                        enemy_group.empty()
                        player_object.reset()


                        # sets new start time to keep track of score
                        start_time = pygame.time.get_ticks()



    ############# GAME SCREEN ##################


    if game:


        # background
        background_object.update()
        # i should change the background surface when stage changes


        # updates score on screen, stores in variable so it can be displayed when game ends
        current_score = update_score()


        # updates player location
        player_object.move_player()

        # moves enemies and saves their new rects for the next iteration
        enemy_group.update()


        
        # checks if player hit an enemy and if so ends the game
        for i in enemy_group:
            if i.rect.colliderect(player_object.player_collide_rect):
                game = False
                break


    ############## START / RESTART SCREENS #####################


    else:


        ############## INTRO SCREEN ##################


        if intro:

            # background
            screen.fill("white")


            # other start screen content
            screen.blit(man_surface, man_rect)
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