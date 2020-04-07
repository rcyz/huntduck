import pygame
import random

#       --- Classes ---


class Screen():
    def __init__(self):
        self.screen = pygame.display.set_mode((891, 608))
        pygame.display.set_caption('Hunt Duck')
        defaultDir = 'skins/default/'

        self.background = pygame.image.load(defaultDir + 'background.png')
        self.pausescreen = pygame.image.load(defaultDir + 'pausescreen.png')
        self.titlescreen = pygame.image.load(defaultDir + 'titlescreen.png')
        self.gameoverscreen = pygame.image.load(defaultDir + 'losing.png')

    def drawScreen(self, name):
        if name == 'title':
            self.screen.blit(self.titlescreen, (0, 0))
        elif name == 'pause':
            self.screen.blit(self.pausescreen, (0, 0))
        elif name == 'go':
            self.screen.blit(self.gameoverscreen, (0, 0))
        elif name == 'bg':
            self.screen.blit(self.background, (0, 0))

    def drawLabel(self, label, x, y):
        self.screen.blit(label, (x, y))

    def drawSprites(self, list):
        list.draw(self.screen)


class Duck(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super(Duck, self).__init__()

        self.image = pygame.image.load('skins/default/duck.png')

        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = (pos[0]-28)
        self.rect.y = (pos[1]-20)


class Dog(pygame.sprite.Sprite):

    def __init__(self):
        super(Dog, self).__init__()

        self.image = pygame.image.load('skins/default/dog.png')

        self.rect = self.image.get_rect()

    def update(self):

        self.rect.x = 350
        self.rect.y = 450


class Tomato(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self, mx, my, speed):
        # Call the parent class (Sprite) constructor
        super(Tomato, self).__init__()
        self.speed = speed

        self.image = pygame.image.load('skins/default/tomato.png')

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1, 891)
        self.rect.y = 608

        self.xdir = mx - self.rect.x
        self.ydir = self.rect.y - my

    def update(self):
        """ Move the bullet. """

        self.rect.x += self.xdir/self.speed
        self.rect.y -= self.ydir/self.speed


class Label():
    def __init__(self, text, x, y, screen, fontsize):
        super(Label, self).__init__()
        self.text = text
        self.x = x
        self.y = y
        self.screen = screen
        self.gamefont = pygame.font.Font(None, fontsize)

    def draw(self, colour):
        label = self.gamefont.render(self.text, 1, colour)
        self.screen.drawLabel(label, self.x, self.y)

    def updateText(self, text):
        self.text = text
