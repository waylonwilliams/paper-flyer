import pygame

class Player(pygame.sprite.Sprite):
    player_straight_1 = pygame.image.load("graphics/p1.png").convert_alpha()
    player_straight_2 = pygame.image.load("graphics/p2.png").convert_alpha()
    player_up = pygame.image.load("graphics/plane1up.PNG").convert_alpha()
    player_down = pygame.image.load("graphics/plane2down.PNG").convert_alpha()
    player_surfaces = [player_straight_1, player_straight_2, player_up, player_down]

    move_sound = pygame.mixer.Sound("audio/flyingsfx.wav")

    player_group = pygame.sprite.GroupSingle()

    def __init__(self):
        super().__init__()

        self.player_moving = 0 # 0 not moving, 1 up, 2 down
        self.player_animation = 0 # 0 or 1
        self.image = Player.player_surfaces[self.player_animation] # image is the current surface of the sprite
        self.rect = self.image.get_rect(center = (501, 300)) # rect is the rect which image will be displayed on
        self.player_collide_rect = self.rect.copy()
        self.player_collide_rect.update(self.rect.left, self.rect.top + 10, self.rect.width - 30, self.rect.height - 20) # i use this rect for checking if player has collided, otherwise the player box is too large

    def move_player(self):
        if self.rect.left != 15:
            self.rect.left -= 5

        elif self.player_moving != 0:
            if self.player_moving == 1: # player moving up
                self.rect.y -= 5
                self.player_collide_rect.y -= 5
                self.image = Player.player_surfaces[2]

            elif self.player_moving == 2: # player moving down
                self.rect.y += 5
                self.player_collide_rect.y += 5
                self.image = Player.player_surfaces[3]
            
            if self.rect.centery == 100 or self.rect.centery == 300 or self.rect.centery == 500: # when player reaches one of the rows
                self.player_moving = 0
                self.player_collide_rect.update((self.player_collide_rect.left, self.player_collide_rect.top - 5, self.player_collide_rect.width + 15, self.player_collide_rect.height + 10))
                self.image = Player.player_surfaces[self.player_animation]

    def animate_player(self):
        if self.player_animation == 0:
            self.image = Player.player_surfaces[self.player_animation]
            self.player_animation = 1
        else:
            self.image = Player.player_surfaces[self.player_animation]
            self.player_animation = 0

    def reset(self):
        self.rect.midleft = (15, 300)
        self.player_collide_rect.midleft = (15, 300)
        self.image = Player.player_surfaces[self.player_animation]
        if self.player_moving != 0:
            self.player_moving = 0
            self.player_collide_rect.update(self.player_collide_rect.left, self.player_collide_rect.top - 5, self.player_collide_rect.width + 15, self.player_collide_rect.height + 10)

    def start_reset(self):
        self.rect.center = (501, 300)
        self.player_collide_rect.midleft = (15, 300)
        self.image = Player.player_surfaces[self.player_animation]
        if self.player_moving != 0:
            self.player_moving = 0
            self.player_collide_rect.update(self.player_collide_rect.left, self.player_collide_rect.top - 5, self.player_collide_rect.width + 15, self.player_collide_rect.height + 10)

    def key_pressed(self, event):
        if event == pygame.K_UP: # up arrow key
            if self.rect.centery != 100: # can't move up if at the top
                if self.player_moving == 0: # not currently moving
                    self.player_moving = 1 # player moving state is now up
                    self.player_collide_rect.update(self.player_collide_rect.left, self.player_collide_rect.top + 5, self.player_collide_rect.width - 15, self.player_collide_rect.height - 10)
                    Player.move_sound.play()
                    Player.move_sound.fadeout(750)

        if event == pygame.K_DOWN: # down arrow key
            if self.rect.centery !=  500: # can't move down if at the bottom
                if self.player_moving == 0: # not currently moving
                    self.player_moving = 2 # player moving state is now down
                    self.player_collide_rect.update(self.player_collide_rect.left, self.player_collide_rect.top + 5, self.player_collide_rect.width - 15, self.player_collide_rect.height - 10)
                    Player.move_sound.play()
                    Player.move_sound.fadeout(750)