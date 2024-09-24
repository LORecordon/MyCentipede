
import pygame


class Explotion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.center = center
        self.frame = 0
        self.images = ["images/explosion1.png", "images/explosion2.png", "images/explosion3.png", "images/explosion4.png"]
        self.image = pygame.image.load(self.images[self.frame])
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def update(self):
        self.frame += 1
        if self.frame >= len(self.images):
            self.kill()
        else:
            self.image = pygame.image.load(self.images[self.frame])
            self.rect = self.image.get_rect()
            self.rect.center = self.center
    