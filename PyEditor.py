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

        # Dictionary to store game asset objects mapped to their name string as key
        self.assets = {
            'background': load_sprite('background.png'),
            'grass': load_sprites('tiles/grass'),
            'stone': load_sprites('tiles/stone'),
            'clouds': load_sprites('clouds'),
            'decor': load_sprites('tiles/decor'),
            'spawners': load_sprites('tiles/spawners'),
            'large_decor': load_sprites('tiles/large_decor'),
        }

        # Movement state on both axes [Left, Right, Up, Down]
        self.movement = [False, False, False, False]

        # Camera
        self.camera_scroll = [0, 0]

        self.tilemap = Tilemap(self)

    def run(self):
        """ Main game loop """
        while True:
            self.window.fill((0, 0, 0))
            self.viewport.blit(self.assets['background'], (0, 0))

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

            # Viewport is rendered in the main window and is scaled to match its size to mimic a zoomed-in effect
            self.window.blit(pygame.transform.scale(self.viewport, (840, 630)), (16, 16))

            pygame.display.update()
            self.clock.tick(60)


Editor().run()
