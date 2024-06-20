import sys
import pygame

from scripts.entities.PhysicsEntity import PhysicsEntity
from scripts.Tilemap import Tilemap
from scripts.Utils import load_sprite, load_sprites


class Game:
    def __init__(self):
        """ Initialize pygame and setup game properties """
        pygame.init()

        # Set game window resolution and title
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('PyNinja')

        # Game is rendered on this surface, and it's later scaled to match windows size
        self.viewport = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        # Dictionary to store game asset objects mapped to their name string as key
        self.assets = {
            'background': load_sprite('background.png'),
            'player': load_sprite('entities/player.png'),
            'grass': load_sprites('tiles/grass'),
            'stone': load_sprites('tiles/stone')
        }

        self.player = PhysicsEntity(self, (50, 50), (15, 8))

        # Movement state on x-axis
        self.movement_x = [False, False]

        self.tilemap = Tilemap(self)

    def run(self):
        """ Main game loop """
        while True:
            self.viewport.blit(self.assets['background'], (0, 0))

            # Booleans implicitly converts to integers when arithmetic operation are performed on them
            self.player.update((self.movement_x[1] - self.movement_x[0], 0))
            self.player.render(self.viewport)

            self.tilemap.render(self.viewport)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement_x[0] = True
                    if event.key == pygame.K_d:
                        self.movement_x[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement_x[0] = False
                    if event.key == pygame.K_d:
                        self.movement_x[1] = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Viewport is rendered in the main window and is scaled to match its size to mimic a zoomed-in effect
            self.window.blit(pygame.transform.scale(self.viewport, self.window.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)


Game().run()
