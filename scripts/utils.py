import pygame

BASE_SPRITE_PATH = 'assets/sprites/'


def load_sprite(path):
    sprite = pygame.image.load(BASE_SPRITE_PATH + path).convert()
    sprite.set_colorkey((0, 0, 0))
    return sprite
