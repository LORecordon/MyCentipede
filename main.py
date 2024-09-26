import pygame
import random
import time


from player import Player
from bullet import Bullet
from centipede import Centipede
from mushroom import Mushroom
from spider import Spider
from faller import Faller
from explotion import Explotion

pygame.init()
pygame.mixer.init()

MAIN_VOLUME = 0.1


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

def create_reversed_centipede(screen, level, body_parts):
    centipede_segments = []
    offset = screen.get_width() - 16 * (body_parts + 2)
    head = False
    for num in range(body_parts):
        segment = Centipede(screen, offset, head, level)
        centipede_segments.append(segment)
        offset += 16
        if num == body_parts - 2:
            head = True
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

def menu():
    #simple menu with start and quit and 3 types of difficulty to choose from

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Centipede")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background = pygame.transform.scale(background, (640, 480))
    background.fill((0, 0, 0))

    #use image for background
    background = pygame.image.load("images/bg.jpg")
    background = pygame.transform.scale(background, (800, 600))

    select_sound = pygame.mixer.Sound("sounds/menu.mp3")
    select_sound.set_volume(MAIN_VOLUME)







    title_font = pygame.font.Font(None, 72)
    main_font = pygame.font.Font(None, 46)
    dif_font = pygame.font.Font(None, 36)

    title = title_font.render("Centipede", 1, (30, 200, 30))
    start = main_font.render("Start", 1, (255, 255, 255))
    quit = main_font.render("Quit", 1, (255, 255, 255))

    easy = dif_font.render("Easy", 1, (100, 255, 100))
    medium = dif_font.render("Medium", 1, (100, 100, 255))
    hard = dif_font.render("Hard", 1, (255, 100, 100))

    

    clock = pygame.time.Clock()
    exit = False

    difficulty = 1

    while not exit:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (0, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= event.pos[0] <= 350 and 250 <= event.pos[1] <= 300:
                    return (1, difficulty)
                if 450 <= event.pos[0] <= 550 and 250 <= event.pos[1] <= 300:
                    select_sound.play()
                    return (0, 0)
                if 100 <= event.pos[0] <= 310 and 350 <= event.pos[1] <= 400:
                    select_sound.play()
                    difficulty = 1
                if 300 <= event.pos[0] <= 510 and 350 <= event.pos[1] <= 400:
                    select_sound.play()
                    difficulty = 2
                if 500 <= event.pos[0] <= 710 and 350 <= event.pos[1] <= 400:
                    select_sound.play()
                    difficulty = 3

        screen.blit(background, (0, 0))
        screen.blit(title, (270, 100))
        screen.blit(start, (250, 250))
        screen.blit(quit, (450, 250))
        screen.blit(easy, (150, 350))
        screen.blit(medium, (350, 350))
        screen.blit(hard, (550, 350))

        #render green square around the selected difficulty
        if difficulty == 1:
            pygame.draw.rect(screen, (0, 255, 0), (100, 340, 170, 50), 2)
        if difficulty == 2:
            pygame.draw.rect(screen, (0, 255, 0), (315, 340, 170, 50), 2)
        if difficulty == 3:
            pygame.draw.rect(screen, (0, 255, 0), (500, 340, 170, 50), 2)

            

        pygame.display.flip()

    pygame.quit()






def game(difficulty):

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Centipede")
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    health = 3
    level = 1
    points = 0

    player = Player(screen, False, level)
    bullets = pygame.sprite.Group()
    centipede = pygame.sprite.Group(create_centipede(screen, difficulty, 8))
    mushrooms = pygame.sprite.Group(create_mushrooms(50))
    spiders = pygame.sprite.Group(create_spider(screen, level))
    fallers = pygame.sprite.Group(create_faller(screen))
    explosions = pygame.sprite.Group()

    centipedes = [centipede]
    total_centipedes = 1
    allSprites = pygame.sprite.OrderedUpdates(player, centipedes, centipede, mushrooms, bullets, spiders, fallers)

    shoot_sound = pygame.mixer.Sound("sounds/shoot.mp3")
    shoot_sound.set_volume(MAIN_VOLUME)
    spider_sound = pygame.mixer.Sound("sounds/spider.mp3")
    spider_sound.set_volume(MAIN_VOLUME)
    faller_sound = pygame.mixer.Sound("sounds/faller.mp3")
    faller_sound.set_volume(MAIN_VOLUME)
    death_sound = pygame.mixer.Sound("sounds/death.mp3")
    death_sound.set_volume(MAIN_VOLUME)
    centipede_sound = pygame.mixer.Sound("sounds/centipede.mp3")
    centipede_sound.set_volume(MAIN_VOLUME)
    centipede_death_sound = pygame.mixer.Sound("sounds/centipede_death.mp3")
    centipede_death_sound.set_volume(MAIN_VOLUME)


    spider_timer = time.time()
    faller_timer = time.time()
    if difficulty == 1:
        spider_interval = 20
        faller_interval = 25
    if difficulty == 2:
        spider_interval = 15
        faller_interval = 20
    if difficulty == 3:
        spider_interval = 8
        faller_interval = 10

    timer_centipede_2 = time.time()
    cent2created = False
    timer_centipede_3 = time.time()
    cent3created = False
    respawn_timer = time.time()


    clock = pygame.time.Clock()
    stop = False
    death = False

    while not stop:

        if difficulty == 1:
            spider_interval = 20 - level 
            if spider_interval < 15:
                spider_interval = 15
            faller_interval = 25 - level
            if faller_interval < 15:
                faller_interval = 15
        if difficulty == 2:
            spider_interval = 15 - level
            if spider_interval < 8:
                spider_interval = 8
            faller_interval = 20 - level
            if faller_interval < 10:
                faller_interval = 10
        if difficulty == 3:
            spider_interval = 8 - level
            if spider_interval < 5:
                spider_interval = 5
            faller_interval = 10 - level
            if faller_interval < 5:
                faller_interval = 5



        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True

        #CENTIPEDE x MUSHROOM 
        for i in centipedes:
            for segment in i:
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
                        x_pos = mushroom.rect.right - mushroom.rect.right % 16 - 8
                        y_pos = mushroom.rect.top - mushroom.rect.top % 16 + 4
                        explosion = Explotion((x_pos, y_pos))
                        explosions.add(explosion)
                        allSprites.add(explosions)
                              

        #BULLET x CENTIPEDE
        for bullet in bullets:
            for i in centipedes:
                hited_segment = pygame.sprite.spritecollide(bullet, i, True)
                if hited_segment:
                    for segment in hited_segment:
                        mushroom = Mushroom(segment.rect.right, segment.rect.top)
                        mushrooms.add(mushroom)
                        allSprites.add(mushrooms)
                        bullet.kill()
                        points += segment.get_points()
                        centipede_sound.play()


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
                #explode spider
                x_pos = hited_spider[0].rect.right - hited_spider[0].rect.right % 16
                y_pos = hited_spider[0].rect.top - hited_spider[0].rect.top % 16
                explosion = Explotion((x_pos, y_pos))
                explosions.add(explosion)
                allSprites.add(explosions)
                spider_sound.play()




        #PLAYER x CENTIPEDE
        for i in centipedes:
            for segment in i:
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
                #explode faller
                x_pos = hited_faller[0].rect.right - hited_faller[0].rect.right % 16
                y_pos = hited_faller[0].rect.top - hited_faller[0].rect.top % 16
                explosion = Explotion((x_pos, y_pos))
                explosions.add(explosion)
                allSprites.add(explosions)
                faller_sound.play()

        
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
    
                    


        if not death or time.time() - respawn_timer < 2:
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
                shoot_sound.play()
            death = False
        else:
            respawn_timer = time.time()
            health -= 1
            death_sound.play()
            if health == 0:
                return game_over(points)
            
            #explode player
            x_pos = player.rect.right - player.rect.right % 16
            y_pos = player.rect.top - player.rect.top % 16
            explosion = Explotion((x_pos, y_pos))
            explosions.add(explosion)
            allSprites.add(explosions)
            #remove current player and create new player
            player.kill()
            player = Player(screen, False, level)
            allSprites.add(player)
            death = False

        if not cent2created:
            #if difficulty is 2 create new centipede after timer_centipede_2 > 5
            if difficulty >= 2 and time.time() - timer_centipede_2 > 6:
                timer_centipede_2 = time.time()
                centipede = pygame.sprite.Group(create_centipede(screen, difficulty, 8))
                centipedes.append(centipede)
                allSprites.add(centipede)
                cent2created = True
                total_centipedes += 1

        if not cent3created:
            #if difficulty is 3 create new centipede after timer_centipede_3 > 10
            if difficulty == 3 and time.time() - timer_centipede_3 > 12:
                timer_centipede_3 = time.time()
                centipede = pygame.sprite.Group(create_centipede(screen, difficulty, 8))
                centipedes.append(centipede)
                allSprites.add(centipede)
                cent3created = True
                total_centipedes += 1

        #if centipede reaches bottom of screen delete all centipede segments
        for i in centipedes: 
            for segment in i:
                if segment.rect.bottom >= screen.get_height():
                    segment.kill()
            if len(i) == 0:
                centipedes.remove(i)
                centipede_death_sound.play()

        


        for i in centipedes:
            if len(i) == 0:
                centipedes.remove(i)

        if len(centipedes) < total_centipedes:
            #create new centipede
            print("create new centipede")
            centipede = pygame.sprite.Group(create_centipede(screen, difficulty, 8))
            centipedes.append(centipede)
            allSprites.add(centipede)




        #if no centipede segments left create new centipede
        #for i in range(len(centipedes)):
        #    if len(centipedes[i]) == 0:
        #        centipedes.pop(i)
        #        #remove centipede from list
        #        centipede_death_sound.play()
        #        level += 1
        #        centipede = pygame.sprite.Group(create_centipede(screen, difficulty, 8))
        #        allSprites.add(centipede)  
        #        centipedes.append(centipede)

        #if spider timer is up create new spider
        if time.time() - spider_timer > spider_interval:
            spider_timer = time.time()
            spiders.add(create_spider(screen, level))
            allSprites.add(spiders)

        #if faller timer is up create new faller
        if time.time() - faller_timer > faller_interval:
            faller_timer = time.time()
            fallers.add(create_faller(screen))
            allSprites.add(fallers)




        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)   
        draw_points(screen, points)   

        #draw x amount of player.png to represent health in top right corner
        for num in range(health):
            screen.blit(player.image, (screen.get_width() - 50 - num * 20, 10)) 

    
        pygame.display.flip()

def game_over(score):
    #simple game over screen with score and option to play again or quit
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Centipede")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    font = pygame.font.Font(None, 72)
    main_font = pygame.font.Font(None, 46)
    
    title = font.render("Game Over", 1, (255, 0, 0))
    score = font.render("Score: " + str(score), 1, (255, 255, 255))
    play_again = main_font.render("Play Again", 1, (255, 255, 255))
    quit = main_font.render("Quit", 1, (255, 255, 255))

    clock = pygame.time.Clock()
    exit = False

    while not exit:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= event.pos[0] <= 350 and 350 <= event.pos[1] <= 400:
                    return True
                if 450 <= event.pos[0] <= 550 and 350 <= event.pos[1] <= 400:
                    return False

        screen.blit(background, (0, 0))
        screen.blit(title, (270, 100))
        screen.blit(score, (250, 200))
        screen.blit(play_again, (250, 350))
        screen.blit(quit, (450, 350))

        pygame.display.flip()

    pygame.quit()

def main():
    stop = False
    while not stop: 
        selection = menu()
        if selection[0] == 1:
            option = game(selection[1])
            if not option:
                stop = True
        else:
            pygame.quit()

main()