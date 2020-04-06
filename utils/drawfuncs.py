from utils.initvars import *


def draw(screen, text, loc):
    screen.blit(text, loc)


def draw_timer(screen, font, time):
    timelabel = 'Time: ' + str(time)
    text = font.render(timelabel, 1, black)
    draw(screen, text, (750, 10))

# a subroutine to draw the lives to the screen


def draw_lives(screen, font, lives):
    life_string = 'Lives: ' + str(lives)
    life_label = font.render(str(life_string), 1, black)
    draw(screen, life_label, (30, 10))

# a subroutine to draw the final time to the gameover screen


def draw_finaltime(screen, font, time,):
    end_time = str(time) + 's'
    time_label = font.render(str(end_time), 1, white)
    draw(screen, time_label, (710, 363))

# a subroutine to draw the hiscores to the screen


def draw_hiscores(screen, font, time):
    text = font.render('Hiscore', 1, black)
    draw(screen, text, (10, 528))
    text = font.render(str(time), 1, black)
    draw(screen, text, (40, 558))


def draw_difficulty(screen, font, difficulty):
    text = font.render(difficulty, 1, black)
    draw(screen, text, (800, 550))
