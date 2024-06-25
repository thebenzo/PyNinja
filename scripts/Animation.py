class Animation:
    """ Class for sprite animations """
    def __init__(self, sprites, sprite_duration=5, loop=True):
        self.sprites = sprites
        self.sprite_duration = sprite_duration
        self.loop = loop
        self.completed = False
        self.current_frame = 0

    def copy(self):
        """ Returns a copy of current object """
        return Animation(self.sprites, self.sprite_duration, self.loop)

    def update(self):
        if self.loop:
            self.current_frame = (self.current_frame + 1) % (self.sprite_duration * len(self.sprites))
        else:
            self.current_frame = min(self.current_frame + 1, self.sprite_duration * len(self.sprites) - 1)
            if self.current_frame >= self.sprite_duration * len(self.sprites) - 1:
                self.completed = True

    def get_frame_sprite(self):
        """ Return sprite to render for the current frame """
        return self.sprites[int(self.current_frame / self.sprite_duration)]
