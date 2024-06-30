import pygame


class PhysicsEntity:
    """ Class for a game entity that simulates physics """
    def __init__(self, name, game, pos, size):
        self.entity_name = name
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.velocity = [0.0, 0.0]
        self.terminal_velocity_y = 5.0
        self.gravity = 0.1

        # Defines collision states in four directions
        self.collision_states = {'top': False, 'right': False, 'bottom': False, 'left': False}

        # Animation States
        self.state = ''
        self.flip = False
        self.set_animation_state('idle')
        self.anim_offset = (-3, -3)

    def get_collision_rect(self):
        """ Return a collision rect at entity position """
        return pygame.Rect(self.pos, self.size)

    def set_animation_state(self, state):
        """ Change animation state to the one passed as string """
        if state != self.state:
            self.state = state
            self.animation = self.game.assets[self.entity_name + '/' + self.state].copy()

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

        # Flip the entity to face the move direction
        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True

        # Apply gravity to the entity with a terminal velocity in y-axis
        self.velocity[1] = min(self.terminal_velocity_y, self.velocity[1] + self.gravity)

        # Reset the y velocity if entity is colliding at top or bottom
        if self.collision_states['top'] or self.collision_states['bottom']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.flip(self.animation.get_frame_sprite(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0],
                                                                                                        self.pos[1] - offset[1]+ self.anim_offset[1]))
