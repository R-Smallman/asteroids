# === Imports ===
import pygame
# === Modules ===
from circleshape import CircleShape
from constants import *

# === Health Pack ===
class Health_Pack(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "green", (self.position.x, self.position.y), self.radius, 0)

    def update(self, dt):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt