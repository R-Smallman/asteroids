import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    # initialisation
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    # fps
    clock = pygame.time.Clock()
    dt = 0

    # game state grouping
    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # draw asteroids
    Asteroid.containers = (asteroids, updatables, drawables)

    # draw asteroid field
    AsteroidField.containers = updatables
    asteroid_field = AsteroidField()

    # draw player
    Player.containers = (updatables, drawables)
    player = Player(x, y, PLAYER_RADIUS)

    # draw shots
    Shot.containers = (shots, updatables, drawables)

    # game loop
    while True:
        # enable quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # exit game
                return
        # background colour
        screen.fill("black")
        # update game state
        updatables.update(dt)
        
        remove_these_shots = set()
        remove_these_asteroids = set()
        # check for collisions between asteroids, players and shots
        for asteroid in asteroids:
            # if asteroid collides with player
            if asteroid.collision(player):
                print("Game Over!")
                # exit game
                return
            # if shot collides with asteroid
            for shot in shots:
                if asteroid.collision(shot):
                    remove_these_shots.add(shot)
                    remove_these_asteroids.add(asteroid)
        # remove shots
        for shot in remove_these_shots:
            shot.kill()
        # split asteroids
        for asteroid in remove_these_asteroids:
            asteroid.split()

        # draw game state
        for drawable in drawables:
            drawable.draw(screen)
        # refresh screen
        pygame.display.flip()
        # limit frame rate
        pygame.display.set_caption(f"Asteroids - FPS: {clock.get_fps():.2f}")
        # get time since last frame
        dt = clock.tick(60) / 1000

    # messages
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()