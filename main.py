# === Imports ===
import pygame

# === Modules ===
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from health_pack import Health_Pack

# === Functions ===
def main():
    # === Startup ===
    background_music_ch.play(background_music_fi, loops=-1) # start background music

    updatables = pygame.sprite.Group() # create group
    drawables = pygame.sprite.Group() # create group
    asteroids = pygame.sprite.Group() # create group
    shots = pygame.sprite.Group() # create group
    health_packs = pygame.sprite.Group() # create group
    
    Asteroid.containers = (asteroids, updatables, drawables) # add asteroids to groups
    AsteroidField.containers = updatables # add asteroid_field to group
    Player.containers = (updatables, drawables) # draw player
    Shot.containers = (shots, updatables, drawables) # draw shots
    Health_Pack.containers = (health_packs, updatables, drawables) # draw health packs

    asteroid_field = AsteroidField() # create asteroid field
    player = Player(x, y, PLAYER_RADIUS) # create player

    dt = 0 # time

    # === Game Loop ===
    while True:
        global score
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # enable quit button
                # exit game
                exit()
        
        screen.fill("black") # fill
        
        updatables.update(dt) # update game state
        
        remove_these_shots = set()
        remove_these_asteroids = set()
        remove_these_health_packs = set()

        for asteroid in asteroids: # check for collisions between asteroids, players and shots
            
            if asteroid.collision(player): # if asteroid collides with player

                player.lives -= 1 # remove one life

                if player.lives == 0: # if no lives remaining
                    
                    centered_text("Game Over!", gameover_font, (255, 0, 0), x, y)  # display text
                    pygame.display.flip() # render
                    
                    centered_text_sfx = pygame.mixer.Sound("assets/soundfx/game-over.wav")
                    background_music_ch.play(centered_text_sfx) # replace background music with gameover soundfx
                    while background_music_ch.get_busy(): # when gameover soundfx is finished; end the game
                        continue

                    return # exit game
                
                else:
                    player.position.x = SCREEN_WIDTH / 2
                    player.position.y = SCREEN_HEIGHT / 2
            
            for shot in shots:
                if asteroid.collision(shot): # if shot collides with asteroid
                    remove_these_shots.add(shot)
                    remove_these_asteroids.add(asteroid)
        
        for health_pack in health_packs:

            if health_pack.collision(player):
                if player.lives < 3: # check if life at maximum (3)
                    player.lives += 1 # add one life

                remove_these_health_packs.add(health_pack)

        for health_pack in remove_these_health_packs:
            health_pack.kill() # remove health packs
        
        for shot in remove_these_shots: 
            shot.kill() # remove shots
        
        for asteroid in remove_these_asteroids:
            asteroid.split() # split asteroids
            score += 100 # score ; increment score by 100 if asteroid destroyed

        for drawable in drawables:
            drawable.draw(screen) # draw game state
        
        score_text = f"Score: {int(score)}" # display score
        lives_text = f"Lives: {player.lives}" # display lives

        lives_img = font.render(lives_text, True, (0, 255, 0)) # create img
        sph_img = font.render("|", True, (255,255,255), 0)
        score_img = font.render(score_text, True, (255,255,0)) # create img

        screen.blit(score_img, (10, 10)) # position img
        screen.blit(sph_img, (score_img.get_width() + 15, 10))
        screen.blit(lives_img, (score_img.get_width() + 30, 10)) # position img

        pygame.display.flip() # render

        dt = clock.tick(60) / 1000 # get time since last frame
        score += dt * 10 # increment score as time passes ; approx. 10 points per second

# === Input : Player Name ===
def player_name_input():
    player_name = ""
    # input
    while True:
        for event in pygame.event.get(): # check events

            if event.type == pygame.QUIT: # enable quit
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN: # typing
                if event.key == pygame.K_RETURN: # pressing enter
                    return player_name # output
                
                elif event.key == pygame.K_BACKSPACE: # pressing backspace
                    player_name = player_name[:-1] # delete last character
                
                else: # otherwise, typing
                    player_name += event.unicode # record character
        
        screen.fill("black") # fill
        centered_text(f"Enter name: {player_name}", gameover_font, (255, 255, 255), x, y) # display text
        pygame.display.flip() # render

# display score
def scoreboard(text, font, text_col, x, y):
    text_font = pygame.font.SysFont("Arial", 30)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# display centered text
def centered_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

# === Main ===
if __name__ == "__main__":
    # === Initialisation ===
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    pygame.display.set_caption(f"Asteroids! : A Guided Course by Boot.dev (with additions by R-Smallman)")
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create screen
    x, y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 # screen center coords

    background_music_ch = pygame.mixer.Channel(0) # create background music channel
    background_music_fi = pygame.mixer.Sound("assets/music/space-chase.wav") # create background music
    background_music_ch.set_volume(0.2)

    # font
    gameover_font = pygame.font.SysFont("Arial", 72)
    font = pygame.font.SysFont("Arial", 30)
    player_name_font = pygame.font.SysFont("Arial", 30)

    # fps management
    clock = pygame.time.Clock()

    # === Title ===
    screen.fill("black") # fill w/ black
    centered_text(f"Asteroids!", gameover_font, (255, 255, 255), x, y) # display text
    pygame.display.flip() # render
    pygame.time.wait(1000) # wait

    # === Game Loop ===
    player = player_name_input()  # input : player name
    
    play_game = True
    while play_game == True:
        # play game
        score = 0
        main()

        # === Output Score ===
        with open("player_scores.txt", "a") as file:
            file.write("\n" + f"player: {player} | score: {score}")

        # === Play Again? ===
        play_again_selected = False
        while not play_again_selected:
            # text
            screen.fill("black") # fill w/ black
            centered_text(f"Play Again? (y/n)", gameover_font, (255, 255, 255), x, y) # display text
            pygame.display.flip() # render
            
            # input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # === Restart ===
                    if event.key == pygame.K_y:
                        play_again_selected = True
                        pygame.event.clear() # clear event log

                    # === Exit ===
                    elif event.key == pygame.K_n:
                        play_game = False
                        play_again_selected = True

                        # text
                        screen.fill("black") # fill w/ black
                        centered_text(f"Thanks for Playing!", gameover_font, (255, 255, 255), x, y) # display text
                        pygame.display.flip() # render
                        pygame.time.wait(1000) # wait
                        
                        pygame.quit() # close window
                        exit() # exit program