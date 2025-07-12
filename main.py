import pygame
from constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # game loop
    while True:
        # enable quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # background colour
        screen.fill("black")
        # refresh screen
        pygame.display.flip()

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()