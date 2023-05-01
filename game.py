import pygame
import logging
import os
from random import randint

from bird import Bird
from pipe import Pipe
from database import Database

class Game:
    # Constants
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 500
    PIPE_GAP = 150
    PIPE_FREQUENCY = 500
    PIPE_SPEED = 5
    FONT_SIZE = 16
    FRAME_RATE = 30
    
    def __init__(self):
        # Set up logging
        logging.basicConfig(filename='./data/flappy_bird.log', level=logging.DEBUG)

        # Initialize Pygame
        try:
            pygame.init()
        except pygame.error as e:
            logging.error("Pygame initialization failed: %s", e)
            raise SystemExit

        # Set up the screen
        self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        # Load the background image
        background_image_path = os.path.join(os.path.dirname(__file__), "images/background_day.png")
        self.background_image = pygame.image.load(background_image_path).convert()
        self.background_image = pygame.transform.scale(self.background_image, (Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))

        # Create the bird object
        self.bird = Bird(Game.SCREEN_WIDTH // 2 - 20, Game.SCREEN_HEIGHT // 2)
        self.name = ''

        # Load font and create score text
        font_path = os.path.join(os.path.dirname(__file__), "fonts/moonhouse.ttf")
        self.font = pygame.font.Font(font_path, Game.FONT_SIZE)
        self.score_text = self.font.render(f"S C O R E: {self.bird.score}", True, (0, 0, 0))
        self.gamover_text = self.font.render(f"G A M E O V E R", True, (40, 40, 40))
        self.name_text = self.font.render(f"E N T E R   N A M E: {self.name}", True, (200, 200, 200))
        

        # load game sounds
        self.point_sound = pygame.mixer.Sound('./sounds/point.mp3')
      

		# create database for storing users names & scores
        self.db = Database('./data/database.txt')

        # Set up the clock
        self.clock = pygame.time.Clock()

        # Set up the pipes
        self.pipes = []
        self.last_key = 'bottom'
        self.last_pipe_time = 0

        # Game variables
        self.menu_screen = True
        self.name_entered = False
        self.gameover = False

    def handle_events(self):
        """Handle Pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.name_entered:
                        self.name_entered = True
                    else:
                        self.bird.flap()
                elif event.key == pygame.K_RETURN:
                    self.menu_screen = False
                elif event.key == pygame.K_BACKSPACE:
                    if self.name_entered:
                        self.name = self.name[:-1]
                        self.name_text = self.font.render(f"E N T E R   N A M E: {self.name}", True, (200, 200, 200))
                elif event.key < 256 and self.name_entered:
                    self.name += chr(event.key)
                    self.name_text = self.font.render(f"E N T E R   N A M E: {self.name}", True, (200, 200, 200))
    
    def add_score_to_database(self, name, score):
        """Add a user's score to the database"""
        data = self.db.read()
        if name in data:
            data[name] += score
        else:
            data[name] = score
        self.db.write(data)

    def update_game_objects(self):
        """Update the game objects (bird and pipes)"""
        self.bird.update()
        for pipe in self.pipes:
            pipe.update(self.screen)
            if not pipe.scored and pipe.rect.x <= self.SCREEN_WIDTH // 2 - 20:
                self.bird.score += 1
                pipe.scored = True

    def render_screen(self):
        """Render the game screen"""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.bird.image, self.bird.rect)

        # Update the pipes
        for pipe in self.pipes:
            self.bird.collide(pipe)
            if not self.bird.dead:
                pipe.update(self.screen)
            if not pipe.scored and pipe.rect.x <= self.SCREEN_WIDTH // 2 - 20:
                self.bird.score += 1
                if self.bird.score % 10 == 0:
                    self.point_sound.play()
                pipe.scored = True

        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_time > self.PIPE_FREQUENCY:
            self.last_pipe_time = current_time
            if self.last_key == 'top':
                key = 'bottom'
                y = self.SCREEN_HEIGHT - randint(60, 220)
            else:
                key = 'top'
                y = randint(-200, -70)
            self.last_key = key
            pipe = Pipe(self.SCREEN_WIDTH, y, self.PIPE_GAP, self.PIPE_SPEED, key)
            self.pipes.append(pipe)
        self.score_text = self.font.render("Score: " + str(self.bird.score), True, (255, 255, 255))
        self.screen.blit(self.score_text, (20, 20))

    def display_leaderboards(self):
        """Update the leaderboard on the menu screen"""
        scores = self.db.read()
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        leaderboard_text = self.font.render("LEADERBOARD:", True, (255, 255, 255))
        self.screen.blit(leaderboard_text, (self.SCREEN_WIDTH // 2 - 50, self.SCREEN_HEIGHT // 2))
        y_offset = self.SCREEN_HEIGHT // 2 + 20
        for i in range(min(len(sorted_scores), 5)):
            score_text = self.font.render(f"{i+1}. {sorted_scores[i][0]}: {sorted_scores[i][1]}", True, (255, 255, 255))
            self.screen.blit(score_text, (self.SCREEN_WIDTH // 2 - 50, y_offset))
            y_offset += 20
     
    def display_menu(self):
        # menu screen
        while self.menu_screen:
            self.handle_events()
            self.screen.fill((60, 60, 60))
            self.display_leaderboards()
            self.screen.blit(self.name_text, (40, 40))
    
            pygame.display.update()
            
    def display_gamover_screen(self):
        while self.gameover:
            self.handle_events()
            self.screen.blit(self.gamover_text, (self.SCREEN_WIDTH // 2 - 90, self.SCREEN_HEIGHT // 2))

        pygame.display.update()

    def run(self):
        # Game loop
        while not self.bird.dead:
            self.handle_events()
            self.update_game_objects()
            self.render_screen()


            # Update the screen
            pygame.display.update()

            # Wait for the next frame
            self.clock.tick(self.FRAME_RATE)
   

