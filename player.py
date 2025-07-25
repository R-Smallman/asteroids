import pygame

from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, PLAYER_RADIUS):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        # audio channels
        self.player_shoot_ch = pygame.mixer.Channel(1)
        self.player_move_ch = pygame.mixer.Channel(2)
        # moving : audio sfx
        self.spaceship_moving_sfx = pygame.mixer.Sound("assets/soundfx/spaceship-engine.wav")
        self.spaceship_moving_sfx.set_volume(0.3)
        # shooting : audio sfx
        self.player_shoot_sfx = pygame.mixer.Sound("assets/soundfx/player-shoot.wav")
        self.player_shoot_sfx.set_volume(0.3)

        # lives
        self.lives = 3
    
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
        pygame.draw.polygon(screen, "green", self.triangle(), 2)
    
    # rotate the player
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    # update the player
    def update(self, dt):
        # update cooldown
        if self.shoot_cooldown > 0: # if on cooldown
            self.shoot_cooldown -= dt # reduce cooldown

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
            # audio
            if not self.player_move_ch.get_busy():
                self.player_move_ch.play(self.spaceship_moving_sfx)
        # move backward
        if keys[pygame.K_s]:
            self.move(-dt)
        # shoot
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        if not keys[pygame.K_w]:
            self.player_move_ch.fadeout(100)
    
    # move the player
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    # player shoots
    def shoot(self):
        if self.shoot_cooldown > 0: # if during cooldown
            return # player can't shoot

        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS) # create bullet
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED # set bullet velocity

        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN # reset cooldown
        
        self.player_shoot_ch.play(self.player_shoot_sfx) # play sfx

        