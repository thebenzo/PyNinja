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

        for i in range(8):
            self.grid_tiles[str(5 + i) + ';8'] = {'type': 'grass', 'variant': 1, 'pos': (5 + i, 8)}
            self.grid_tiles['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    def update(self):
        pass

    def __world_to_grid_pos(self, pos):
        """ Returns grid position to a corresponding world position in pixels """
        return pos[0] * self.tile_size, pos[1] * self.tile_size

    def render(self, surf):
        for tile_key in self.grid_tiles:
            tile = self.grid_tiles[tile_key]
            surf.blit(self.game.assets[tile['type']][tile['variant']], self.__world_to_grid_pos(tile['pos']))
