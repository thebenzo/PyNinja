import sys
import pygame

from scripts.utils import load_sprite
from scripts.entities import PhysicsEntity


class Game:
    def __init__(self):
        pygame.init()

        # Set display window properties (size and title)
        self.window = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('PyNinja')

        # All rendering is done on this surface. It is later scaled to window size
        self.viewport = pygame.Surface((640, 360))

        # Dictionary of game assets with entityType as the key
        self.assets = {
            'player': load_sprite('entities/player.png')
        }

        # The boolean list represents [left, right] movement
        self.movement = [False, False]

        self.player = PhysicsEntity(self, 'player', (200, 100), (10, 15))

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.viewport.fill((78, 159, 229))

            ''' This takes benefit of the fact that booleans convert to integer value implicitly 
                when used with arithmetic operators. '''
            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.viewport)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            # Scaling viewport to match window size which gives a zoomed-in view to the game world
            self.window.blit(pygame.transform.scale(self.viewport, self.window.get_size()), (0, 0))

            pygame.display.update()
            # Limit the game to 60 FPS
            self.clock.tick(60)


Game().run()
