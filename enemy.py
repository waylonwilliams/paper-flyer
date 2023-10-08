import pygame
from random import randint

class Enemy(pygame.sprite.Sprite):
    bird_1 = pygame.image.load("graphics/bird2.PNG").convert_alpha()
    bird_2 = pygame.image.load("graphics/bird1.PNG").convert_alpha()
    bird_surfaces = [bird_1, bird_2]
    plane_1 = pygame.image.load("graphics/temp_plane.png").convert_alpha()
    plane_2 = plane_1
    plane_surfaces = [plane_1, plane_2]
    rocket_1 = pygame.image.load("graphics/rocket1.PNG").convert_alpha()
    rocket_2 = pygame.image.load("graphics/rocket2.PNG").convert_alpha()
    rocket_surfaces = [rocket_1, rocket_2]
    alien_1 = pygame.image.load("graphics/ufo1.PNG").convert_alpha()
    alien_2 = pygame.image.load("graphics/ufo2.PNG").convert_alpha()
    alien_surfaces = [alien_1, alien_2]

    enemy_animation = 0
    spawn_speed = 1400
    speed = 8
    possible_rows = [0, 1]
    prev_row = 2
    current_type = bird_surfaces

    enemy_group = pygame.sprite.Group()

    def __init__(self):
        super().__init__()
        
        self.animation = 0
        self.type = Enemy.bird_surfaces
        self.image = Enemy.current_type[self.animation]
        self.rect = self.image.get_rect(midleft = (1200, 100))

    def create():
        new_enemy = Enemy()
        new_enemy.type = Enemy.current_type
        new_enemy.image = new_enemy.type[0]
        rand = randint(0, 1)
        new_enemy.rect.midleft = ((1100 + (Enemy.possible_rows[rand] * 200 + 100)), (Enemy.possible_rows[rand] * 200 + 100))
        Enemy.enemy_group.add(new_enemy)
        Enemy.possible_rows.append(Enemy.prev_row)
        Enemy.prev_row = Enemy.possible_rows.pop(rand)

    def stage_update(stage):
        if stage == 0:
            Enemy.current_type = Enemy.plane_surfaces
        elif stage == 1:        
            Enemy.current_type = Enemy.rocket_surfaces
        elif stage == 2:
            Enemy.current_type = Enemy.alien_surfaces

        if Enemy.spawn_speed > 400:
            Enemy.spawn_speed -= 200
        Enemy.speed += 2

    def update(self):
        self.rect.left -= Enemy.speed
        if self.rect.left < -200:
            Enemy.enemy_group.remove(self)

    def animate(self):
        if self.animation == 0:
            self.image = self.type[self.animation]
            self.animation = 1
        elif self.animation == 1:
            self.image = self.type[self.animation]
            self.animation = 0