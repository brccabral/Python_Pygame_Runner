import pygame
from sys import exit
from random import randint
from typing import List

def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surface = text_font.render(f'Score: {current_time}', False, GRAY_TEXT)
    score_rect = score_surface.get_rect(center = (SCREEN_WIDTH//2, 50))
    pygame.draw.rect(screen,BLUE_SHADOW,score_rect)
    pygame.draw.rect(screen,BLUE_SHADOW,score_rect,6)
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_rect_list: List[pygame.Rect]):
    if obstacle_rect_list:
        for obs_rect in obstacle_rect_list:
            if obs_rect.bottom < ground_rect.top:
                obs_rect.x -= fly_x_speed
                screen.blit(fly_surface, obs_rect)
            else:
                obs_rect.x -= snail_x_speed
                screen.blit(snail_surface, obs_rect)

        obstacle_rect_list = [obs_rect for obs_rect in obstacle_rect_list if obs_rect.right > -10]

    return obstacle_rect_list

def collisions(player: pygame.Rect, obstacles: List[pygame.Rect]):
    if obstacles:
        for obs_rec in obstacles:
            return not player.colliderect(obs_rec)
    return True

def player_animation():
    global player_surface, player_index_surface
    if player_rect.bottom < ground_rect.top:
        player_surface = player_jump_surface
    else:
        player_index_surface += 0.1
        if player_index_surface >= len(player_walk_surfaces): player_index_surface = 0
        player_surface = player_walk_surfaces[int(player_index_surface)]
    screen.blit(player_surface, player_rect)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GRAY_TEXT = (64,64,64)
BLUE_SHADOW = '#c0e8ec'
GREEN_SHADOW = (111,196,169)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('assets/graphics/Sky.png').convert()
ground_surface = pygame.image.load('assets/graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(topleft = (0,sky_surface.get_height()))

# Enemies
obstacle_rect_list = []

snail_surface = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
snail_x_speed = 6
snail_rect = snail_surface.get_rect(bottomleft = (SCREEN_WIDTH-100,ground_rect.top))

fly_surface = pygame.image.load('assets/graphics/Fly/Fly1.png').convert_alpha()
fly_x_speed = 8
fly_rect = fly_surface.get_rect(bottomleft = (SCREEN_WIDTH-100,ground_rect.top+50))


# Player
player_walk1_surface = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
player_walk2_surface = pygame.image.load('assets/graphics/Player/player_walk_2.png').convert_alpha()
player_index_surface = 0
player_jump_surface = pygame.image.load('assets/graphics/Player/jump.png').convert_alpha()
player_walk_surfaces = [player_walk1_surface, player_walk2_surface]
player_surface = player_walk_surfaces[player_index_surface]
player_rect = player_walk1_surface.get_rect(midbottom = (50,ground_rect.top))
player_jump_y = 20
player_y_pos = 0
player_gravity = 1

# Game over player
player_stand = pygame.image.load('assets/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2.5)
player_stand_rect = player_stand.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

game_name = text_font.render('Runner', False, GREEN_SHADOW)
game_name_rect = game_name.get_rect(center = (player_stand_rect.centerx, player_stand_rect.top - 20))

game_message  = text_font.render('Press space or click to start', False, GREEN_SHADOW)
game_message_rect = game_message.get_rect(center = (player_stand_rect.centerx, player_stand_rect.bottom + 30))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_y_pos = -player_jump_y
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= ground_rect.top:
                    player_y_pos = -player_jump_y
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(SCREEN_WIDTH+100, SCREEN_WIDTH + 300), ground_rect.top)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(SCREEN_WIDTH+100, SCREEN_WIDTH + 300), ground_rect.top-50)))
        else:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                obstacle_rect_list.clear()
                player_rect.bottom = ground_rect.top
                player_y_pos = 0
                start_time = pygame.time.get_ticks()//1000
                game_active = True
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,ground_rect)
        score = display_score()

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # screen.blit(snail_surface,snail_rect)

        # snail_rect.x -= snail_x_speed
        # if snail_rect.right < 0:
        #     snail_rect.left = SCREEN_WIDTH+10

        # increases every loop to give gravity feels of acceleration
        player_y_pos += player_gravity
        player_rect.bottom += player_y_pos
        if player_rect.bottom >= ground_rect.top:
            player_rect.bottom = ground_rect.top
        # screen.blit(player_walk1_surface,player_rect)
        player_animation()

        game_active = collisions(player_rect, obstacle_rect_list)
    else:
        screen.fill(BLUE_SHADOW)
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            score_message = text_font.render(f'Your score: {score}', False, GREEN_SHADOW)
            score_message_rect = score_message.get_rect(center = (SCREEN_WIDTH//2, player_stand_rect.bottom + 30))
            screen.blit(score_message, score_message_rect)

    
    pygame.display.update()
    clock.tick(60)