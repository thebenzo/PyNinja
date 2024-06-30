import sys
import pygame

from scripts.entities.Player import Player
from scripts.Tilemap import Tilemap
from scripts.Cloud import Clouds
from scripts.Animation import Animation
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
            'grass': load_sprites('tiles/grass'),
            'stone': load_sprites('tiles/stone'),
            'clouds': load_sprites('clouds'),
            'decor': load_sprites('tiles/decor'),
            'player/idle': Animation(load_sprites('entities/player/idle'), sprite_duration=6),
            'player/run': Animation(load_sprites('entities/player/run'), sprite_duration=4),
            'player/jump': Animation(load_sprites('entities/player/jump'))
        }

        self.player = Player(self, (100, 50), (8, 15))
        self.jump_force = 2

        # Movement state on x-axis
        self.movement_x = [False, False]

        # Camera
        self.camera_scroll = [0, 0]

        self.tilemap = Tilemap(self)

        self.clouds = Clouds(self.assets['clouds'])

    def run(self):
        """ Main game loop """
        while True:
            self.viewport.blit(self.assets['background'], (0, 0))

            self.camera_scroll[0] += (self.player.get_collision_rect().centerx - self.viewport.get_width() / 2 - self.camera_scroll[0]) / 30
            self.camera_scroll[1] += (self.player.get_collision_rect().centery - self.viewport.get_height() / 2 - self.camera_scroll[1]) / 30
            render_scroll = (int(self.camera_scroll[0]), int(self.camera_scroll[1]))

            self.clouds.update()
            self.clouds.render(self.viewport, render_scroll)

            self.tilemap.render(self.viewport, render_scroll)

            # Booleans implicitly converts to integers when arithmetic operation are performed on them
            self.player.update(self.tilemap, (self.movement_x[1] - self.movement_x[0], 0))
            self.player.render(self.viewport, render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement_x[0] = True
                    if event.key == pygame.K_d:
                        self.movement_x[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -self.jump_force
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
