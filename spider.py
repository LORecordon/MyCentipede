import pygame
import random



class Spider(pygame.sprite.Sprite):
    def __init__(self, screen, level):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        if level == 1:
            self.x_speed = 2
            self.y_speed = 2
        else:
            self.x_speed = 4
            self.y_speed = 4

        self.image = pygame.image.load("images/spider.png")
        self.rect = self.image.get_rect()
        self.rect.centery = self.screen.get_height() - 56

        if random.randint(0, 1) == 0:
            self.rect.left = 0
        else:
            self.rect.right = self.screen.get_width() - 15
            self.x_speed = -self.x_speed
       
        

    def get_points(self):
        return [200, 400, 600][random.randrange(0, 3)]

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        # Changes the y direction if it goes past the borders
        if self.rect.top <= self.screen.get_height() - 112 or self.rect.bottom >= self.screen.get_height():
            self.y_speed = -self.y_speed

        # Kills the sprite if it goes off the screen
        if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
            self.kill()

