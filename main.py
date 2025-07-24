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
        global score
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
                centered_text("Game Over!", gameover_font, (255, 0, 0), x, y)
                pygame.display.flip()
                # audio
                centered_text_sfx = pygame.mixer.Sound("assets/soundfx/game-over.wav")
                # replace background music with gameover soundfx
                background_music_ch.play(centered_text_sfx)
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
            # score ; increment score by 100 if asteroid destroyed
            score += 100

        # draw game state
        for drawable in drawables:
            drawable.draw(screen)
        # refresh screen
        # scoreboard
        scoreboard(f"Score: {int(score)}", score_font, (255, 255, 255), 0, 0)
        pygame.display.flip()
        # limit frame rate
        pygame.display.set_caption(f"Asteroids - FPS: {clock.get_fps():.2f}")
        # get time since last frame
        dt = clock.tick(60) / 1000
        # increment score as time passes ; approx. 10 points per second
        score += dt * 10

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

    # font
    pygame.font.init()
    gameover_font = pygame.font.SysFont("Arial", 72)
    score_font = pygame.font.SysFont("Arial", 30)
    player_name_font = pygame.font.SysFont("Arial", 30)
    # helper function
    def scoreboard(text, font, text_col, x, y):
        text_font = pygame.font.SysFont("Arial", 30)
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    
    def centered_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)

    # fps management
    clock = pygame.time.Clock()

    # player name
    def player_name_input():
        player_name = ""
        # input
        while True:
            # check event
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # typing
                if event.type == pygame.KEYDOWN:
                    # pressing enter
                    if event.key == pygame.K_RETURN:
                        # output
                        return player_name
                    # pressing backspace
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    # otherwise, typing
                    else:
                        player_name += event.unicode
            # fill
            screen.fill("black")
            # display
            centered_text(f"Enter name: {player_name}", gameover_font, (255, 255, 255), x, y)
            # render
            pygame.display.flip()
    # store
    player = player_name_input()

    # main
    play_game = True
    while play_game == True:
        # start music
        background_music_ch.play(background_music_fi, loops=-1)
        # play game
        score = 0
        main()

        # write player score to file
        with open("player_scores.txt", "a") as file:
            file.write("\n" + f"player: {player} | score: {score}")

        # play again?
        play_again_selected = False

        while not play_again_selected:
            screen.fill("black")
            # text
            centered_text(f"Play Again? (y/n)", gameover_font, (255, 255, 255), x, y)
            # render
            pygame.display.flip()
            
            # input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # play again
                    if event.key == pygame.K_y:
                        play_again_selected = True
                        # clear
                        pygame.event.clear()
                    # exit game
                    elif event.key == pygame.K_n:
                        play_game = False
                        play_again_selected = True
                        screen.fill("black")
                        centered_text(f"Thanks for Playing!", gameover_font, (255, 255, 255), x, y)
                        # render
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        # close window
                        pygame.quit()
                        # exit program
                        exit()
