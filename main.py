import pygame
import random


from player import Player
from bullet import Bullet
from centipede import Centipede
from mushroom import Mushroom
from spider import Spider
from faller import Faller
from explotion import Explotion

pygame.init()
pygame.mixer.init()


"""
TODO:
- Add sound effects
- Add music
- Add levels
- Constant enemy spawn
- Menu
- Game over screen
- High score (maybe)
- Spawn Mushroom in grid
- Dont spawn mushroom on another mushroom
- Difficulty
"""


def draw_points(screen, points):
    font = pygame.font.Font(None, 36)
    text = font.render(str(points), 1, (255, 255, 255))
    screen.blit(text, (10, 10))

def create_centipede(screen, level, body_parts):
    centipede_segments = []
    offset = body_parts * 16
    head = True
    for num in range(body_parts):
        segment = Centipede(screen, offset, head, level)
        centipede_segments.append(segment)
        offset -= 16
        head = False
    return centipede_segments

def create_mushrooms(amount):
    temp = []
    for num in range(amount):
        mushroom = Mushroom(0, 0)
        temp.append(mushroom)
    return temp

def create_spider(screen, level):
    spider = Spider(screen, level)
    return spider

def create_faller(screen):
    faller = Faller(screen)
    return faller


def game():

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Centipede")
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    level = 1
    points = 0

    player = Player(screen, False, level)

    bullets = pygame.sprite.Group()
    centipede = pygame.sprite.Group(create_centipede(screen, 2, 8))
    mushrooms = pygame.sprite.Group(create_mushrooms(50))
    spiders = pygame.sprite.Group(create_spider(screen, level))
    fallers = pygame.sprite.Group(create_faller(screen))
    explosions = pygame.sprite.Group()

    allSprites = pygame.sprite.OrderedUpdates(player, centipede, mushrooms, bullets, spiders, fallers)

    clock = pygame.time.Clock()
    stop = False
    death = False

    while not stop:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True

        #CENTIPEDE x MUSHROOM 
        for segment in centipede:
            if pygame.sprite.spritecollide(segment, mushrooms, False):
                segment.change_movement()
                if pygame.sprite.spritecollide(segment, mushrooms, False):
                    segment.change_movement()
        
        #BULLET x MUSHROOM
        for bullet in bullets:
            hited_mushroom = pygame.sprite.spritecollide(bullet, mushrooms, False)
            if hited_mushroom:
                bullet.kill()
                for mushroom in hited_mushroom:
                    mushroom.hit()
                    if mushroom.get_lives() == 0:
                        points += mushroom.get_points()
                        mushroom.kill()
                        x_pos = mushroom.rect.right - mushroom.rect.right % 16
                        y_pos = mushroom.rect.top - mushroom.rect.top % 16
                        explosion = Explotion((x_pos, y_pos))
                        explosions.add(explosion)
                        allSprites.add(explosions)
                              

        #BULLET x CENTIPEDE
        for bullet in bullets:
            hited_segment = pygame.sprite.spritecollide(bullet, centipede, True)
            if hited_segment:
                for segment in hited_segment:
                    mushroom = Mushroom(segment.rect.right, segment.rect.top)
                    mushrooms.add(mushroom)
                    allSprites.add(mushrooms)
                    bullet.kill()
                    points += segment.get_points()


        #PLAYER x MUSHROOM
        hited_mushroom = pygame.sprite.spritecollide(player, mushrooms, False)
        if hited_mushroom:
            if player.rect.collidepoint(hited_mushroom[0].rect.midleft):
                player.rect.right = hited_mushroom[0].rect.left
            if player.rect.collidepoint(hited_mushroom[0].rect.midright):
                player.rect.left = hited_mushroom[0].rect.right
            if player.rect.collidepoint(hited_mushroom[0].rect.midtop):
                player.rect.bottom = hited_mushroom[0].rect.top
            if player.rect.collidepoint(hited_mushroom[0].rect.midbottom):
                player.rect.top = hited_mushroom[0].rect.bottom

        #PLAYER x SPIDER
        hited_spider = pygame.sprite.spritecollide(player, spiders, True)
        if hited_spider:
            player.set_killed()
            death = True
        
        #BULLET x SPIDER
        for bullet in bullets:
            hited_spider = pygame.sprite.spritecollide(bullet, spiders, True)
            if hited_spider:
                bullet.kill()
                points += hited_spider[0].get_points()

        #PLAYER x CENTIPEDE
        for segment in centipede:
            if player.rect.colliderect(segment.rect):
                player.set_killed()
                death = True
        
        #PLAYER x FALLER
        hited_faller = pygame.sprite.spritecollide(player, fallers, True)
        if hited_faller:
            player.set_killed()
            death = True

        #BULLET x FALLER
        for bullet in bullets:
            hited_faller = pygame.sprite.spritecollide(bullet, fallers, True)
            if hited_faller:
                bullet.kill()
                points += hited_faller[0].get_points()

        
        #FALLER CREATES MUSHROOM
        for faller in fallers:
            if random.randint(0, 3) != 1:
                continue
            if (-2 <= faller.rect.bottom % 16 <= 2) and faller.rect.top <= screen.get_height() - 100:
                y_pos = faller.rect.right - faller.rect.right % 16
                x_pos = faller.rect.top - faller.rect.top % 16
                mushroom = Mushroom(y_pos, x_pos)
                mushrooms.add(mushroom)
                allSprites.add(mushrooms)
    
                    


        if not death:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player.move_up()
            if keys[pygame.K_DOWN]:
                player.move_down()
            if keys[pygame.K_LEFT]:
                player.move_left()
            if keys[pygame.K_RIGHT]:
                player.move_right()
            if keys[pygame.K_SPACE] and len(bullets) <= 0:                 
                missile = Bullet(player.rect.center, level)
                bullets.add(missile)
                allSprites.add(bullets)     


        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)   
        draw_points(screen, points)    

    
        pygame.display.flip()



def main():
    game()
    pygame.quit()

main()