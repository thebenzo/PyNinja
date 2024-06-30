from scripts.entities.PhysicsEntity import PhysicsEntity


class Player(PhysicsEntity):
    """ Class representing player. Inherits from PhysicsEntity """
    def __init__(self, game, pos, size):
        super().__init__('player', game, pos, size)

        self.airborne_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.airborne_time += 1
        if self.collision_states['bottom']:
            self.airborne_time = 0

        if self.airborne_time > 4:
            self.set_animation_state('jump')
        elif movement[0] != 0:
            self.set_animation_state('run')
        else:
            self.set_animation_state('idle')
