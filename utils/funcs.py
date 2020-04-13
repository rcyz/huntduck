from utils.classes import *


def save_hiscores(time):

    timesfile = open('hiscores.txt', 'w')
    timesfile.write(str(time))
    timesfile.close()

# a subroutine that calculates what the high score is


def load_hiscore():
    name = "hiscores.txt"
    try:
        timesfile = open(name, 'r')
    except IOError:
        file = open(name, "w")
        file.write(str(0))
        file.close()
        return 0

    return int(timesfile.readline())


def createLabels(screen):
    menuLabels = {
        'Hiscores': Label("Hiscore: ", 10, 528, screen, 42),
        'Difficulty': Label('Easy', 750, 550, screen, 42)
    }
    gameLabels = {
        'Lives': Label('Lives: ', 30, 10, screen, 42),
        'Timer': Label('Time: ', 750, 10, screen, 42)
    }

    finalLabel = Label("", 710, 363, screen, 100)

    return menuLabels, gameLabels, finalLabel
