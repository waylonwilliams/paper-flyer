import pygame

class Background(pygame.sprite.Sprite):
    bird_background = pygame.image.load("graphics/bird_background.png").convert()
    plane_background = pygame.image.load("graphics/plane_background.png").convert()
    rocket_background = pygame.image.load("graphics/rocket_background.png").convert()
    alien_background = pygame.image.load("graphics/alien_background.png").convert()
    backgrounds = [bird_background, plane_background, rocket_background, alien_background]

    background_group = pygame.sprite.Group()

    def __init__(self, enemy_speed):
        super().__init__()
        self.image = Background.backgrounds[0]
        self.rect = self.image.get_rect(topleft = (1000, 0))
        self.speed = enemy_speed - 1

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

        # after calling this blit every background
        self.rect.left -= self.speed
        if self.rect.left < 0 and self.rect.left > -100:
            self.speed = 2
        if self.rect.left <= -1000:
            if len(Background.background_group) > 1:
                Background.background_group.remove(self)
            else:
                self.rect.left = 0