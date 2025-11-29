import pygame
import os
from random import randint

# Initialize pygame
pygame.init()

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Flight")

# Load images safely
def load_image(path):
    if not os.path.exists(path):
        print(f"ERROR: '{path}' is missing!")
        exit()
    return pygame.image.load(path)

# Load game assets
background = load_image("images/background.png")
balloon_image = load_image("images/balloon.png")
bird_image = load_image("images/bird-up.png")
house_image = load_image("images/house.png")
tree_image = load_image("images/tree.png")

# Set initial positions
balloon_rect = balloon_image.get_rect(center=(400, 300))
bird_rect = bird_image.get_rect(topleft=(randint(800, 1600), randint(10, 200)))
house_rect = house_image.get_rect(topleft=(randint(800, 1600), 460))
tree_rect = tree_image.get_rect(topleft=(randint(800, 1600), 450))

# Game variables
bird_up = True
up = False
game_over = False
score = 0
number_of_updates = 0

# Load high scores
scores = []
filename = "high-scores.txt"

if os.path.exists(filename):
    with open(filename, "r") as file:
        scores = [int(score) for score in file.read().split()]
else:
    with open(filename, "w") as file:
        file.write("0 0 0 0 0")

# Update high scores
def update_high_scores():
    global score, scores
    scores.append(score)
    scores = sorted(scores, reverse=True)[:5]
    with open(filename, "w") as file:
        file.write(" ".join(map(str, scores)))

# Display high scores
def display_high_scores():
    font = pygame.font.Font(None, 36)
    screen.fill((255, 255, 255))
    title = font.render("HIGH SCORES", True, (0, 0, 0))
    screen.blit(title, (350, 150))
    y = 175
    for i, high_score in enumerate(scores, start=1):
        score_text = font.render(f"{i}. {high_score}", True, (0, 0, 0))
        screen.blit(score_text, (350, y))
        y += 25
    pygame.display.update()

# Draw function
def draw():
    screen.blit(background, (0, 0))
    if not game_over:
        screen.blit(balloon_image, balloon_rect)
        screen.blit(bird_image, bird_rect)
        screen.blit(house_image, house_rect)
        screen.blit(tree_image, tree_rect)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (700, 5))
    else:
        display_high_scores()
    pygame.display.update()

# Mouse controls
def on_mouse_down():
    global up
    up = True
    balloon_rect.y -= 50

def on_mouse_up():
    global up
    up = False

# Bird animation
def flap():
    global bird_up, bird_image
    if bird_up:
        bird_image = load_image("images/bird-down.png")
        bird_up = False
    else:
        bird_image = load_image("images/bird-up.png")
        bird_up = True

# Game update function
def update():
    global game_over, score, number_of_updates

    if not game_over:
        # Balloon falls if not moving up
        if not up:
            balloon_rect.y += 1

        # Move bird
        if bird_rect.x > 0:
            bird_rect.x -= 4
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            bird_rect.x = randint(800, 1600)
            bird_rect.y = randint(10, 200)
            score += 1
            number_of_updates = 0

        # Move house
        if house_rect.right > 0:
            house_rect.x -= 2
        else:
            house_rect.x = randint(800, 1600)
            score += 1

        # Move tree
        if tree_rect.right > 0:
            tree_rect.x -= 2
        else:
            tree_rect.x = randint(800, 1600)
            score += 1

        # Check for game over conditions
        if balloon_rect.top < 0 or balloon_rect.bottom > 560:
            game_over = True
            update_high_scores()

        # Check for collisions
        if (balloon_rect.colliderect(bird_rect) or
            balloon_rect.colliderect(house_rect) or
            balloon_rect.colliderect(tree_rect)):
            game_over = True
            update_high_scores()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            on_mouse_down()
        elif event.type == pygame.MOUSEBUTTONUP:
            on_mouse_up()

    update()
    draw()
    clock.tick(60)  

pygame.quit()
