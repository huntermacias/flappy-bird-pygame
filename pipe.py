import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, gap_size, speed, key):
        super().__init__()

        # Load the pipe images
        if key == 'top':
            self.pipe_image = pygame.image.load("./images/pipe.png").convert_alpha()
            self.image = pygame.transform.rotate(self.pipe_image, 180)
        else:
            self.image = pygame.image.load("./images/pipe.png").convert_alpha()
            

        # Set the position and velocity of the pipe
        self.speed = speed
        if key == 'top':
            self.rect = self.image.get_rect(topleft=(x, y))
        else:
            self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

        self.gap_size = gap_size
        self.key = key
        self.scored = False

    def update(self, screen):
        # Move the pipe to the left
        self.rect.move_ip(-self.speed, 0)

        # Check if the pipe is off the screen
        if self.rect.right < 0:
            self.kill()

        # Update the image on the screen
        screen.blit(self.image, self.rect)
   
