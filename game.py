import sys
import pygame

pygame.init()

# Set display window properties (size and title)
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('PyNinja')

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    # Limit the game to 60 FPS
    clock.tick(60)
