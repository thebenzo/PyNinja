import sys
import pygame


class Game:
    def __init__(self):
        pygame.init()

        # Set display window properties (size and title)
        self.window = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('PyNinja')

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            # Limit the game to 60 FPS
            self.clock.tick(60)


Game().run()
