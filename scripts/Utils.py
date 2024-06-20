import os
import pygame

BASE_PATH = 'assets/images/'


def load_sprite(path):
    """ Load an image from a file and returns a Surface """
    sprite = pygame.image.load(BASE_PATH + path).convert()
    sprite.set_colorkey((0, 0, 0))
    return sprite


def load_sprites(path):
    """ Load multiple image from a directory and returns a list of Surfaces """
    sprites = []
    for file_name in sorted(os.listdir(BASE_PATH + path)):
        sprites.append(load_sprite(path + '/' + file_name))
    return sprites
