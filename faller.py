import pygame
import random


class Faller(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.lives = 2
        self.y_speed = 2
        self.value = random.randrange(0, 641)
        self.y_pos = self.value - self.value % 16

        self.image = pygame.image.load("images/faller.png")
        self.rect = self.image.get_rect()

        self.rect.bottom = 0
        self.rect.right = self.y_pos

    def get_points(self):
        return 200

    def hit(self):
        self.lives -= 1

    def get_lives(self):
        return self.lives

    def update(self):

        self.rect.bottom += self.y_speed

        # Kills the flea sprite if it goes past the screen
        if self.rect.top >= self.screen.get_height():
            self.kill()

        # Doubles the speed of the flea if it has 1 hit point
        if self.lives == 1:
            self.y_speed = 4