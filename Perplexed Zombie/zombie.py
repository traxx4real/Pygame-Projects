# Perplexed Zombie

import pygame  # importing the Pygame Library
from sys import exit
from random import randint
from random import choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("Assets/Player1.png").convert_alpha()
        player_walk_2 = pygame.image.load("Assets/Player2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("Assets/Player1.png").convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 540))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("Assets/Jump.mp3")

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 540:
            self.gravity = -23
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 540:
            self.rect.bottom = 540

    def animation_state(self):
        if self.rect.bottom < 540:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "bee":
            bee_1 = pygame.image.load("Assets/Bee1.png").convert_alpha()
            bee_2 = pygame.image.load("Assets/Bee2.png").convert_alpha()
            self.frames = [bee_1, bee_2]
            y_position = 230
        else:
            snail_1 = pygame.image.load("Assets/Snail1.png").convert_alpha()
            snail_2 = pygame.image.load("Assets/Snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_position = 530

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1100, 1300), y_position))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 7
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    main_score = sub_font.render(f'Score: {current_time}', True, "Black")
    score_rect = main_score.get_rect(center=(511, 50))
    screen.blit(main_score, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 7

            if obstacle_rect.bottom == 530:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(bee_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list

    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surface
    global player_index

    if player_rect.bottom < 540:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((1022, 710))
pygame.display.set_caption("Perplexed Zombie")
icon = pygame.image.load("Assets/Icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
main_font = pygame.font.Font("C:/Windows/Fonts/Impact.ttf", 70)
sub_font = pygame.font.Font("C:/Windows/Fonts/Impact.ttf", 40)
game_active = False
start_time = 0
score = 0
BGM = pygame.mixer.Sound("Assets/BGScore.mp3")
BGM.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Background and Foreground
sky = pygame.image.load("Assets/Sky.jpg").convert()
ground = pygame.image.load("Assets/Ground.png").convert_alpha()

# Obstacles
# Snail
snail_frame_1 = pygame.image.load("Assets/Snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("Assets/Snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# Bee
bee_frame_1 = pygame.image.load("Assets/Bee1.png").convert_alpha()
bee_frame_2 = pygame.image.load("Assets/Bee2.png").convert_alpha()
bee_frames = [bee_frame_1, bee_frame_2]
bee_frame_index = 0
bee_surface = bee_frames[bee_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load("Assets/Player1.png").convert_alpha()
player_walk_2 = pygame.image.load("Assets/Player2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("Assets/Player1.png").convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(150, 540))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load("Assets/Stand.png").convert_alpha()
player_stand_rect = player_stand.get_rect(center=(511, 355))

game_name = main_font.render("Perplexed Zombie", True, "#526f39")
game_name_rect = game_name.get_rect(center=(511, 100))

game_message = sub_font.render("Press SPACE to start", True, "#526f39")
game_message_rect = game_message.get_rect(center=(511, 600))

# Timer Mechanic
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 400)

bee_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bee_animation_timer, 100)

while True:
    # all the elements will be drawn in here
    # everything will be updated in here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -23
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 540:
                    player_gravity = -23
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bee', 'snail', 'snail', 'snail'])))
                # if randint(0, 2):
                #     obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(1100, 1300), 530)))
                # else:
                #     obstacle_rect_list.append(bee_surface.get_rect(bottomright=(randint(1100, 1300), 230)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == bee_animation_timer:
                if bee_frame_index == 0:
                    bee_frame_index = 1
                else:
                    bee_frame_index = 0
                bee_surface = bee_frames[bee_frame_index]

    if game_active:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 500))

        # screen.blit(score, score_rect)
        score = display_score()

        # Player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 540:
        #     player_rect.bottom = 540
        # player_animation()
        # screen.blit(player_surface, player_rect)
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle Movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision Mechanic
        game_active = collision_sprite()
        # game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill("#b6fba0")
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (150, 540)
        player_gravity = 0
        score_message = sub_font.render(f"Your Score is {score}", True, "#526f39")
        score_text = sub_font.render(f"Press SPACE to restart", True, "#526f39")
        score_message_rect = score_message.get_rect(center=(511, 580))
        score_text_rect = score_text.get_rect(center=(511, 640))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(score_text, score_text_rect)

    pygame.display.update()  # updates the screen variable
    clock.tick(60)  # this ensures that the while loop doesn't run faster than 60 times per second
