import pygame
from constants import *

from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    # fps
    clock = pygame.time.Clock()
    dt = 0

    # game state grouping
    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    
    # draw asteroids
    Asteroid.containers = (asteroids, updatables, drawables)

    # draw asteroid field
    AsteroidField.containers = (updatables)
    asteroid_field = AsteroidField()

    # draw player
    
    Player.containers = (updatables, drawables)
    player = Player(x, y, PLAYER_RADIUS)

    # game loop
    while True:
        # enable quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # background colour
        screen.fill("black")
        #
        updatables.update(dt)

        for drawable in drawables:
            drawable.draw(screen)
        # refresh screen
        pygame.display.flip()
        #
        dt = clock.tick(60) / 1000

    #
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()