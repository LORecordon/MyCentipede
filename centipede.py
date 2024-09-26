import pygame


class Centipede(pygame.sprite.Sprite):
    def __init__(self, screen, offset, head, level):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        
        self.offset = offset # The offset of the centipede segment
        self.turn = False
        
        self.level = level #level controls speed
        if self.level == 1:
            self.x_speed = 2
        elif self.level == 2:
            self.x_speed = 4
        elif self.level == 3:
            self.x_speed = 4
        else:
            self.x_speed = 2

        self.head_img = pygame.image.load("images/head.png")
        self.body_img = pygame.image.load("images/body.png")
        self.head = head
        if self.head:
            self.points = 100
            self.image = self.head_img
        else:
            self.points = 10
            self.image = self.body_img

        # Sets the rect attributes for the centipede
        self.rect = self.image.get_rect()
        
        self.rect.right = self.offset + 16
        self.rect.top = 16

    def change_movement(self):
        '''This method lowers the sprite by 16 pixels and changes the x direction.'''
        if self.turn == False:
            self.rect.top += 16
        else:
            self.rect.top -= 16
        self.x_speed = -self.x_speed
    
    def change_direction(self):
        self.x_speed = -self.x_speed
        
    def get_points(self):
        return self.points

    def update(self):
        '''This method will be called automatically to change the image of the 
        centipede(animation) and reposition the centipede sprite on the screen.'''




        self.rect.right += self.x_speed

        # If statement checks that if the centipede has not reached the bottom
        if self.turn == False:
            # checks whether the sprite has hit the left/right of the screen and 
            # lowers the sprite & changes the x direction
            if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
                self.rect.top += 16
                self.x_speed = -self.x_speed
            elif self.rect.bottom == (self.screen.get_height() + 16):
                self.turn = True
                self.rect.top -= 32
                
        # Changes the boundary of the centipede if it has reached the bottom before
        if self.turn:
            if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
                self.rect.top -= 16
                self.x_speed = -self.x_speed
            elif self.rect.top == self.screen.get_height() - 128:
                self.rect.top += 32
                self.turn = False