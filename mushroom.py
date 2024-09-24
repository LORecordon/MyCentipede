import pygame
import random


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 4

        if x == 0 and y == 0:
            self.x = self.get_random_position(32, 610)
            self.y = self.get_random_position(80, 500)
        else:
            self.x = x
            self.y = y

        self.images = ["images/mushroom1.png", "images/mushroom2.png", "images/mushroom3.png", "images/mushroom4.png"]
        self.image = pygame.image.load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.right = self.x
        self.rect.top = self.y

    def get_random_position(self, minnum, maxnum):
        temp = random.randrange(minnum, maxnum)
        if temp % 16 != 0:
            temp -= temp % 16
        return temp

    def hit(self):
        self.lives -= 1
        if self.lives == 0:
            self.kill()
        elif self.lives == 1:
            self.image = pygame.image.load(self.images[3])
        elif self.lives == 2:
            self.image = pygame.image.load(self.images[2])
        elif self.lives == 3:
            self.image = pygame.image.load(self.images[1])
        elif self.lives == 4:
            self.image = pygame.image.load(self.images[0])
    
        
    def get_points(self):
        return 1
        
    def get_lives(self):
        return self.lives   

