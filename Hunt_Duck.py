import pygame
import sys
import time
from pygame.locals import *
from utils.classes import *
from utils.hiscoreFuncs import *
from utils.drawfuncs import *

pygame.init()

# initialising screen
screen = pygame.display.set_mode((891, 608))
pygame.display.set_caption('Hunt Duck')
clock = pygame.time.Clock()

backgroundImg = pygame.image.load('images/background.png')
pausescreen = pygame.image.load('images/pausescreen.png')
titlescreen = pygame.image.load('images/titlescreen.png')
gameoverscreen = pygame.image.load('images/losing.png')
gamefont = pygame.font.Font(None, 42)
endfont = pygame.font.Font(None, 100)

# main loop condition
main = True

# Sprite lists
all_sprites_list = pygame.sprite.Group()

dog = Dog()
all_sprites_list.add(dog)

duck = Duck()
all_sprites_list.add(duck)

diffIndex = 0

#       --- MAIN LOOP ---

while main:

    # creates the tomato list and direction lists
    # also wipes them everytime the game restarts
    tomato_sprites_list = pygame.sprite.Group()

    # loop conditions
    main = True
    menu = True
    draw = False
    game = True
    playing = True
    paused = False
    game_over = False

    # initialise variables used for the timer and life system
    times = 0
    pause = {
        'start': 0,
        'end': 0,
        'paused': 0,
        'totalpaused': 0
    }
    diffSpeeds = {
        'Easy': 100,
        'Medium': 50,
        'Hard': 20,
        'Insane': 10,
        'Fearless': 5
    }
    lives = 5
    respawn = 10
    delay = 0
    currDiff = str(list(diffSpeeds.keys())[diffIndex])

    # game loop
    while game:
        while menu:
            screen.blit(titlescreen, (0, 0))
            # calculate high score and draw to screen
            best_time = calc_hiscores()
            draw_hiscores(screen, gamefont, best_time)
            draw_difficulty(screen, gamefont, currDiff)

            # grab the mouse location
            mousex, mousey = pygame.mouse.get_pos()

            pygame.display.update()

            # events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    # grab the status of the mouse buttons and check if the left
                    # mouse button is pressed
                    mousestatus = pygame.mouse.get_pressed()
                    if mousestatus[0]:
                        # check whether the mouse is over the start button
                        if mousex > 320 and mousex < 550 and mousey > 400 and mousey < 460:
                            menu = False
                            playing = True
                            start = time.process_time()
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        if diffIndex < (len(diffSpeeds)-1):
                            diffIndex += 1
                    elif event.key == K_LEFT:
                        if diffIndex > 0:
                            diffIndex -= 1
                    currDiff = str(list(diffSpeeds.keys())[diffIndex])

        # playing loop
        while playing:

            # works out time played and renders the label
            elapsed = int(time.process_time() - start - pause['totalpaused'])
            if respawn != 0:
                if elapsed > delay:
                    if elapsed % 1 == 0:
                        for tomato in tomato_sprites_list:
                            tomato.speed /= 2
                        delay += 5
                        respawn -= 1

            elapsedInt = int(float(time.process_time() - start - pause['totalpaused']) * 1000)
            draw_timer(screen, gamefont, elapsed)

            # creating bullet sprites and adding them to sprite list
            if elapsedInt % respawn == 0:
                if len(tomato_sprites_list) < 20:
                    # creates tomato sprite
                    mousex, mousey = pygame.mouse.get_pos()
                    tomato = Tomato(mousex, mousey, diffSpeeds[currDiff])

                    tomato_sprites_list.add(tomato)

            # updates the position of all the sprites
            all_sprites_list.update()
            # for loop updating each tomato in turn
            # and checking if events have happened
            for tomato in tomato_sprites_list:
                # checks for collision between duck and tomato
                if tomato.rect.colliderect(duck.rect):
                    lives -= 1
                    tomato_sprites_list.remove(tomato)
                elif tomato.rect.x > 891 or tomato.rect.x < 0 or tomato.rect.y > 608 or tomato.rect.y < 40:
                    tomato_sprites_list.remove(tomato)

                # updates the position of the tomato
                tomato.update()

            # drawing the background, timer and sprites to the screen
            screen.blit(backgroundImg, (0, 0))
            draw_timer(screen, gamefont, elapsed)
            all_sprites_list.draw(screen)
            tomato_sprites_list.draw(screen)
            draw_lives(screen, gamefont, lives)

            # checks if the duck has ran out of lives
            if lives <= 0:
                # records the time when the player died
                finaltime = str(elapsed)
                playing = False
                game_over = True

            # events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # checks if the left mouse button has been released and if so
                # enters the pause loop
                elif event.type == MOUSEBUTTONUP:
                    mousestatus = pygame.mouse.get_pressed()
                    if not mousestatus[0]:
                        playing = False
                        paused = True
                        pause['start'] = time.process_time()
                        times = elapsed

            pygame.display.update()

            # pause loop
            while paused:

                # draws the pause screen, lives and timer to the screen
                screen.blit(pausescreen, (0, 0))
                draw_timer(screen, gamefont, times)
                draw_lives(screen, gamefont, lives)

                pygame.display.update()

                # events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    # if the left mouse button has been pressed, calculate the time while paused
                    # and return to the game loop
                    if event.type == MOUSEBUTTONDOWN:
                        mousestatus = pygame.mouse.get_pressed()
                        if mousestatus[0]:
                            playing = True
                            paused = False
                            pause['end'] = time.process_time()
                            pause['paused'] = pause['end'] - pause['start']
                            pause['totalpaused'] += pause['paused']
                    # check if the player wants to return to the main menu
                    if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                        paused = False
                        game = False
                        menu = True

            # game over loop
            while game_over:
                # draw the game over screen and final time to the screen
                screen.blit(gameoverscreen, (0, 0))
                draw_finaltime(screen, endfont, finaltime)
                pygame.display.update()
                # events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == MOUSEBUTTONDOWN:
                        # save the score to the hiscore text file
                        save_hiscores(finaltime)
                        # return to the menu loop
                        game_over = False
                        game = False
                        menu = True
            clock.tick(60)
