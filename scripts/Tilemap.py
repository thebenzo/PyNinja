import pygame


class Tilemap:
    """ Class for tilemap of the game world made up of grid and offgrid tile """
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size

        # Stores tiles that align to the grid. Each tile is stored as a dictionary mapped to grid position string
        # Since the majority of game world is air, we store tiles in a sparse matrix represented by a dictionary
        self.grid_tiles = {}
        self.offgrid_tiles = []

    def grid_to_world_pos(self, pos):
        """ Returns world position in pixels to a corresponding grid position """
        return pos[0] * self.tile_size, pos[1] * self.tile_size

    def world_to_grid_pos(self, pos):
        """ Returns grid position to a corresponding world position in pixels """
        return int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for tile_key in self.grid_tiles:
            tile = self.grid_tiles[tile_key]
            world_pos = self.grid_to_world_pos(tile['pos'])
            surf.blit(self.game.assets[tile['type']][tile['variant']], (world_pos[0] - offset[0], world_pos[1] - offset[1]))
