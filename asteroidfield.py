# === Imports ===
import pygame
import random
# === Modules ===
from asteroid import Asteroid
from constants import *
from health_pack import Health_Pack
from player import Player

class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self): # constructor for asteroid field
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer_asteroids = 0.0 # spawn timer for asteroids
        self.spawn_timer_health_packs = 0.0 # spawn timer for health packs

    def spawn(self, radius, position, velocity, type): # method for spawning objects
        if type == "asteroid":
            # === Asteroids ===
            asteroid = Asteroid(position.x, position.y, radius) # create asteroid
            asteroid.velocity = velocity # asteroid velocity
        if type == "health pack":
            # === Health Pack ===
            health_pack = Health_Pack(position.x, position.y, radius)
            health_pack.velocity = velocity # asteroid velocity
    
    def object_properties(self):
        edge = random.choice(self.edges)
        speed = random.randint(40, 100)
        velocity = edge[0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        position = edge[1](random.uniform(0, 1))

        return position, velocity

    def update(self, dt):

        self.spawn_timer_asteroids += dt
        self.spawn_timer_health_packs += dt

        types = ["asteroid", "health pack"] # object types
        type = random.choice(types) # random choice

        position, velocity = self.object_properties() # unpack object properties

        if type == "asteroid":
            if self.spawn_timer_asteroids > ASTEROID_SPAWN_RATE:
                self.spawn_timer_asteroids = 0

                kind = random.randint(1, ASTEROID_KINDS) # asteroid size (small, medium, large)
                radius = ASTEROID_MIN_RADIUS * kind # radius from 1,3

                self.spawn(radius, position, velocity , type) # spawn asteroid object

        if type == "health pack":
            if self.spawn_timer_health_packs > HEALTH_PACK_SPAWN_RATE:
                self.spawn_timer_health_packs = 0
                
                radius = ASTEROID_MIN_RADIUS

                self.spawn(radius, position, velocity , type) # spawn health pack object