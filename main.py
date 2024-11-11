import pygame

pygame.init()

GAME_RES = WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
FPS = 60
GAME_TITLE = "Primo esempio su PyGame"

window = pygame.display.set_mode(GAME_RES, pygame.HWACCEL|pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

BG_COLOR = (25, 25, 25)
count = 1

radius = 5

player_img = pygame.image.load("player.jpg")
enemy_img = pygame.image.load("enemy.jpg")

player_img = pygame.transform.scale(player_img, (64, 64))
enemy_img = pygame.transform.scale(enemy_img, (64, 64))

player_rect = player_img.get_rect(center=(32, 32))
enemy_rect = enemy_img.get_rect(center=(32, 32))

player_rect.x = 50
player_rect.y = 50
enemy_rect.x = 50
enemy_rect.y = 50

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
    if keys_pressed[pygame.K_s]:
        player_rect.y += 5
    if keys_pressed[pygame.K_a]:
        player_rect.x -= 5
    if keys_pressed[pygame.K_d]:
        player_rect.x += 5
        
    if keys_pressed[pygame.K_UP]:
        enemy_rect.y -= 5
    if keys_pressed[pygame.K_DOWN]:
        enemy_rect.y += 5
    if keys_pressed[pygame.K_LEFT]:
        enemy_rect.x -= 5
    if keys_pressed[pygame.K_RIGHT]:
        enemy_rect.x += 5
    
    # Update game logic
    count += 1
    
    # Display draw and update
    pygame.Surface.fill(window, BG_COLOR)
    
    window.blit(player_img, player_rect)
    window.blit(enemy_img, enemy_rect)
    
    pygame.draw.circle(window, (255, 0, 0), (player_rect.x, player_rect.y), radius)
    pygame.draw.circle(window, (0, 255, 0), (enemy_rect.x, enemy_rect.y), radius)
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
    

    
    

