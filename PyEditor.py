import sys
import pygame

from scripts.Tilemap import Tilemap
from scripts.Utils import load_sprite, load_sprites


class Editor:
    def __init__(self):
        """ Initialize pygame and setup game properties """
        pygame.init()

        # Set game window resolution and title
        self.window = pygame.display.set_mode((872, 960))
        pygame.display.set_caption('PyEditor')

        # Game is rendered on this surface, and it's later scaled to match windows size
        self.viewport = pygame.Surface((320, 240))

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
        self.selected_tile_sprite = None

        # Movement state on both axes [Left, Right, Up, Down]
        self.movement = [False, False, False, False]

        # Camera
        self.camera_scroll = [0, 0]
        self.scroll_speed = 2

    def run(self):
        """ Main game loop """
        while True:
            self.window.fill((144, 201, 120))
            self.viewport.blit(self.background, (0, 0))

            level_text = f'map{self.level}.json'
            level_text_surface = self.font.render(level_text, True, (30, 30, 30))
            self.window.blit(level_text_surface, (840 / 2 - level_text_surface.get_width() / 2, 4))

            self.camera_scroll[0] += (self.movement[1] - self.movement[0]) * self.scroll_speed
            self.camera_scroll[1] += (self.movement[3] - self.movement[2]) * self.scroll_speed
            render_scroll = (int(self.camera_scroll[0]), int(self.camera_scroll[1]))
            self.tilemap.render(self.viewport, render_scroll)

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
                            self.selected_tile_sprite = self.assets[tile_group][i]
                            selected_sprite_rect = sprite_rect
                    col += sprite.get_width() + 20
                row += sprite.get_height() + 15
                col = 0

            if self.selected_tile_sprite:
                pygame.draw.rect(self.window, (200, 25, 25), selected_sprite_rect, 3)

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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.window, (50, 50, 50), pygame.Rect(12, 22, 848, 638))
            # Viewport is rendered in the main window and is scaled to match its size to mimic a zoomed-in effect
            self.window.blit(pygame.transform.scale(self.viewport, (840, 630)), (16, 26))

            pygame.display.update()
            self.clock.tick(60)


Editor().run()
