import pygame

from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, PLAYER_RADIUS):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
    
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    # draw the player
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
    
    # rotate the player
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    # update the player
    def update(self, dt):
        # update cooldown
        self.shoot_cooldown -= dt
        keys = pygame.key.get_pressed()
        # rotate left
        if keys[pygame.K_a]:
            self.rotate(-dt)
        # rotate right
        if keys[pygame.K_d]:
            self.rotate(dt)
        # move forward
        if keys[pygame.K_w]:
            self.move(dt)
        # move backward
        if keys[pygame.K_s]:
            self.move(-dt)
        # shoot
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    # move the player
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    # player shoots
    def shoot(self):
        # check if the player can shoot
        if self.shoot_cooldown > 0:
            return
        # create a new shot
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        # set the shot's velocity
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED        
        # increment the cooldown
        self.shoot_cooldown += PLAYER_SHOOT_COOLDOWN
        