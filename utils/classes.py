import pygame
import os
import random
from utils import ptext


class Screen():
    def __init__(self):
        self.screen = pygame.display.set_mode((891, 608))
        self.skinNames = ['default']
        self.skinNum = 0
        pygame.display.set_caption('Hunt Duck')
        self.skinNames += self.loadSkinNames()
        self.skinNames = list(dict.fromkeys(self.skinNames))
        print(self.skinNames)
        self.loadSkin(self.skinNames, self.skinNum)

    def drawScreen(self, name):
        if name == 'title':
            self.screen.blit(self.titlescreen, (0, 0))
        elif name == 'pause':
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.pausescreen, (0, 50))
        elif name == 'go':
            self.screen.blit(self.gameoverscreen, (0, 0))
        elif name == 'bg':
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 50))
        elif name == 'win':
            self.screen.blit(self.winscreen, (0, 0))

    def drawLabel(self, label, x, y):
        self.screen.blit(label, (x, y))

    def drawSprites(self, list):
        list.draw(self.screen)

    def increaseSkin(self):
        if self.skinNum == len(self.skinNames) - 1:
            self.skinNum = 0
        else:
            self.skinNum += 1
        self.loadSkin(self.skinNames, self.skinNum)

    def decreaseSkin(self):
        if self.skinNum == 0:
            self.skinNum = len(self.skinNames) - 1
        else:
            self.skinNum -= 1
        self.loadSkin(self.skinNames, self.skinNum)

    def loadSkinNames(self):
        skins = [f.name for f in os.scandir('skins') if f.is_dir()]
        return skins

    def loadSkin(self, skins, skinNum):
        dir = 'skins/' + skins[skinNum]
        print(dir)
        self.background = pygame.transform.scale(
            pygame.image.load(dir + '/background.png'), (891, 558))
        self.pausescreen = pygame.transform.scale(
            pygame.image.load(dir + '/pausescreen.png'), (891, 558))
        self.titlescreen = pygame.transform.scale(
            pygame.image.load(dir + '/titlescreen.png'), (891, 608))
        self.gameoverscreen = pygame.transform.scale(
            pygame.image.load(dir + '/losing.png'), (891, 608))
        self.winscreen = pygame.transform.scale(
            pygame.image.load(dir + '/completion.png'), (891, 608))

    def getFolder(self):
        return 'skins/' + str(self.skinNames[self.skinNum])


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super(Player, self).__init__()

        self.image = pygame.image.load('skins/default/player.png')

        self.image = pygame.transform.scale(self.image, (70, 40))
        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = (pos[0]-28)
        self.rect.y = (pos[1]-20)

    def updateSkin(self, screen):
        self.image = pygame.transform.scale(pygame.image.load(
            screen.getFolder() + '/player.png'), (70, 40))


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self, mx, my, speed, screen):
        # Call the parent class (Sprite) constructor
        super(Bullet, self).__init__()
        self.speed = speed

        self.imageLoc = screen.getFolder() + '/bullet.png'

        self.image = pygame.transform.scale(pygame.image.load(self.imageLoc), (40, 40))

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
        self.fontsize = fontsize
        self.gamefont = pygame.font.Font(None, fontsize)

    def draw(self, colour):
        white = (255, 255, 255)
        black = (0, 0, 0)
        label = self.gamefont.render(self.text, 1, colour)
        ptext.draw(self.text, (self.x, self.y), owidth=1.5,
                   ocolor=black, color=white, fontsize=self.fontsize)
        # self.screen.drawLabel(label, self.x, self.y)

    def updateText(self, text):
        self.text = text
