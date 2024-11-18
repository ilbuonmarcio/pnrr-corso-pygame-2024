import pygame
import random
import time

pygame.init()
pygame.font.init()

GAME_RES = WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
FPS = 60
GAME_TITLE = "Primo esempio su PyGame"

text_font = pygame.font.SysFont('Comic Sans MS', 16)

window = pygame.display.set_mode(GAME_RES, pygame.HWACCEL|pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

BG_COLOR = (25, 25, 25)
loops = 1

radius = 5

background_img = pygame.image.load("background.jpg")
player_img = pygame.image.load("player.jpg")
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

player_rect = player_img.get_rect(center=(32, 32))
enemy_rect = enemy_img.get_rect(center=(32, 32))

def get_random_apple():
    apple_rect = apple_img.get_rect(center=(24, 24))
    apple_rect.x = random.randint(48, WINDOW_WIDTH - (48 + 48 + 1))
    apple_rect.y = random.randint(48, WINDOW_HEIGHT - (48 + 48 + 1))
    return apple_rect

player_rect.x = 50
player_rect.y = 50
enemy_rect.x = 550
enemy_rect.y = 50

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
    if keys_pressed[pygame.K_w]:
        player_rect.y -= 5
        player_direction[1] = -1
    elif keys_pressed[pygame.K_s]:
        player_rect.y += 5
        player_direction[1] = +1
    else:
        player_direction[1] = 0
        
    if keys_pressed[pygame.K_a]:
        player_rect.x -= 5
        player_direction[0] = -1
    elif keys_pressed[pygame.K_d]:
        player_rect.x += 5
        player_direction[0] = +1
    else:
        player_direction[0] = 0
        
    if keys_pressed[pygame.K_UP]:
        enemy_rect.y -= 5
        enemy_direction[1] = -1
    elif keys_pressed[pygame.K_DOWN]:
        enemy_rect.y += 5
        enemy_direction[1] = +1
    else:
        enemy_direction[1] = 0
        
    if keys_pressed[pygame.K_LEFT]:
        enemy_rect.x -= 5
        enemy_direction[0] = -1
    elif keys_pressed[pygame.K_RIGHT]:
        enemy_rect.x += 5
        enemy_direction[0] = +1
    else:
        enemy_direction[0] = 0
        
    if keys_pressed[pygame.K_SPACE] and player_direction != [0, 0]:
        player_shooting = True
    else:
        player_shooting = False
        
    if keys_pressed[pygame.K_0] and enemy_direction != [0, 0]:
        enemy_shooting = True
    else:
        enemy_shooting = False
        
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
    
    # Update game logic
    loops += 1
    
    # Aggiungi una mela ogni 5 secondi
    if loops % (FPS * 5) == 0:
        apples.append(get_random_apple())
    
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
    
    # Muoviamo le frecce
    for arrow in arrows:
        arrow[0].x += arrow[1][0] * 8
        arrow[0].y += arrow[1][1] * 8
    
    # Display draw and update
    pygame.Surface.fill(window, BG_COLOR)
    window.blit(background_img, (0, 0))
    
    # Disegno le mele per terra
    for apple_rect in apples:
        window.blit(apple_img, apple_rect)
        
    # Disegno le frecce
    for arrow in arrows:
        window.blit(arrow_img, arrow[0])
    
    window.blit(player_img, player_rect)
    window.blit(enemy_img, enemy_rect)
    
    player_life_label = text_font.render(str(player_life), False, (0, 255, 0))
    enemy_life_label = text_font.render(str(enemy_life), False, (255, 0, 0))
    
    player_coords_label = text_font.render(str((player_rect.x, player_rect.y)), False, (0, 255, 0))
    enemy_coords_label = text_font.render(str((enemy_rect.x, enemy_rect.y)), False, (255, 0, 0))
    
    window.blit(player_life_label, player_rect)
    window.blit(enemy_life_label, enemy_rect)
    
    pygame.draw.circle(window, (0, 255,0), (player_rect.x, player_rect.y), radius)
    pygame.draw.circle(window, (255, 0,0), (enemy_rect.x, enemy_rect.y), radius)
    
    window.blit(player_coords_label, (0, 0))
    window.blit(enemy_coords_label, (0, 20))
    
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()
exit(0)







