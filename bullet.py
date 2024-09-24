import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, center, level):
        pygame.sprite.Sprite.__init__(self)
        self.center = center
        self.speed = -15
        self.image = pygame.image.load("images/bullet.png")

        self.rect = self.image.get_rect()

        self.rect.center = self.center


    def update(self):
        self.rect.centery += self.speed
        if self.rect.bottom <= 0:
            self.kill()