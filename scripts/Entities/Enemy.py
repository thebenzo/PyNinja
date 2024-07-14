import random

import pygame

from scripts.entities.PhysicsEntity import PhysicsEntity


class Enemy(PhysicsEntity):
    """ Class representing enemy. Inherits from PhysicsEntity """
    def __init__(self, game, pos, size):
        super().__init__('enemy', game, pos, size)

        self.walking_timeframe = 0

    def update(self, tilemap, movement=(0, 0)):
        if self.walking_timeframe:
            if tilemap.check_solid_tiles_around(self.get_collision_rect().center, self.flip):
                movement = (movement[0] - 0.5 if self.flip else movement[0] + 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking_timeframe = max(0, self.walking_timeframe - 1)
            if not self.walking_timeframe:
                distance = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                # Check if player is at same y-level as enemy
                if abs(distance[1] < 16):
                    if distance[0] < 0 and self.flip:
                        self.game.projectiles.append({'pos': [self.get_collision_rect().centerx - 7, self.get_collision_rect().centery], 'velocity': -1.5, 'lifespan': 360})
                    elif distance[0] > 0 and not self.flip:
                        self.game.projectiles.append({'pos': [self.get_collision_rect().centerx + 7, self.get_collision_rect().centery], 'velocity': 1.5, 'lifespan': 360})
        elif random.random() < 0.01:
            self.walking_timeframe = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_animation_state('run')
        else:
            self.set_animation_state('idle')

        if abs(self.game.player.dash_timeframe) >= 50:
            if self.get_collision_rect().colliderect(self.game.player.get_collision_rect()):
                return True

    def render(self, surface, offset=(0, 0)):
        super().render(surface, offset=offset)

        if self.flip:
            surface.blit(pygame.transform.flip(self.game.assets['gun'], True, False),
                         (self.get_collision_rect().centerx - 3 - self.game.assets['gun'].get_width() - offset[0],
                          self.get_collision_rect().centery - offset[1]))
        else:
            surface.blit(self.game.assets['gun'], (self.get_collision_rect().centerx + 3 - offset[0],
                         self.get_collision_rect().centery - offset[1]))
