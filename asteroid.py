# === Imports ===
import pygame
import random
# === Modules ===
from circleshape import CircleShape
from constants import *

# === Asteroid ===
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # audio channels
        self.asteroid_sfx_ch = pygame.mixer.Channel(3)
        # audio sfx
        self.asteroid_explode_sfx = pygame.mixer.Sound("assets/soundfx/asteroid-explode.wav")
        self.asteroid_explode_sfx.set_volume(0.1)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, 2)

    def update(self, dt):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
    
    def split(self):
        # remove the initial asteroid
        self.kill()
        # if small asteroid
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # generate random angle
        angle_between_asteroids = random.uniform(20, 50)

        # update velocity
        asteroid_velocity_1 = self.velocity.rotate(angle_between_asteroids)
        asteroid_velocity_2 = self.velocity.rotate(-angle_between_asteroids)

        # create new radii
        new_radii = self.radius - ASTEROID_MIN_RADIUS

        # create new "split" asteroids
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radii)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radii)
        
        # update split asteroid velocities
        asteroid_1.velocity = 1.2 * asteroid_velocity_1
        asteroid_2.velocity = asteroid_velocity_2
        
        # audio
        self.asteroid_sfx_ch.play(self.asteroid_explode_sfx)