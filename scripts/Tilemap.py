import json
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

    def load_map(self, path):
        """ load map data from a json file """
        map_file = open(path, 'r')
        map_data = json.load(map_file)
        map_file.close()

        self.tile_size = map_data['tile_size']
        self.grid_tiles = map_data['grid_tiles']
        self.offgrid_tiles = map_data['offgrid_tiles']

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

    def get_tiles(self, type_variant, destroy=True):
        """ Return grid and offgrid tiles that matches (type, variant) tuple """
        tiles = []
        for pos in self.grid_tiles:
            tile = self.grid_tiles[pos]
            if (tile['type'], tile['variant']) in type_variant:
                tiles.append(tile.copy())
                tiles[-1]['pos'] = tiles[-1]['pos'].copy()
                tiles[-1]['pos'] = self.__grid_to_world_pos(tiles[-1]['pos'])
                if destroy:
                    del self.grid_tiles[pos]

        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in type_variant:
                tiles.append(tile.copy())
                if destroy:
                    self.offgrid_tiles.remove(tile)

        return tiles

    def check_solid_tiles_around(self, pos, flip):
        """ Check for solid tiles down to either sides of the position based on flip """
        grid_pos = self.__world_to_grid_pos((pos[0] - 7 if flip else pos[0] + 7, pos[1] + 23))
        check_pos = str(grid_pos[0]) + ';' + str(grid_pos[1])
        if check_pos in self.grid_tiles:
            if self.grid_tiles[check_pos]['type'] in PHYSICS_TILES:
                return True
        return False

    def check_solid_tile(self, pos):
        """ Check if tile at pos is a solid tile """
        grid_pos = self.__world_to_grid_pos(pos)
        check_pos = str(grid_pos[0]) + ';' + str(grid_pos[1])
        if check_pos in self.grid_tiles:
            if self.grid_tiles[check_pos]['type'] in PHYSICS_TILES:
                return True
        return False

    def get_collision_rects(self, pos):
        """ Returns a list of collision rects of tiles around a position """
        collision_rects = []
        for tile in self.__get_neighbour_tiles(pos):
            if tile['type'] in PHYSICS_TILES:
                collision_rects.append(pygame.Rect(self.__grid_to_world_pos(tile['pos']), (self.tile_size, self.tile_size)))
        return collision_rects

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for tile_key in self.grid_tiles:
            tile = self.grid_tiles[tile_key]
            world_pos = self.__grid_to_world_pos(tile['pos'])
            surf.blit(self.game.assets[tile['type']][tile['variant']], (world_pos[0] - offset[0], world_pos[1] - offset[1]))
