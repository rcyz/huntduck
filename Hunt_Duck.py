import pygame
import sys
import time
from pygame.locals import *
from utils.classes import *
from utils.funcs import *

pygame.init()

# initialising screen
screen = Screen()
pygame.display.set_caption('Hunt Duck')
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0,   0,   0)

# main loop condition
main = True
diffIndex = 0
diffSpeeds = {
    'Easy': 200,
    'Medium': 100,
    'Hard': 50,
    'Insane': 25,
    'Fearless': 10
}
diffLives = {
    'Easy': 20,
    'Medium': 10,
    'Hard': 5,
    'Insane': 5,
    'Fearless': 2
}

# Sprite lists
player_sprite = pygame.sprite.Group()
menuLabels, gameLabels, finalLabel = createLabels(screen)

player = Player()
player_sprite.add(player)

while main:

    # creates the tomato list and direction lists
    # also wipes them everytime the game restarts
    bullet_list = pygame.sprite.Group()

    # loop conditions
    main = True
    menu = True
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

    delay = 0
    respawn = 10

    currDiff = str(list(diffSpeeds.keys())[diffIndex])
    speed = diffSpeeds[currDiff]
    currSkin = screen.getSkinName()

    # game loop
    while game:
        while menu:
            lives = diffLives[currDiff]
            screen.drawScreen('title')
            startRect = screen.drawStart()
            # calculate high score and draw to screen
            best_time = load_hiscore()
            menuLabels['Hiscores'].updateText('Hiscore: ' + str(best_time))
            menuLabels['Difficulty'].updateText(currDiff)
            menuLabels['Skin'].updateText(currSkin)
            for label in menuLabels.values():
                label.draw(black)

            pygame.display.update()

            # events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN and event.button == 1:

                    mpos = pygame.mouse.get_pos()

                    mousestatus = pygame.mouse.get_pressed()
                    if startRect.collidepoint(mpos):
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
                    elif event.key == K_UP:
                        currSkin = screen.increaseSkin()
                        player.updateSkin(screen)
                    elif event.key == K_DOWN:
                        currSkin = screen.decreaseSkin()
                        player.updateSkin(screen)
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    currDiff = str(list(diffSpeeds.keys())[diffIndex])
                    speed = diffSpeeds[currDiff]

        # playing loop
        while playing:

            # works out time played and renders the label
            elapsed = int(time.process_time() - start - pause['totalpaused'])
            elapsedInt = int(float(time.process_time() - start - pause['totalpaused']) * 1000)

            if respawn != 0:
                if elapsed > delay:
                    if elapsed % 1 == 0:
                        speed /= 2
                        delay += 5
                        if respawn > 1:
                            respawn -= 1

            # creating bullet sprites and adding them to sprite list
            if elapsedInt % respawn == 0:
                if len(bullet_list) < 20:
                    # creates tomato sprite
                    mousex, mousey = pygame.mouse.get_pos()
                    bullet = Bullet(mousex, mousey, speed, screen)

                    bullet_list.add(bullet)

            # updates the position of all the sprites
            player.update()
            # for loop updating each tomato in turn
            # and checking if events have happened
            for bullet in bullet_list:
                # checks for collision between duck and tomato
                if bullet.rect.colliderect(player.rect):
                    lives -= 1
                    bullet_list.remove(bullet)
                elif bullet.rect.x > 891 or bullet.rect.x < 0 or bullet.rect.y > 608 or bullet.rect.y < 40:
                    bullet_list.remove(bullet)

                # updates the position of the tomato
                bullet.update()

            gameLabels['Timer'].updateText('Time: ' + str(elapsed))
            gameLabels['Lives'].updateText('Lives: ' + str(lives))
            # drawing the background, timer and sprites to the screen
            screen.drawScreen('background')
            for label in gameLabels.values():
                label.draw(black)
            screen.drawSprites(player_sprite)
            screen.drawSprites(bullet_list)

            # checks if the duck has ran out of lives
            if lives <= 0:
                # records the time when the player died
                finaltime = elapsed
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
                screen.drawScreen('pause')
                for label in gameLabels.values():
                    label.draw(black)

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
                if finaltime > best_time:
                    save = True
                    screen.drawScreen('win')
                else:
                    screen.drawScreen('gameover')
                finalLabel.updateText(str(finaltime) + "s")
                finalLabel.draw(white)
                pygame.display.update()
                # events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == MOUSEBUTTONDOWN:
                        # return to the menu loop
                        if save:
                            save_hiscores(finaltime)
                        game_over = False
                        game = False
                        menu = True
            clock.tick(60)
