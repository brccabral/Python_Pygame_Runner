import pygame
from sys import exit
from random import randint, choice
from typing import List

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk1_surface = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2_surface = pygame.image.load('assets/graphics/Player/player_walk_2.png').convert_alpha()
        self.index_surface = 0
        self.player_walk_surfaces = [player_walk1_surface, player_walk2_surface]
        self.player_jump_surface = pygame.image.load('assets/graphics/Player/jump.png').convert_alpha()
        self.image = self.player_walk_surfaces[self.index_surface]
        self.rect = self.image.get_rect(midbottom = (80,ground_rect.top))
        self.gravity = 0
        self.y_jump = 20

        self.jump_sound = pygame.mixer.Sound('assets/audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= ground_rect.top:
            self.gravity = -self.y_jump
            self.jump_sound.play()

    def reset_pos(self):
        self.gravity = 0
        self.rect.bottom = ground_rect.top

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= ground_rect.top:
            self.rect.bottom = ground_rect.top

    def animation_state(self):
        if self.rect.bottom < ground_rect.top:
            self.image = self.player_jump_surface
        else:
            self.index_surface += 0.1
            if self.index_surface >= len(self.player_walk_surfaces):
                self.index_surface = 0
            self.image = self.player_walk_surfaces[int(self.index_surface)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type: str) -> None:
        super().__init__()
        if type == 'fly':
            fly_frame1_surface = pygame.image.load('assets/graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2_surface = pygame.image.load('assets/graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1_surface, fly_frame2_surface]
            self.x_speed = 8
            self.animation_speed = 0.3
            self.y_pos = ground_rect.top - 90
        else:
            snail_frame1_surface = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
            snail_frame2_surface = pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1_surface, snail_frame2_surface]
            self.x_speed = 6
            self.animation_speed = 0.1
            self.y_pos = ground_rect.top
        
        self.index_surface = 0
        self.image = self.frames[self.index_surface]
        self.rect = self.image.get_rect(bottomleft = (randint(SCREEN_WIDTH+100, SCREEN_WIDTH + 300),self.y_pos))
    
    def animation_state(self):
        self.index_surface += self.animation_speed
        if self.index_surface >= len(self.frames):
            self.index_surface = 0
        self.image = self.frames[int(self.index_surface)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= self.x_speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surface = text_font.render(f'Score: {current_time}', False, GRAY_TEXT)
    score_rect = score_surface.get_rect(center = (SCREEN_WIDTH//2, 50))
    pygame.draw.rect(screen,BLUE_SHADOW,score_rect)
    pygame.draw.rect(screen,BLUE_SHADOW,score_rect,6)
    screen.blit(score_surface, score_rect)
    return current_time

def collisions_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemies_group, False):
        enemies_group.empty()
        return False
    return True

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
background_music = pygame.mixer.Sound('assets/audio/music.wav')
background_music.set_volume(0.5)
background_music.play(loops = -1)

sky_surface = pygame.image.load('assets/graphics/Sky.png').convert()
ground_surface = pygame.image.load('assets/graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(topleft = (0,sky_surface.get_height()))

# Player

player = pygame.sprite.GroupSingle()
player.add(Player())

# Enemies
enemies_group = pygame.sprite.Group()

# Game over player
player_stand = pygame.image.load('assets/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2.5)
player_stand_rect = player_stand.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

game_name = text_font.render('Runner', False, GREEN_SHADOW)
game_name_rect = game_name.get_rect(center = (player_stand_rect.centerx, player_stand_rect.top - 20))

game_message  = text_font.render('Press space or click to start', False, GREEN_SHADOW)
game_message_rect = game_message.get_rect(center = (player_stand_rect.centerx, player_stand_rect.bottom + 30))

# Timers
enemy_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_spawn_timer, 900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == enemy_spawn_timer:
                enemies_group.add(Enemy(choice(['snail','fly'])))
        else:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                start_time = pygame.time.get_ticks()//1000
                playersprite: Player = player.sprites()[0]
                playersprite.reset_pos()
                game_active = True
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,ground_rect)
        score = display_score()

        player.update()
        player.draw(screen)

        enemies_group.draw(screen)
        enemies_group.update()

        game_active = collisions_sprite()
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