import pygame
import random

#       --- Classes ---


class Duck(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super(Duck, self).__init__()

        self.image = pygame.image.load('images/duck.png')

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

        self.image = pygame.image.load('images/dog.png')

        self.rect = self.image.get_rect()

    def update(self):

        self.rect.x = 350
        self.rect.y = 450


class Tomato(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self, mx, my):
        # Call the parent class (Sprite) constructor
        super(Tomato, self).__init__()
        self.speed = 50

        self.image = pygame.image.load('images/tomato.png')

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1, 891)
        self.rect.y = 608

        self.xdir = (mx - self.rect.x)/50
        self.ydir = (self.rect.y - my)/50

    def update(self):
        """ Move the bullet. """

        self.rect.x += self.xdir
        self.rect.y -= self.ydir
