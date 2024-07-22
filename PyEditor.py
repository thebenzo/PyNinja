import sys
import pygame

from scripts.Tilemap import Tilemap
from scripts.Utils import load_sprite, load_sprites


class Editor:
    def __init__(self):
        """ Initialize pygame and setup game properties """
        pygame.init()

        # Set game window resolution and title
        self.window_size = (872, 960)
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('PyEditor')

        # Game is rendered on this surface, and it's later scaled to match windows size
        self.viewport_size = (320, 240)
        self.scaled_viewport_size = (840, 630)
        self.viewport_pos = (16, 26)
        self.viewport = pygame.Surface(self.viewport_size)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font('assets/CascadiaCode-Regular.ttf', 14)

        self.level = 0

        self.background = load_sprite('background.png')

        # Dictionary to store game asset objects mapped to their name string as key
        self.assets = {
            'grass': load_sprites('tiles/grass'),
            'stone': load_sprites('tiles/stone'),
            'decor': load_sprites('tiles/decor'),
            'spawners': load_sprites('tiles/spawners'),
            'large_decor': load_sprites('tiles/large_decor')
        }

        self.tilemap = Tilemap(self)

        self.selected_tile = None

        # Movement state on both axes [Left, Right, Up, Down]
        self.movement = [False, False, False, False]

        self.left_clicking = False
        self.right_clicking = False
        self.ctrl = False
        self.snap_to_grid = False
        self.debug_rects = False
        self.map_changed = False

        # Camera
        self.camera_scroll = [0, 0]
        self.scroll_speed = 2

    def run(self):
        """ Main game loop """
        while True:
            self.window.fill((144, 201, 120))
            self.viewport.blit(self.background, (0, 0))

            level_text = f'{'*' if self.map_changed else ''}map{self.level}.json [Use ↑ or ↓ to change map]'
            level_text_surface = self.font.render(level_text, True, (255, 25, 25) if self.map_changed else (30, 30, 30))
            self.window.blit(level_text_surface, (840 / 2 - level_text_surface.get_width() / 2, 4))

            save_info_text = 'lCTRL + S to save map'
            load_info_text = '(O) to load current map.'
            auto_tile_info_text = '(SPACE) to auto-tile.'
            clear_info_text = 'Del to clear map.'
            save_info_text_surface = self.font.render(save_info_text, True, (30, 30, 30))
            load_info_text_surface = self.font.render(load_info_text, True, (30, 30, 30))
            clear_info_text_surface = self.font.render(clear_info_text, True, (30, 30, 30))
            auto_tile_info_text_surface = self.font.render(auto_tile_info_text, True, (30, 30, 30))
            self.window.blit(save_info_text_surface, (self.window_size[0] - save_info_text_surface.get_width() - 16,
                                                           740 + save_info_text_surface.get_height()))
            self.window.blit(load_info_text_surface, (self.window_size[0] - load_info_text_surface.get_width() - 16,
                                                           760 + load_info_text_surface.get_height() + 10))
            self.window.blit(auto_tile_info_text_surface, (self.window_size[0] - auto_tile_info_text_surface.get_width() - 16,
                                                                780 + auto_tile_info_text_surface.get_height() + 20))
            self.window.blit(clear_info_text_surface, (self.window_size[0] - clear_info_text_surface.get_width() - 16,
                                                            800 + clear_info_text_surface.get_height() + 30))

            self.camera_scroll[0] += (self.movement[1] - self.movement[0]) * self.scroll_speed
            self.camera_scroll[1] += (self.movement[3] - self.movement[2]) * self.scroll_speed
            render_scroll = (int(self.camera_scroll[0]), int(self.camera_scroll[1]))
            self.tilemap.render(self.viewport, render_scroll)

            if self.debug_rects:
                self.tilemap.render_tile_rects(self.viewport, render_scroll)

            mouse_pos = pygame.mouse.get_pos()

            col, row = 0, 0
            for tile_group in list(self.assets):
                font_surface = self.font.render(tile_group + ': ', True, (30, 30, 30))
                self.window.blit(font_surface, (16 + col, 676 + row))
                col += font_surface.get_width() + 10
                for i in range(len(self.assets[tile_group])):
                    sprite = pygame.transform.scale(self.assets[tile_group][i], (self.assets[tile_group][i].get_width() * 2, self.assets[tile_group][i].get_height() * 2))
                    sprite_rect = pygame.Rect(16 + col, 670 + row, sprite.get_width(), sprite.get_height())
                    self.window.blit(sprite, (16 + col, 670 + row))
                    if sprite_rect.collidepoint(mouse_pos):
                        if pygame.mouse.get_pressed()[0]:
                            self.selected_tile = {'sprite': self.assets[tile_group][i], 'type': tile_group, 'variant': i, 'rect': sprite_rect}
                    col += sprite.get_width() + 20
                row += sprite.get_height() + 15
                col = 0

            viewport_rect = pygame.Rect(self.viewport_pos, self.scaled_viewport_size)
            viewport_mouse_pos = ((mouse_pos[0] - self.viewport_pos[0]) * self.viewport_size[0] / self.scaled_viewport_size[0],
                                  (mouse_pos[1] - self.viewport_pos[1]) * self.viewport_size[1] / self.scaled_viewport_size[1])

            if self.selected_tile and viewport_rect.collidepoint(mouse_pos):
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)

            # Render ghost tile for the game viewport
            if self.selected_tile and viewport_rect.collidepoint(mouse_pos):
                ghost_tile = self.selected_tile['sprite'].copy()
                ghost_tile.set_alpha(150)
                ghost_tile_pos = (viewport_mouse_pos[0] - ghost_tile.get_width() / 2, viewport_mouse_pos[1] - ghost_tile.get_height() / 2)
                ghost_tile_grid_pos = self.tilemap.world_to_grid_pos(ghost_tile_pos)
                self.viewport.blit(ghost_tile, self.tilemap.grid_to_world_pos(ghost_tile_grid_pos) if self.snap_to_grid else ghost_tile_pos)

            # Draw border around selected tile
            if self.selected_tile:
                pygame.draw.rect(self.window, (200, 25, 25), self.selected_tile['rect'], 3)

            # Place off-gird tiles
            if not self.snap_to_grid and self.left_clicking and self.selected_tile and viewport_rect.collidepoint(mouse_pos):
                offgrid_tile_pos = (viewport_mouse_pos[0] + self.camera_scroll[0] - self.selected_tile['sprite'].get_width() / 2,
                                    viewport_mouse_pos[1] + self.camera_scroll[1] - self.selected_tile['sprite'].get_height() / 2)
                offgrid_tile = {'type': self.selected_tile['type'], 'variant': self.selected_tile['variant'], 'pos': offgrid_tile_pos}
                self.tilemap.offgrid_tiles.append(offgrid_tile)
                self.left_clicking = False
                self.map_changed = True

            # Place grid tiles
            if self.snap_to_grid and self.left_clicking and self.selected_tile and viewport_rect.collidepoint(mouse_pos):
                grid_tile_pos = self.tilemap.world_to_grid_pos((viewport_mouse_pos[0] + self.camera_scroll[0] - self.selected_tile['sprite'].get_width() / 2,
                                                                viewport_mouse_pos[1] + self.camera_scroll[1] - self.selected_tile['sprite'].get_height() / 2))
                grid_tile = {'type': self.selected_tile['type'], 'variant': self.selected_tile['variant'], 'pos': grid_tile_pos}
                self.tilemap.grid_tiles[str(grid_tile_pos[0]) + ';' + str(grid_tile_pos[1])] = grid_tile
                self.left_clicking = False
                self.map_changed = True

            if self.right_clicking and viewport_rect.collidepoint(mouse_pos):
                # Remove grid tiles from the tilemap
                grid_tile_pos = self.tilemap.world_to_grid_pos((viewport_mouse_pos[0] + self.camera_scroll[0] - 16,
                                                                viewport_mouse_pos[1] + self.camera_scroll[1] - 16))
                tilemap_key = str(grid_tile_pos[0]) + ';' + str(grid_tile_pos[1])
                if tilemap_key in self.tilemap.grid_tiles:
                    del self.tilemap.grid_tiles[tilemap_key]
                    self.map_changed = True

                # Remove offgrid tiles from the tilemap
                offgrid_tile_pos = (viewport_mouse_pos[0] + self.camera_scroll[0],
                                    viewport_mouse_pos[1] + self.camera_scroll[1])
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_sprite = self.assets[tile['type']][tile['variant']]
                    tile_rect = pygame.Rect(tile['pos'][0] - self.camera_scroll[0], tile['pos'][1] - self.camera_scroll[1],
                                            tile_sprite.get_width(), tile_sprite.get_height())
                    if tile_rect.collidepoint(offgrid_tile_pos):
                        self.tilemap.offgrid_tiles.remove(tile)
                        self.map_changed = True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_UP:
                        self.level += 1
                    if event.key == pygame.K_DOWN:
                        self.level = max(self.level - 1, 0)
                    if event.key == pygame.K_g:
                        self.snap_to_grid = not self.snap_to_grid
                    if event.key == pygame.K_v:
                        self.debug_rects = not self.debug_rects
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = True
                    if self.ctrl and event.key == pygame.K_s:
                        self.tilemap.save_map(f'assets/maps/map{self.level}.json')
                        self.map_changed = False
                    if event.key == pygame.K_o:
                        try:
                            self.tilemap.load_map(f'assets/maps/map{self.level}.json')
                        except FileNotFoundError:
                            print(f'map{self.level}.json does not exist')
                    if event.key == pygame.K_SPACE:
                        self.tilemap.auto_tile()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.left_clicking = True
                    if event.button == 3:
                        self.right_clicking = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.left_clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.window, (50, 50, 50), pygame.Rect(12, 22, 848, 638))
            # Viewport is rendered in the main window and is scaled to match its size to mimic a zoomed-in effect
            self.window.blit(pygame.transform.scale(self.viewport, self.scaled_viewport_size), self.viewport_pos)

            snap_to_grid_status_text = self.font.render(f'Snap to grid (G): {self.snap_to_grid}', True, (0, 0, 0))
            debug_status_text = self.font.render(f'Debug Rects (V): {self.debug_rects}', True, (0, 0, 0))
            self.window.blit(snap_to_grid_status_text, (self.viewport_pos[0] + 10, self.viewport_pos[1] + 10))
            self.window.blit(debug_status_text, (self.viewport_pos[0] + self.scaled_viewport_size[0] - debug_status_text.get_width() - 10, self.viewport_pos[1] + 10))

            pygame.display.update()
            self.clock.tick(60)


Editor().run()
