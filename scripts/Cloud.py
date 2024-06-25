import random


class Cloud:
    """ Class for a single cloud entity """
    def __init__(self, pos, speed, sprite, z_depth):
        self.pos = list(pos)
        self.speed = speed
        self.cloud_sprite = sprite
        self.z_depth = z_depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surface, offset=(0, 0)):
        # Multiplying pos with z-depth gives parallax effect to clouds
        render_pos = (self.pos[0] - offset[0] * self.z_depth, self.pos[1] - offset[1] * self.z_depth)

        # Mod let the clouds loop across screen enabling entity pooling
        surface.blit(self.cloud_sprite, (render_pos[0] % (surface.get_width() + self.cloud_sprite.get_width()) - self.cloud_sprite.get_width(),
                                         render_pos[1] % (surface.get_height() + self.cloud_sprite.get_height()) - self.cloud_sprite.get_height()))


class Clouds:
    """ Class representing a list of clouds. It is responsible for instantiating and updating each cloud entity """
    def __init__(self, cloud_sprites, count=12):
        self.clouds = []

        for i in range(count):
            self.clouds.append(Cloud((random.random() * 9999, random.random() * 9999), random.random() * 0.05 + 0.05, random.choice(cloud_sprites), random.random() * 0.6 + 0.2))

        # Sort cloud based on z-depth so that clouds in front are rendered over the ones in back
        self.clouds.sort(key=lambda x: x.z_depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surface, offset)
