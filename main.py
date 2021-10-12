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
snail_x_pos = SCREEN_WIDTH-100
snail_x_speed = 4

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,sky_surface.get_height()))
    screen.blit(snail_surface,(snail_x_pos,sky_surface.get_height()-snail_surface.get_height()))

    snail_x_pos -= snail_x_speed
    if snail_x_pos < -snail_surface.get_width():
        snail_x_pos = SCREEN_WIDTH+10
    
    pygame.display.update()
    clock.tick(60)