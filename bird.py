import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Load the bird images
        self.images = [
            pygame.image.load("bird1.png").convert_alpha(),
            pygame.image.load("bird2.png").convert_alpha(),
            pygame.image.load("bird3.png").convert_alpha()
        ]
        
        # Set the initial image, position, and velocity of the bird
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0
        self.max_velocity = 20
        
        # Set the bird's animation variables
        self.frame = 0
        self.animation_time = 0
        self.animation_delay = 5
        
        # Set the bird's rotation variables
        self.rotation = 0
        self.rotation_speed = 2
        self.max_rotation = 25
        self.dead = False
        
		# Set bird stat variables
        self.score = 0
        
    def collide(self, pipe):
        if self.rect.colliderect(pipe.rect):
            # Hit a pipe, rotate backwards and fall
            self.dead = True
            self.velocity = 10
            self.rotation = -90
            rotated_image = pygame.transform.rotate(self.image, self.rotation)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            self.image = rotated_image
            self.rect = new_rect
        
    def update(self):
        # Handle the bird's animation
        self.animation_time += 1
        if self.animation_time % self.animation_delay == 0:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
        
          # Handle the bird's rotation
        if self.velocity < 0:
            self.rotation = self.max_rotation
        else:
            if self.rotation > -90:
                self.rotation -= self.rotation_speed
        
        # Update the bird's position and velocity
        self.velocity += 1.5
        self.rect.y += self.velocity
        
       
        
    def flap(self):
        # Handle the bird flapping
        self.velocity = -15
        self.rotation = self.max_rotation
        
		# Rotate the bird image
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect = new_rect
