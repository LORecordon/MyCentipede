import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, killed, level):
        pygame.sprite.Sprite.__init__(self)

        # Instance variables to keep track of the screen surface, x,y vectors, 
        # whether or not the player sprite is killed and level
        self.screen = screen
        self.x_speed = 4
        self.y_speed = 4
        self.killed = False

        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_width()/2
        self.rect.centery = self.screen.get_height() - 50
        
    def move_up(self):
        '''This method moves the player sprite up by dy.'''
        self.rect.centery -= self.y_speed
    
    def move_down(self):
        '''This method moves the player sprite down by dy.'''
        self.rect.centery += self.y_speed
    
    def move_left(self):
        '''This methods moves the player sprite left by dx.'''
        self.rect.centerx -= self.x_speed
        
    def move_right(self):
        '''This methods moves the player sprite right by dx.'''
        self.rect.centerx += self.x_speed

    def set_killed(self):
        self.killed = True

    def update(self):
        '''This method will be called automatically to reposition the player 
        sprite on the screen and to switch images for death animation.'''
        # top
        if self.rect.top <= (self.screen.get_height() - 112):
            self.rect.top = self.screen.get_height() - 112
        # bottom
        if self.rect.bottom >= self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
        # left
        if self.rect.left <= 0:
            self.rect.left = 0
        # right
        if self.rect.right >= self.screen.get_width():
            self.rect.right = self.screen.get_width()
