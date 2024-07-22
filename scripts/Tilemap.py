import json
import pygame

AUTO_TILE_TYPES = {'grass', 'stone'}
AUTO_TILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}


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

    def render_tile_rects(self, surf, offset=(0, 0)):
        """ Render debug rects around tiles """
        for tile in self.offgrid_tiles:
            tile_sprite = self.game.assets[tile['type']][tile['variant']]
            tile_rect = pygame.Rect(tile['pos'][0] - offset[0], tile['pos'][1] - offset[1], tile_sprite.get_width(), tile_sprite.get_height())
            pygame.draw.rect(surf, (255, 255, 255), tile_rect, 1)

        for tile_key in self.grid_tiles:
            tile = self.grid_tiles[tile_key]
            world_pos = self.grid_to_world_pos(tile['pos'])
            tile_sprite = self.game.assets[tile['type']][tile['variant']]
            tile_rect = pygame.Rect(world_pos[0] - offset[0], world_pos[1] - offset[1], tile_sprite.get_width(), tile_sprite.get_height())
            pygame.draw.rect(surf, (0, 0, 255), tile_rect, 1)

    def auto_tile(self):
        for key in self.grid_tiles:
            tile = self.grid_tiles[key]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_tile = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_tile in self.grid_tiles:
                    if self.grid_tiles[check_tile]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTO_TILE_TYPES) and (neighbors in AUTO_TILE_MAP):
                tile['variant'] = AUTO_TILE_MAP[neighbors]

    def save_map(self, path):
        """ Save map to a json file at path specified """
        map_file = open(path, 'w')
        json.dump({'tile_size': self.tile_size, 'grid_tiles': self.grid_tiles, 'offgrid_tiles': self.offgrid_tiles}, map_file)
        map_file.close()

    def load_map(self, path):
        """ load map data from a json file """
        map_file = open(path, 'r')
        map_data = json.load(map_file)
        map_file.close()

        self.tile_size = map_data['tile_size']
        self.grid_tiles = map_data['grid_tiles']
        self.offgrid_tiles = map_data['offgrid_tiles']

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for tile_key in self.grid_tiles:
            tile = self.grid_tiles[tile_key]
            world_pos = self.grid_to_world_pos(tile['pos'])
            surf.blit(self.game.assets[tile['type']][tile['variant']], (world_pos[0] - offset[0], world_pos[1] - offset[1]))
