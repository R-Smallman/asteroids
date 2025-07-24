import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
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

    # time
    dt = 0
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
                # render game over message
                game_over("Game Over!", gameover_font, (255, 0, 0), x, y)
                pygame.display.flip()
                # audio
                game_over_sfx = pygame.mixer.Sound("assets/soundfx/game-over.wav")
                # replace background music with gameover soundfx
                background_music_ch.play(game_over_sfx)
                # when gameover soundfx is finished; end the game
                while background_music_ch.get_busy():
                    continue
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
            # score
            global score
            score += 100

        # draw game state
        for drawable in drawables:
            drawable.draw(screen)
        # refresh screen
        # scoreboard
        scoreboard(f"Score: {score}", score_font, (255, 255, 255), 0, 0)
        pygame.display.flip()
        # limit frame rate
        pygame.display.set_caption(f"Asteroids - FPS: {clock.get_fps():.2f}")
        # get time since last frame
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    # initialisation
    pygame.init()
    # screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # screen center coords
    x, y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

    # audio
    pygame.mixer.init()
    # audio starts
    background_music_ch = pygame.mixer.Channel(0)
    background_music_fi = pygame.mixer.Sound("assets/music/space-chase.wav")
    background_music_ch.play(background_music_fi, loops=-1)

    # font
    pygame.font.init()
    gameover_font = pygame.font.SysFont("Arial", 72)
    score_font = pygame.font.SysFont("Arial", 30)
    # helper function
    def scoreboard(text, font, text_col, x, y):
        text_font = pygame.font.SysFont("Arial", 30)
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    
    def game_over(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)

    # fps management
    clock = pygame.time.Clock()

    # score
    score = 0

    # main
    main()