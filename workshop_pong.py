import pygame
import time
import math
import random

pygame.init()
pygame.font.init()

GAME_RES = GAME_WIDTH, GAME_HEIGHT = 1280, 720
FPS = 60

BACKGROUND_COLOR = (0, 127, 0)

player_points = 0
enemy_points = 0

def get_sin_background():
    t = time.time()
    return [x * math.sin(math.pi * (t - int(t))) for x in BACKGROUND_COLOR]


screen = pygame.display.set_mode(GAME_RES, pygame.HWACCEL|pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_caption("Pong - Workshop PyGame 2024")
clock = pygame.time.Clock()

text_font = pygame.font.SysFont('Comic Sans MS', 60)

player_img = pygame.transform.scale_by(pygame.image.load("assets/bricks/paddle1_2p.png"), 2)
enemy_img = pygame.transform.scale_by(pygame.image.load("assets/bricks/paddle2_2p.png"), 2)
ball_img = pygame.transform.scale_by(pygame.image.load("assets/ball/ball.png"), 3)
star_img = pygame.image.load("assets/paddle/bullet.png")
star_imgs = [pygame.transform.scale_by(star_img, i) for i in [0.5, 1, 1.5, 2, 2.5, 3, 3.5]]

stars = [random.choice(star_imgs) for i in range(100)]
stars = [[
    star,
    star.get_rect(center=(random.randint(0, GAME_WIDTH), random.randint(0, GAME_HEIGHT))),
    [random.random() * random.choice([-1, 1]), random.random() * random.choice([-1, 1])]
    ]
    for star in stars
]

player_rect = player_img.get_rect(center=(24, GAME_HEIGHT // 2))
enemy_rect = enemy_img.get_rect(center=(GAME_WIDTH - 24, GAME_HEIGHT // 2))
ball_rect = ball_img.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2))
ball_direction = [-1, 1]
ball_speed = 300

players_speed = 500

player_direction = 0
enemy_direction = 0

dt = clock.tick(FPS) / 1000
game_ended = False
while not game_ended:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_ended = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_ended = True
                
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_w]:
        player_rect.y -= players_speed * dt
        player_direction = -1
    elif keys_pressed[pygame.K_s]:
        player_rect.y += players_speed * dt
        player_direction = 1
    else:
        player_direction = 0
        
        
    if keys_pressed[pygame.K_UP]:
        enemy_rect.y -= players_speed * dt
        enemy_direction = -1
    elif keys_pressed[pygame.K_DOWN]:
        enemy_rect.y += players_speed * dt
        enemy_direction = 1
    else:
        enemy_direction = 0
        
    ## Limitiamo il giocatore allo schermo
    if player_rect.y < 0:
        player_rect.y = 0
    if player_rect.y + player_rect.height > GAME_HEIGHT:
        player_rect.y = GAME_HEIGHT - player_rect.height
        
    if enemy_rect.y < 0:
        enemy_rect.y = 0
    if enemy_rect.y + enemy_rect.height > GAME_HEIGHT:
        enemy_rect.y = GAME_HEIGHT - enemy_rect.height
        
    ## HACK
    enemy_rect.y = ball_rect.y
    player_rect.y = ball_rect.y
                
    # Game logic
    ball_rect.x += ball_direction[0] * ball_speed * dt
    ball_rect.y += ball_direction[1] * ball_speed * dt
    
    ## Controlla se rimbalza sui vertici in alto
    if ball_rect.y < 0 or ball_rect.y + ball_rect.height > GAME_HEIGHT:
        ball_direction[1] *= -1
        
    ## Controlla se ha rimbalzato su un player o enemy
    if player_rect.colliderect(ball_rect):
        ball_speed += 50
        ball_direction[0] *= -1
        # Effetto attrito
        if player_direction in [-1, 1]:
            ball_direction[1] = player_direction
    if enemy_rect.colliderect(ball_rect):
        ball_speed += 50
        ball_direction[0] *= -1
        # Effetto attrito
        if enemy_direction in [-1, 1]:
            ball_direction[1] = enemy_direction
        
    ## Controlla se qualcuno ha fatto punto
    if ball_rect.x < 0:
        player_points += 1
        ball_direction = [random.choice([-1, 1]), random.randrange(-45, 45) / 100]
        ball_rect.x = GAME_WIDTH // 2
        ball_rect.y = GAME_HEIGHT // 2
        ball_speed = 300
    if ball_rect.x + ball_rect.width > GAME_WIDTH:
        enemy_points += 1
        ball_direction = [random.choice([-1, 1]), 0]
        ball_rect.x = GAME_WIDTH // 2
        ball_rect.y = GAME_HEIGHT // 2
        ball_speed = 300
                
    # Draw on screen
    screen.fill(get_sin_background())
    
    # Draw stars
    for star in stars:
        star[1].x += star[2][0]
        star[1].y += star[2][1]
        
        if star[1].x < 0 or star[1].x > GAME_WIDTH:
            star[2][0] *= -1
        if star[1].y < 0 or star[1].y > GAME_HEIGHT:
            star[2][1] *= -1
                
        screen.blit(star[0], star[1])
    
    screen.blit(player_img, player_rect)
    screen.blit(enemy_img, enemy_rect)
    screen.blit(ball_img, ball_rect)
    
    player_points_label = text_font.render(f"{player_points}", False, (255, 255, 255))
    enemy_points_label = text_font.render(f"{enemy_points}", False, (255, 255, 255))
    player_points_rect = player_points_label.get_rect(center=(GAME_WIDTH * 0.25, 48))
    enemy_points_rect = enemy_points_label.get_rect(center=(GAME_WIDTH * 0.75, 48))
    
    screen.blit(player_points_label, player_points_rect)
    screen.blit(enemy_points_label, enemy_points_rect)
    
    pygame.display.update()
    dt = clock.tick(FPS) / 1000.0

pygame.quit()
exit(0)
