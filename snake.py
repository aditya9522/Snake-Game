import pygame
import random
import time
import os

pygame.mixer.init()
pygame.init()
pygame.display.set_caption("Snake Game")

# initializing variables
screen_width = 600
screen_height = 600
clock = pygame.time.Clock()
fps = 70
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

game_screen = pygame.display.set_mode((screen_width, screen_height))

# background media files loading
playing_background = pygame.image.load('assets/playbg.jpg')
playing_background = pygame.transform.scale(playing_background, (screen_width, screen_height)).convert_alpha()

home_screen_background = pygame.image.load('assets/home.png')
home_screen_background = pygame.transform.scale(home_screen_background, (screen_width, screen_height)).convert_alpha()

game_over_background = pygame.image.load('assets/gameover.png')
game_over_background = pygame.transform.scale(game_over_background, (screen_width, screen_height)).convert_alpha()

playing_music = pygame.mixer.Sound('assets/playsound.mp3')
game_over_music = pygame.mixer.Sound('assets/gameover.wav')

font = pygame.font.SysFont('bungee', 40, 'bold')


def display_text(text, color, x, y):
    data = font.render(text, True, color)
    game_screen.blit(data, [x, y])


def plot_snake(game_window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.ellipse(game_window, color, [x, y, snake_size, snake_size - 8], width=0)


def run_home_screen():
    exit_game = False
    while not exit_game:
        game_screen.blit(home_screen_background, (0, 0))

        # display_text("Welcome To Snake Game", red, 120,100)
        # display_text("Press Space To PLay", green, screen_width/4,250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing_music.play()
                    run_game()

        pygame.display.update()
        clock.tick(fps)


def run_game():
    exit_game = False
    game_over = False

    init_velocity = 4
    velocity_x = 0
    velocity_y = 0
    snake_x = 200
    snake_y = 200
    snake_size = 25

    food_x = random.randint(10, screen_width - 20)
    food_y = random.randint(10, screen_height - 20)
    food_radius = 10
    food_thickness = 0
    pygame.display.update()

    score = 0
    snake_length = 1
    snake_list = []
    if not os.path.exists('high score.txt'):
        with open("high score.txt", "w") as f:
            f.write("0")

    with open("high score.txt") as f:
        high_score = f.read()

    while not exit_game:
        if game_over:
            with open("high score.txt", "w") as f:
                f.write(str(high_score))

            game_screen.blit(game_over_background, (0, 0))
            display_text(f"{score}", blue, 285, 300)
            pygame.time.delay(int(game_over_music.get_length() * 1000))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        playing_music.play()
                        run_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        run_home_screen()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x -= init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y -= init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_l:  # cheat code
                        score += 10

            if abs(snake_x - food_x) < 9 and abs(snake_y - food_y) < 9:
                pygame.mixer.music.load('assets/eat.mp3')
                pygame.mixer.music.play()
                food_x = random.randint(10, screen_width - 20)
                food_y = random.randint(10, screen_height - 20)
                score += 10
                snake_length += 3
                if score > int(high_score):
                    high_score = score

            if len(snake_list) > snake_length:
                del snake_list[0]

            head = [snake_x, snake_y]
            snake_list.append(head)

            if snake_x < 0 or snake_y > screen_height or snake_x > screen_width or snake_y < 0:
                pygame.mixer.music.load('assets/hit.mp3')
                pygame.mixer.music.play()
                playing_music.stop()
                time.sleep(1)
                game_over_music.play()
                game_over = True

            if head in snake_list[:-2]:
                pygame.mixer.music.load('assets/hit.mp3')
                pygame.mixer.music.play()
                playing_music.stop()
                time.sleep(1)
                game_over_music.play()
                game_over = True

            snake_x += velocity_x
            snake_y += velocity_y
            game_screen.blit(playing_background, (0, 0))

            display_text(f"Score: {score}", blue, 10, 10)
            display_text(f"High Score: {high_score}", blue, 375, 10)
            plot_snake(game_screen, green, snake_list, snake_size)
            # pygame.draw.rect(game_screen, green, [snake_x, snake_y, snake_size, snake_size], 0)
            pygame.draw.circle(game_screen, red, [food_x, food_y], food_radius, food_thickness)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


run_home_screen()
