import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍 Levels")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)
over_font = pygame.font.SysFont(None, 60)

def draw_score_level(score, level):
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(score, level):
    screen.fill(BLACK)
    over_text = over_font.render("Game Over!", True, RED)
    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 60))
    score_text = font.render(f"Final Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    info_text = font.render("Press R to Play Again or Q to Quit", True, WHITE)
    screen.blit(info_text, (WIDTH//2 - info_text.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def generate_obstacles(num_obstacles, snake, food):
    obstacles = []
    while len(obstacles) < num_obstacles:
        pos = (random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
               random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE)
        if pos not in snake and pos != food and pos not in obstacles:
            obstacles.append(pos)
    return obstacles

def play_game():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = RIGHT
    food = (random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
            random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE)
    score = 0
    speed = 10
    level = 1
    points_per_level = 5  

    obstacles = generate_obstacles(level * 5, snake, food) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

        head_x, head_y = snake[0]
        new_head = (head_x + direction[0] * CELL_SIZE,
                    head_y + direction[1] * CELL_SIZE)
        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            food = (random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE)
            speed = 10 + score // 3 

           
            if score % points_per_level == 0:
                level += 1
                obstacles = generate_obstacles(level * 5, snake, food) 

        else:
            snake.pop()

        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT or
            snake[0] in snake[1:] or
            snake[0] in obstacles):
            return score, level

        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
        obstacle_color = GRAY if level % 3 == 1 else YELLOW if level % 3 == 2 else BLUE
        for obs in obstacles:
            pygame.draw.rect(screen, obstacle_color, (*obs, CELL_SIZE, CELL_SIZE))
        draw_score_level(score, level)

        pygame.display.flip()
        clock.tick(speed)

while True:
    final_score, final_level = play_game()
    play_again = game_over_screen(final_score, final_level)
    if not play_again:
        break

