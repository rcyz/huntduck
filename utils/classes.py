import pygame
import os
import random


class Screen():
    def __init__(self):
        self.screen = pygame.display.set_mode((891, 608))

        self.skinNumber = 0
        pygame.display.set_caption('Hunt Duck')
        self.skins = self.loadSkins()
        self.loadSkin(self.skins, self.skinNumber)

    def drawScreen(self, name):
        if name == 'title':
            self.screen.blit(self.titlescreen, (0, 0))
        elif name == 'pause':
            self.screen.blit(self.pausescreen, (0, 0))
        elif name == 'go':
            self.screen.blit(self.gameoverscreen, (0, 0))
        elif name == 'bg':
            self.screen.blit(self.background, (0, 0))
        elif name == 'win':
            self.screen.blit(self.winscreen, (0, 0))

    def drawLabel(self, label, x, y):
        self.screen.blit(label, (x, y))

    def drawSprites(self, list):
        list.draw(self.screen)

    def increaseSkin(self):
        if self.skinNumber < len(self.skins) - 1:
            self.skinNumber += 1
            self.loadSkin(self.skins, self.skinNumber)

    def decreaseSkin(self):
        if self.skinNumber > 0:
            self.skinNumber -= 1
            self.loadSkin(self.skins, self.skinNumber)

    def loadSkins(self):
        skins = [f.name for f in os.scandir('skins') if f.is_dir()]
        return skins

    def loadSkin(self, skins, skinNum):
        dir = 'skins/' + skins[skinNum]
        print(dir)
        self.background = pygame.image.load(dir + '/background.png')
        self.pausescreen = pygame.image.load(dir + '/pausescreen.png')
        self.titlescreen = pygame.image.load(dir + '/titlescreen.png')
        self.gameoverscreen = pygame.image.load(dir + '/losing.png')
        self.winscreen = pygame.image.load(dir + '/completion.png')

    def getFolder(self):
        return 'skins/' + str(self.skins[self.skinNumber])


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super(Player, self).__init__()

        self.image = pygame.image.load('skins/default/player.png')

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
        self.image = pygame.image.load(screen.getFolder() + '/player.png')


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self, mx, my, speed):
        # Call the parent class (Sprite) constructor
        super(Bullet, self).__init__()
        self.speed = speed

        self.image = pygame.image.load('skins/default/bullet.png')

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
