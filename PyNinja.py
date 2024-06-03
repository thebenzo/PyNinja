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

        self.pos = [100, 200]

        # Movement state on x-axis
        self.movement_x = [False, False]

    def run(self):
        """ Main game loop """
        while True:
            self.window.fill((30, 150, 220))

            pygame.draw.rect(self.window, (255, 255, 255), (self.pos[0], self.pos[1], 20, 20))

            # Booleans implicitly converts to integers when arithmetic operation are performed on them
            self.pos[0] += self.movement_x[1] - self.movement_x[0]

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

            pygame.display.update()
            self.clock.tick(60)


Game().run()
