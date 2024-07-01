class Particle:
    def __init__(self, game, particle_type, pos, velocity=[0, 0], frame=0):
        self.game = game
        self.type = particle_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + particle_type].copy()
        self.animation.current_frame = frame

    def update(self):
        destroy = False
        if self.animation.completed:
            destroy = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return destroy

    def render(self, surface, offset=(0, 0)):
        sprite = self.animation.get_frame_sprite()
        surface.blit(sprite, (self.pos[0] - offset[0] - sprite.get_width() // 2, self.pos[1] - offset[1] - sprite.get_height() // 2))
