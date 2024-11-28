import pygame
import random
import time
import math

pygame.init()
pygame.font.init()
pygame.mixer.init()

GAME_RES = WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
FPS = 60
GAME_TITLE = "Primo esempio su PyGame"
dt = 1000 / FPS / 1000

text_font = pygame.font.SysFont('Comic Sans MS', 16)
the_end_font = pygame.font.SysFont('Comic Sans MS', 64)

you_won_label = the_end_font.render("YOU WON!", False, (0, 255, 0))
you_lost_label = the_end_font.render("YOU LOST!", False, (255, 0, 0))

you_won_rect = you_won_label.get_rect()
you_lost_rect = you_lost_label.get_rect()

you_won_rect.x = (WINDOW_WIDTH // 2) - (you_won_rect.width // 2)
you_won_rect.y = (WINDOW_HEIGHT // 2) - (you_won_rect.height // 2)
you_lost_rect.x = (WINDOW_WIDTH // 2) - (you_lost_rect.width // 2)
you_lost_rect.y = (WINDOW_HEIGHT // 2) - (you_lost_rect.height // 2)

window = pygame.display.set_mode(GAME_RES, pygame.HWACCEL|pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

background_music = pygame.mixer.music.load("background.mp3", "mp3")
arrow_sound = pygame.mixer.Sound("arrow.ogg")
fireball_sound = pygame.mixer.Sound("fireball.wav")

BG_COLOR = (25, 25, 25)
loops = 1
who_won = None

radius = 5

background_img = pygame.image.load("background.jpg")
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
apple_img = pygame.image.load("apple.png")
arrow_img = pygame.image.load("arrow.png")
fireball_img = pygame.image.load("fireball.png")

background_img = pygame.transform.scale(background_img, GAME_RES)
player_img = pygame.transform.scale(player_img, (64, 64))
enemy_img = pygame.transform.scale(enemy_img, (64, 64))
apple_img = pygame.transform.scale(apple_img, (48, 48))
arrow_img = pygame.transform.scale(arrow_img, (48, 48))
fireball_img = pygame.transform.scale(fireball_img, (48, 48))

arrow_img_directed = {
    (0, 0): arrow_img,
    (1, 0): arrow_img,
    (0, 1): pygame.transform.rotate(arrow_img, -90),
    (1, 1): pygame.transform.rotate(arrow_img, -45),
    (1, -1): pygame.transform.rotate(arrow_img, 45),
    (0, -1): pygame.transform.rotate(arrow_img, 90),
    (-1, -1): pygame.transform.rotate(arrow_img, 135),
    (-1, 0): pygame.transform.rotate(arrow_img, -180),
    (-1, 1): pygame.transform.rotate(arrow_img, -135)
}

fireball_img_directed = {
    (0, 0): fireball_img,
    (1, 0): fireball_img,
    (0, 1): pygame.transform.rotate(fireball_img, -90),
    (1, 1): pygame.transform.rotate(fireball_img, -45),
    (1, -1): pygame.transform.rotate(fireball_img, 45),
    (0, -1): pygame.transform.rotate(fireball_img, 90),
    (-1, -1): pygame.transform.rotate(fireball_img, 135),
    (-1, 0): pygame.transform.rotate(fireball_img, -180),
    (-1, 1): pygame.transform.rotate(fireball_img, -135)
}

player_rect = player_img.get_rect(center=(32, 32))
enemy_rect = enemy_img.get_rect(center=(32, 32))

def get_random_apple():
    apple_rect = apple_img.get_rect(center=(24, 24))
    apple_rect.x = random.randint(48, WINDOW_WIDTH - (48 + 48 + 1))
    apple_rect.y = random.randint(48, WINDOW_HEIGHT - (48 + 48 + 1))
    return apple_rect

player_rect.x = 50
player_rect.y = 50
enemy_rect.x = WINDOW_WIDTH // 2
enemy_rect.y = WINDOW_HEIGHT // 2

player_movespeed = 200 * dt
enemy_movespeed = 200 * dt

player_life = 5
enemy_life = 5

player_direction = [1, 0]
enemy_direction = [-1, 0]
player_shooting = False
enemy_shooting = False


player_shoot_timeout = time.time()
enemy_shoot_timeout = time.time()


apples = []
apples.append(get_random_apple())

arrows = []
fireballs = []

pygame.mixer.music.play(loops=-1)

game_ended = False
while not game_ended:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_ended = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_ended = True
                
    keys_pressed = pygame.key.get_pressed()
    
    if who_won is None:
        if keys_pressed[pygame.K_w]:
            player_rect.y -= player_movespeed
            player_direction[1] = -1
        elif keys_pressed[pygame.K_s]:
            player_rect.y += player_movespeed
            player_direction[1] = +1
        else:
            player_direction[1] = 0
            
        if keys_pressed[pygame.K_a]:
            player_rect.x -= player_movespeed
            player_direction[0] = -1
        elif keys_pressed[pygame.K_d]:
            player_rect.x += player_movespeed
            player_direction[0] = +1
        else:
            player_direction[0] = 0
        
        """
        if keys_pressed[pygame.K_UP]:
            enemy_rect.y -= enemy_movespeed
            enemy_direction[1] = -1
        elif keys_pressed[pygame.K_DOWN]:
            enemy_rect.y += enemy_movespeed
            enemy_direction[1] = +1
        else:
            enemy_direction[1] = 0
            
        if keys_pressed[pygame.K_LEFT]:
            enemy_rect.x -= enemy_movespeed
            enemy_direction[0] = -1
        elif keys_pressed[pygame.K_RIGHT]:
            enemy_rect.x += enemy_movespeed
            enemy_direction[0] = +1
        else:
            enemy_direction[0] = 0
        """
        
    if keys_pressed[pygame.K_SPACE] and player_direction != [0, 0]:
        player_shooting = True
    else:
        player_shooting = False
    
    """
    if keys_pressed[pygame.K_m] and enemy_direction != [0, 0]:
        enemy_shooting = True
    else:
        enemy_shooting = False
    """
    
    # Update game logic
    loops += 1
    
    # Aggiungi una mela ogni 5 secondi
    if who_won is None:
        if loops % (FPS * 5) == 0:
            apples.append(get_random_apple())
            
    # INTELLIGENZA ARTIFICIALE DEL NEMICO
    if who_won is None:
        if loops % (FPS * 1) == 0:
            enemy_direction[0] = random.choice([-1, 0, 1])
            enemy_direction[1] = random.choice([-1, 0, 1])
        if round(time.time()) % 3 == 0:
            enemy_rect.x += enemy_direction[0] * enemy_movespeed
            enemy_rect.y += enemy_direction[1] * enemy_movespeed
        if round(time.time()) % 3 == 0 and enemy_direction != [0, 0]:
            if player_direction != [0, 0]:
                enemy_direction = [player_direction[0] * -1, player_direction[1] * -1]
            enemy_shooting = True
        else:
            enemy_shooting = False
    # INTELLIGENZA ARTIFICIALE DEL NEMICO
    
    # Controllo che le coordinate non escano dallo schermo
    if player_rect.x < 0:
        player_rect.x = 0
    if player_rect.x > WINDOW_WIDTH - player_rect.width:
        player_rect.x = WINDOW_WIDTH - player_rect.width
    if player_rect.y < 0:
        player_rect.y = 0
    if player_rect.y > WINDOW_HEIGHT - player_rect.height:
        player_rect.y = WINDOW_HEIGHT - player_rect.height
        
    if enemy_rect.x < 0:
        enemy_rect.x = 0
    if enemy_rect.x > WINDOW_WIDTH - enemy_rect.width:
        enemy_rect.x = WINDOW_WIDTH - enemy_rect.width
    if enemy_rect.y < 0:
        enemy_rect.y = 0
    if enemy_rect.y > WINDOW_HEIGHT - enemy_rect.height:
        enemy_rect.y = WINDOW_HEIGHT - enemy_rect.height
    
    # Controllo che il giocatore abbia mangiato una mela
    for apple_rect in apples:
        if player_rect.colliderect(apple_rect):
            player_life += 1
            if apple_rect in apples:
                apples.remove(apple_rect)
        if enemy_rect.colliderect(apple_rect):
            enemy_life += 1
            if apple_rect in apples:
                apples.remove(apple_rect)
                
    # Se ci sono proiettili da generare, generali
    if player_shooting and time.time() - player_shoot_timeout > 0.75:
        arrow_rect = arrow_img.get_rect(center=(24, 24))
        arrow_rect.x = player_rect.x
        arrow_rect.y = player_rect.y
        arrows.append([arrow_rect, (player_direction[0], player_direction[1])])
        player_shoot_timeout = time.time()
        pygame.mixer.Sound.play(arrow_sound)
        
    if enemy_shooting and time.time() - enemy_shoot_timeout > 0.75:
        fireball_rect = fireball_img.get_rect(center=(24, 24))
        fireball_rect.x = enemy_rect.x
        fireball_rect.y = enemy_rect.y
        fireballs.append([fireball_rect, (enemy_direction[0], enemy_direction[1])])
        enemy_shoot_timeout = time.time()
        pygame.mixer.Sound.play(fireball_sound)
    
    # Muoviamo le frecce
    for arrow in arrows:
        arrow[0].x += arrow[1][0] * 240 * dt
        arrow[0].y += arrow[1][1] * 240 * dt
        
    for fireball in fireballs:
        fireball[0].x += fireball[1][0] * 240 * dt
        fireball[0].y += fireball[1][1] * 240 * dt
        
    # Controlliamo i conflitti con le frecce
    for arrow in arrows:
        if arrow[0].colliderect(enemy_rect):
            enemy_life -= 1
            if arrow in arrows:
                arrows.remove(arrow)
                
    for fireball in fireballs:
        if fireball[0].colliderect(player_rect):
            player_life -= 1
            if fireball in fireballs:
                fireballs.remove(fireball)
                
    if who_won is None:
        if player_life <= 0:
            who_won = "enemy"
        if enemy_life <= 0:
            who_won = "player"
    
    # Display draw and update
    pygame.Surface.fill(window, BG_COLOR)
    window.blit(background_img, (0, 0))
    
    # Disegno le mele per terra
    for apple_rect in apples:
        window.blit(apple_img, apple_rect)
        
    # Disegno le frecce
    for arrow in arrows:
        window.blit(arrow_img_directed[arrow[1]], arrow[0])
        
    for fireball in fireballs:
        window.blit(fireball_img_directed[fireball[1]], fireball[0])
    
    window.blit(player_img, (math.ceil(player_rect.x), math.ceil(player_rect.y)))
    window.blit(enemy_img, (math.ceil(enemy_rect.x), math.ceil(enemy_rect.y)))
    
    player_life_label = text_font.render(str(player_life), False, (0, 255, 0))
    enemy_life_label = text_font.render(str(enemy_life), False, (255, 0, 0))
    
    # player_coords_label = text_font.render(str((player_rect.x, player_rect.y)), False, (0, 255, 0))
    # enemy_coords_label = text_font.render(str((enemy_rect.x, enemy_rect.y)), False, (255, 0, 0))
    
    window.blit(player_life_label, player_rect)
    window.blit(enemy_life_label, enemy_rect)
    
    # pygame.draw.circle(window, (0, 255,0), (player_rect.x, player_rect.y), radius)
    # pygame.draw.circle(window, (255, 0,0), (enemy_rect.x, enemy_rect.y), radius)
    
    # window.blit(player_coords_label, (0, 0))
    # window.blit(enemy_coords_label, (0, 20))
    
    if who_won is not None:
        if who_won == "player":
            window.blit(you_won_label, you_won_rect)
        if who_won == "enemy":
            window.blit(you_lost_label, you_lost_rect)
    
    pygame.display.update()
    dt = clock.tick(FPS)
    dt /= 1000
    
pygame.quit()
exit(0)







