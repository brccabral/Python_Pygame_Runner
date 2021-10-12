import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GRAY_TEXT = (64,64,64)
BLUE_SHADOW = '#c0e8ec'

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('assets/graphics/Sky.png').convert()
ground_surface = pygame.image.load('assets/graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(topleft = (0,sky_surface.get_height()))

snail_surface = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
snail_x_speed = 4
snail_rect = snail_surface.get_rect(bottomleft = (SCREEN_WIDTH-100,sky_surface.get_height()))

player_surface = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (50,sky_surface.get_height()))
player_jump_y = 20
player_y_pos = 0
player_gravity = 1

score = 0
score_surface = text_font.render(f'Score: {score}', False, GRAY_TEXT)
score_rect = score_surface.get_rect(center = (SCREEN_WIDTH//2, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_y_pos = -player_jump_y
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_y_pos = -player_jump_y
    
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,ground_rect)
    screen.blit(snail_surface,snail_rect)
    pygame.draw.rect(screen,BLUE_SHADOW,score_rect)
    pygame.draw.rect(screen,BLUE_SHADOW,score_rect,6)
    screen.blit(score_surface, score_rect)

    snail_rect.x -= snail_x_speed
    if snail_rect.x < -snail_surface.get_width():
        snail_rect.x = SCREEN_WIDTH+10

    # increases every loop to give gravity feels of acceleration
    player_y_pos += player_gravity
    player_rect.bottom += player_y_pos
    if player_rect.bottom >= ground_rect.top:
        player_rect.bottom = ground_rect.top
    screen.blit(player_surface,player_rect)

    if player_rect.colliderect(snail_rect):
        print('collision')

    pygame.display.update()
    clock.tick(60)