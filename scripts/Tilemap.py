import pygame

NEIGHBOUR_OFFSETS = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (0, 0)]
PHYSICS_TILES = {'grass', 'stone'}


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

    def __grid_to_world_pos(self, pos):
        """ Returns world position in pixels to a corresponding grid position """
        return pos[0] * self.tile_size, pos[1] * self.tile_size

    def __world_to_grid_pos(self, pos):
        """ Returns grid position to a corresponding world position in pixels """
        return int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)

    def __get_neighbour_tiles(self, pos):
        """ Returns a list of tiles neighbouring a position """
        neighbour_tiles = []
        grid_pos = self.__world_to_grid_pos(pos)
        for offset in NEIGHBOUR_OFFSETS:
            check_pos = str(grid_pos[0] + offset[0]) + ';' + str(grid_pos[1] + offset[1])
            if check_pos in self.grid_tiles:
                neighbour_tiles.append(self.grid_tiles[check_pos])
        return neighbour_tiles

    def get_collision_rects(self, pos):
        """ Returns a list of collision rects of tiles around a position """
        collision_rects = []
        for tile in self.__get_neighbour_tiles(pos):
            if tile['type'] in PHYSICS_TILES:
                collision_rects.append(pygame.Rect(self.__grid_to_world_pos(tile['pos']), (self.tile_size, self.tile_size)))
        return collision_rects

    def render(self, surf, offset=(0, 0)):
        for tile_key in self.grid_tiles:
            tile = self.grid_tiles[tile_key]
            world_pos = self.__grid_to_world_pos(tile['pos'])
            surf.blit(self.game.assets[tile['type']][tile['variant']], (world_pos[0] - offset[0], world_pos[1] - offset[1]))
