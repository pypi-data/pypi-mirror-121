import pygame

from aerforge.error import *

class Sprite:
    def __init__(self, window, image, x, y, width = 200, height = 200):
        self.image = pygame.image.load(image)

        if width != None and height != None:
            self.image = pygame.transform.scale(self.image, (height, width))

        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.window.window.blit(self.image, (self.x, self.y))

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def center(self):
        self.x = self.window.width / 2 - self.width / 2
        self.y = self.window.height / 2 - self.height / 2

    def center_x(self):
        self.x = self.window.width / 2 - self.width / 2

    def center_y(self):
        self.y = self.window.height / 2 - self.height / 2