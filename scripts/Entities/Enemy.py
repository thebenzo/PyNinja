import random

from scripts.entities.PhysicsEntity import PhysicsEntity


class Enemy(PhysicsEntity):
    """ Class representing enemy. Inherits from PhysicsEntity """
    def __init__(self, game, pos, size):
        super().__init__('enemy', game, pos, size)

        self.walking_timeframe = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        if self.walking_timeframe:
            pass
        elif random.random() < 0.01:
            self.walking_timeframe = random.randint(30, 120)

    def render(self, surface, offset=(0, 0)):
        super().render(surface, offset=offset)
