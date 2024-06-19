import pygame

BASE_PATH = 'assets/images/'


def load_sprite(path):
    """ Load an image from a file and returns a Surface """
    sprite = pygame.image.load(BASE_PATH + path).convert()
    sprite.set_colorkey((0, 0, 0))
    return sprite
