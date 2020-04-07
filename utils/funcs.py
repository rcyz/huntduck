from utils.classes import *


def save_hiscores(time):

    timesfile = open('hiscores.txt', 'a')
    end_time = str(time + '\n')
    timesfile.write(end_time)
    timesfile.close()

# a subroutine that calculates what the high score is


def calc_hiscores():
    fn = "hiscores.txt"
    try:
        timesfile = open(fn, 'r')
    except IOError:
        file = open(fn, 'w')
        file.close()
        return 0

    all_times = []

    for line in timesfile:
        all_times.append(line)

    end = len(all_times)
    # orders the list that contains the times
    all_times.sort(key=int)
    if end > 1:
        top_time = all_times[end-1]
    elif end == 1:
        top_time = all_times[0]
    else:
        top_time = "0"
    # removes '\n' from the string
    top_time = top_time[:-1]
    timesfile.close()
    return(top_time)


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
