import sys
import pygame


class Game:
    def __init__(self):
        """ Initialize pygame and setup game properties """
        pygame.init()

        # Set game window resolution and title
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('PyNinja')

        self.clock = pygame.time.Clock()

    def run(self):
        """ Main game loop """
        while True:
            self.window.fill((30, 150, 220))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)


Game().run()
