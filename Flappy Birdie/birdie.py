# Flappy Birdie

import pygame
import sys
import random


def draw_foreground():
    screen.blit(foreground_surface, (foreground_x_position, 0))
    screen.blit(foreground_surface, (foreground_x_position + 584, -4))


def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_position - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global can_score

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 850:
        can_score = True
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, "Black")
        score_rect = score_surface.get_rect(center=(292, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, "Black")
        score_rect = score_surface.get_rect(center=(292, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, "Black")
        high_score_rect = high_score_surface.get_rect(center=(292, 740))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False

            if pipe.centerx < 0:
                can_score = True


pygame.init()
screen = pygame.display.set_mode((584, 1024))
pygame.display.set_caption("Flappy Birdie")
icon = pygame.image.load("Assets/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
game_font = pygame.font.Font("C:/Windows/Fonts/Impact.ttf", 40)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

background_surface = pygame.image.load("Assets/background.png").convert_alpha()

foreground_surface = pygame.image.load("Assets/foreground.png").convert_alpha()
foreground_x_position = 0

bird_downflap = pygame.image.load("Assets/bird_downflap.png").convert_alpha()
bird_midflap = pygame.image.load("Assets/bird_midflap.png").convert_alpha()
bird_upflap = pygame.image.load("Assets/bird_upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 150)

# bird_surface = pygame.image.load("Assets/bird_midflap.png").convert_alpha()
# bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load("Assets/pipe.png").convert_alpha()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_over_surface = pygame.image.load("Assets/gameover.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(285, 450))

flap_sound = pygame.mixer.Sound("Assets/SFX/sfx_wing.wav")
death_sound = pygame.mixer.Sound("Assets/SFX/sfx_hit.wav")
score_sound = pygame.mixer.Sound("Assets/SFX/sfx_point.wav")
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(background_surface, (0, -30))

    if game_active:
        # Sparrow
        bird_movement += gravity
        rotated_sparrow = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_sparrow, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        pipe_score_check()
        score_display('main_game')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Foreground
    foreground_x_position -= 1
    draw_foreground()
    if foreground_x_position <= -584:
        foreground_x_position = 0

    pygame.display.update()
    clock.tick(120)
