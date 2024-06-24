import pygame


class PhysicsEntity:
    """ Class for a game entity that simulates physics """
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.velocity = [0.0, 0.0]
        self.terminal_velocity_y = 5.0
        self.gravity = 0.1

        # Defines collision states in four directions
        self.collision_states = {'top': False, 'right': False, 'bottom': False, 'left': False}

    def get_collision_rect(self):
        """ Return a collision rect at entity position """
        return pygame.Rect(self.pos, self.size)

    def update(self, tilemap, movement=(0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Reset collision states
        self.collision_states = {'top': False, 'right': False, 'bottom': False, 'left': False}

        self.pos[0] += frame_movement[0]
        entity_rect = self.get_collision_rect()
        for tile_rect in tilemap.get_collision_rects(self.pos):
            if entity_rect.colliderect(tile_rect):
                if frame_movement[0] > 0:
                    entity_rect.right = tile_rect.left
                    self.collision_states['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = tile_rect.right
                    self.collision_states['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.get_collision_rect()
        for tile_rect in tilemap.get_collision_rects(self.pos):
            if entity_rect.colliderect(tile_rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = tile_rect.top
                    self.collision_states['bottom'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = tile_rect.bottom
                    self.collision_states['top'] = True
                self.pos[1] = entity_rect.y

        # Apply gravity to the entity with a terminal velocity in y-axis
        self.velocity[1] = min(self.terminal_velocity_y, self.velocity[1] + self.gravity)

        # Reset the y velocity if entity is colliding at top or bottom
        if self.collision_states['top'] or self.collision_states['bottom']:
            self.velocity[1] = 0

    def render(self, surface, offset=(0, 0)):
        surface.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
