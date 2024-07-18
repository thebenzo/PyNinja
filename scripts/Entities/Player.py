import random
import math

from scripts.entities.PhysicsEntity import PhysicsEntity
from scripts.ParticleSystem import Particle


class Player(PhysicsEntity):
    """ Class representing player. Inherits from PhysicsEntity """
    def __init__(self, game, pos, size):
        super().__init__('player', game, pos, size)

        self.dead = False

        self.airborne_time = 0
        self.jump_velocity = 2.6
        self.jump_count = 2
        self.dash_velocity = 8
        # Dashing lasts for 60 frames, out of which 10 defines the action and rest defines the cooldown period
        self.dash_timeframe = 0

        # Defines wall sliding state for a frame. Resets every frame
        self.wall_slide = False

    def jump(self):
        """ Player jump action. Handles ground and wall jumps """
        if self.wall_slide:
            if self.flip and self.last_frame_movement[0] < 0:
                self.game.sfx['jump'].play()
                self.velocity[0] = 3.5
                self.velocity[1] = -2.0
                self.airborne_time = 5
                self.jump_count = max(0, self.jump_count - 1)
            elif not self.flip and self.last_frame_movement[0] > 0:
                self.game.sfx['jump'].play()
                self.velocity[0] = -3.5
                self.velocity[1] = -2.0
                self.airborne_time = 5
                self.jump_count = max(0, self.jump_count - 1)

        if self.jump_count > 0:
            self.game.sfx['jump'].play()
            self.velocity[1] = -self.jump_velocity
            self.jump_count -= 1
            self.airborne_time = 5

    def dash(self):
        """ Make player dash in its facing direction """
        if self.dash_timeframe == 0:
            self.game.sfx['dash'].play()
            if self.flip:
                self.dash_timeframe = -60
            else:
                self.dash_timeframe = 60

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.airborne_time += 1
        if self.collision_states['bottom']:
            self.jump_count = 2
            self.airborne_time = 0

        self.wall_slide = False
        if (self.collision_states['right'] or self.collision_states['left']) and self.airborne_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collision_states['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_animation_state('wall_slide')

        if not self.wall_slide:
            if self.airborne_time > 4:
                self.set_animation_state('jump')
            elif movement[0] != 0:
                self.set_animation_state('run')
            else:
                self.set_animation_state('idle')

        # If the dashing is in first 10 frames, i.e. the actual action
        if abs(self.dash_timeframe) > 50:
            self.velocity[0] = abs(self.dash_timeframe) / self.dash_timeframe * self.dash_velocity
            if abs(self.dash_timeframe) == 51:
                self.velocity[0] *= 0.1
            # Particle stream while dashing
            particle_velocity = [abs(self.dash_timeframe) / self.dash_timeframe * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.get_collision_rect().center, velocity=particle_velocity, frame=random.randint(0, 3)))
        if abs(self.dash_timeframe) in {60, 50}:
            # Particle burst at beginning and end of a dash sequence
            for i in range(10):
                # Angle in radians
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                # Calculate velocity vector from an angle in radian
                particle_velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.get_collision_rect().center, velocity=particle_velocity, frame=random.randint(0, 3)))

        if self.dash_timeframe > 0:
            self.dash_timeframe = max(0, self.dash_timeframe - 1)
        if self.dash_timeframe < 0:
            self.dash_timeframe = min(0, self.dash_timeframe + 1)

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        elif self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
