import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

sky_surface = pygame.image.load('assets/graphics/Sky.png').convert()
ground_surface = pygame.image.load('assets/graphics/ground.png').convert()

snail_surface = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
snail_x_speed = 4
snail_rect = snail_surface.get_rect(bottomleft = (SCREEN_WIDTH-100,sky_surface.get_height()))

player_surface = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (50,sky_surface.get_height()))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos): print('mouse')
    
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,sky_surface.get_height()))
    screen.blit(snail_surface,snail_rect)
    screen.blit(player_surface,player_rect)

    snail_rect.x -= snail_x_speed
    if snail_rect.x < -snail_surface.get_width():
        snail_rect.x = SCREEN_WIDTH+10

    if player_rect.colliderect(snail_rect):
        print('collision')

    pygame.display.update()
    clock.tick(60)