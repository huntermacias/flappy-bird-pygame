import pygame
import logging
import os
from random import randint

from bird import Bird
from pipe import Pipe
from database import Database


# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
PIPE_GAP = 150
PIPE_FREQUENCY = 500
PIPE_SPEED = 5
FONT_SIZE = 16
FRAME_RATE = 30

gamover = False

# Set up logging
logging.basicConfig(filename='flappy_bird.log', level=logging.DEBUG)

# Initialize Pygame
try:
    pygame.init()
except pygame.error as e:
    logging.error("Pygame initialization failed: %s", e)
    raise SystemExit

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load the background image
background_image_path = os.path.join(os.path.dirname(__file__), "images/background_day.png")
background_image = pygame.image.load(background_image_path).convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create the bird object
bird = Bird(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2)
name = ''

# Load font and create score text
font_path = os.path.join(os.path.dirname(__file__), "fonts/moonhouse.ttf")
font = pygame.font.Font(font_path, FONT_SIZE)
score_text = font.render(f"S C O R E: {bird.score}", True, (0, 0, 0))
gamover_text = font.render(f"G A M E O V E R", True, (40, 40, 40))
name_text = font.render(f"E N T E R   N A M E: {name}", True, (200, 200, 200))

# Set up the clock
clock = pygame.time.Clock()

# Set up the pipes
pipes = []
last_key = 'bottom'
last_pipe_time = 0

# Game variables
menu_screen = True
name_entered = False



def handle_events():
    """Handle Pygame events"""
    global menu_screen, name_entered, name, name_text
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not name_entered:
                    name_entered = True
                else:
                    bird.flap()
            elif event.key == pygame.K_RETURN:
                menu_screen = False
                # if name_entered:
                #     add_score_to_database(name, bird.score)
                #     name_entered = False
                #     name = ''
            elif event.key == pygame.K_BACKSPACE:
                if name_entered:
                    name = name[:-1]
                    name_text = font.render(f"E N T E R   N A M E: {name}", True, (200, 200, 200))
            elif event.key < 256 and name_entered:
                name += chr(event.key)
                name_text = font.render(f"E N T E R   N A M E: {name}", True, (200, 200, 200))
                
def add_score_to_database(name, score):
    """Add a user's score to the database"""
    db = Database('database.txt')
    data = db.read()
    if name in data:
        data[name] += score
    else:
        data[name] = score
    db.write(data)

def update_game_objects():
    """Update the game objects (bird and pipes)"""
    bird.update()
    for pipe in pipes:
        pipe.update(screen)
        if not pipe.scored and pipe.rect.x <= SCREEN_WIDTH // 2 - 20:
            bird.score += 1
            pipe.scored = True

def render_screen():
    """Render the game screen"""
    global last_pipe_time, last_key
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    screen.blit(bird.image, bird.rect)

    # Update the pipes
    for pipe in pipes:
        bird.collide(pipe)
        if not bird.dead:
            pipe.update(screen)
        if not pipe.scored and pipe.rect.x <= SCREEN_WIDTH // 2 - 20:
            bird.score += 1
            pipe.scored = True

    current_time = pygame.time.get_ticks()
    if current_time - last_pipe_time > PIPE_FREQUENCY:
        last_pipe_time = current_time
        if last_key == 'top':
            key = 'bottom'
            y = SCREEN_HEIGHT - randint(60, 220)
        else:
            key = 'top'
            y = randint(-200, -70)
        last_key = key
        pipe = Pipe(SCREEN_WIDTH, y, PIPE_GAP, PIPE_SPEED, key)
        pipes.append(pipe)
    screen.blit(score_text, (20, 20))

def update_score_text():
    """Update the score text"""
    global score_text
    score_text = font.render(f"S C O R E: {bird.score}", True, (0, 0, 0))

while menu_screen:
    handle_events()
    screen.fill((60, 60, 60))
    screen.blit(name_text, (40, 40))
    
    pygame.display.update()

# Game loop
while not bird.dead:
    handle_events()
    update_game_objects()
    render_screen()
    update_score_text()


    # Update the screen
    pygame.display.update()

    # Wait for the next frame
    clock.tick(FRAME_RATE)


gameover = True

# add score to databaseun
add_score_to_database(name, bird.score)


while gameover:
    handle_events()
    screen.blit(gamover_text, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2))

    pygame.display.update()