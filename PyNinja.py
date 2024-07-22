import sys
import os
import math
import random
import pygame

from scripts.Entities.Player import Player
from scripts.Entities.Enemy import Enemy
from scripts.Tilemap import Tilemap
from scripts.Cloud import Clouds
from scripts.Animation import Animation
from scripts.Utils import load_sprite, load_sprites
from scripts.ParticleSystem import Particle
from scripts.Spark import Spark


class Game:
    def __init__(self):
        """ Initialize pygame and setup game properties """
        pygame.init()

        # Set game window resolution and title
        self.window = pygame.display.set_mode((840, 630))
        pygame.display.set_caption('PyNinja')

        # Game is rendered on this surface, and it's later scaled to match windows size
        self.viewport = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        # Dictionary to store game asset objects mapped to their name string as key
        self.assets = {
            'background': load_sprite('background.png'),
            'grass': load_sprites('tiles/grass'),
            'stone': load_sprites('tiles/stone'),
            'clouds': load_sprites('clouds'),
            'decor': load_sprites('tiles/decor'),
            'spawners': load_sprites('tiles/spawners'),
            'gun': load_sprite('gun.png'),
            'bullet': load_sprite('projectile.png'),
            'large_decor': load_sprites('tiles/large_decor'),
            'player/idle': Animation(load_sprites('entities/player/idle'), sprite_duration=6),
            'player/run': Animation(load_sprites('entities/player/run'), sprite_duration=4),
            'player/jump': Animation(load_sprites('entities/player/jump')),
            'player/wall_slide': Animation(load_sprites('entities/player/wall_slide')),
            'enemy/idle': Animation(load_sprites('entities/enemy/idle'), sprite_duration=6),
            'enemy/run': Animation(load_sprites('entities/enemy/run'), sprite_duration=4),
            'particle/leaf': Animation(load_sprites('particles/leaf'), sprite_duration=16, loop=False),
            'particle/particle': Animation(load_sprites('particles/particle'), sprite_duration=6, loop=False)
        }

        # Dictionary to store game sound effects mapped to their name string as key
        self.sfx = {
            'ambience': pygame.mixer.Sound('assets/sfx/ambience.wav'),
            'dash': pygame.mixer.Sound('assets/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('assets/sfx/hit.wav'),
            'jump': pygame.mixer.Sound('assets/sfx/jump.wav'),
            'shoot': pygame.mixer.Sound('assets/sfx/shoot.wav')
        }

        self.sfx['ambience'].set_volume(0.3)
        self.sfx['dash'].set_volume(0.2)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['jump'].set_volume(0.6)
        self.sfx['shoot'].set_volume(0.5)

        self.player = None

        # Movement state on x-axis
        self.movement_x = [False, False]

        # Camera
        self.camera_scroll = [0, 0]
        self.screen_shake_strength = 0

        self.tilemap = Tilemap(self)

        self.clouds = Clouds(self.assets['clouds'])

        self.enemies = []

        self.projectiles = []

        # Particle System
        self.particles = []
        self.leaf_Spawner = []
        self.sparks = []

        self.respawn_timer = 0
        self.transition_timer = 0

        self.level = 0
        self.load_level(self.level)

    def load_level(self, map_id):
        self.tilemap.load_map(f'assets/maps/map{map_id}.json')

        self.particles = []
        self.sparks = []

        self.camera_scroll = [0, 0]

        self.respawn_timer = 0
        self.transition_timer = -30

        self.leaf_Spawner = []
        for tree in self.tilemap.get_tiles([('large_decor', 2)], destroy=False):
            self.leaf_Spawner.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.get_tiles([('spawners', 0), ('spawners', 1)], destroy=True):
            if spawner['variant'] == 0:
                self.player = Player(self, list(spawner['pos']), (8, 15))
                self.player.dead = False
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

    def run(self):
        """ Main game loop """
        pygame.mixer.music.load('assets/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.sfx['ambience'].play(-1)

        while True:
            self.viewport.blit(self.assets['background'], (0, 0))

            self.screen_shake_strength = max(0, self.screen_shake_strength - 1)

            self.camera_scroll[0] += (self.player.get_collision_rect().centerx - self.viewport.get_width() / 2 - self.camera_scroll[0]) / 30
            self.camera_scroll[1] += (self.player.get_collision_rect().centery - self.viewport.get_height() / 2 - self.camera_scroll[1]) / 30
            render_scroll = (int(self.camera_scroll[0]), int(self.camera_scroll[1]))

            self.clouds.update()
            self.clouds.render(self.viewport, render_scroll)

            self.tilemap.render(self.viewport, render_scroll)

            if self.player.dead:
                self.respawn_timer += 1
                if self.respawn_timer >= 10:
                    self.transition_timer = min(30, self.transition_timer + 1)
                if self.respawn_timer > 40:
                    self.load_level(self.level)

            if not len(self.enemies):
                self.transition_timer += 1
                if self.transition_timer > 30:
                    self.level = min(self.level + 1, len(os.listdir('assets/maps')) - 1)
                    self.load_level(self.level)
            if self.transition_timer < 0:
                self.transition_timer += 1

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.viewport, render_scroll)

                if kill:
                    self.enemies.remove(enemy)

            if not self.player.dead:
                # Booleans implicitly converts to integers when arithmetic operation are performed on them
                self.player.update(self.tilemap, (self.movement_x[1] - self.movement_x[0], 0))
                self.player.render(self.viewport, render_scroll)

            # Projectile is represented as dictionary {pos, velocity, lifespan}
            for projectile in self.projectiles.copy():
                projectile['pos'][0] += projectile['velocity']
                projectile['lifespan'] -= 1
                bullet_sprite = self.assets['bullet']
                self.viewport.blit(bullet_sprite, (projectile['pos'][0] - bullet_sprite.get_width() / 2 - render_scroll[0],
                                                        projectile['pos'][1] - bullet_sprite.get_height() / 2 - render_scroll[1]))
                if projectile['lifespan'] == 0:
                    self.projectiles.remove(projectile)
                elif self.tilemap.check_solid_tile(projectile['pos']):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile['pos'], random.random() - 0.5 + (math.pi if projectile['velocity'] > 0 else 0), random.random() + 2))
                elif abs(self.player.dash_timeframe) < 50:
                    if self.player.get_collision_rect().collidepoint(projectile['pos']):
                        self.projectiles.remove(projectile)
                        self.sfx['hit'].play()
                        self.screen_shake_strength = max(16, self.screen_shake_strength)
                        self.player.dead = True
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.get_collision_rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.get_collision_rect().center,
                                                           [math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], random.randint(0, 3)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.viewport, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for rect in self.leaf_Spawner:
                if random.random() * 99999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 17)))

            for particle in self.particles.copy():
                destroy = particle.update()
                particle.render(self.viewport, render_scroll)
                if particle.type == 'leaf':
                    # Using property of sine wave to imitate swaying effect on the leaf particles
                    particle.pos[0] += math.sin(particle.animation.current_frame * 0.04) * 0.3
                if destroy:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement_x[0] = True
                    if event.key == pygame.K_d:
                        self.movement_x[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_x:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement_x[0] = False
                    if event.key == pygame.K_d:
                        self.movement_x[1] = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.transition_timer:
                transition_surf = pygame.Surface(self.viewport.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.viewport.get_width() // 2, self.viewport.get_height() // 2), (30 - abs(self.transition_timer)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.viewport.blit(transition_surf, (0, 0))

            screen_shake_offset = (random.random() * self.screen_shake_strength - self.screen_shake_strength / 2,
                                   random.random() * self.screen_shake_strength - self.screen_shake_strength / 2)

            # Viewport is rendered in the main window and is scaled to match its size to mimic a zoomed-in effect
            self.window.blit(pygame.transform.scale(self.viewport, self.window.get_size()), screen_shake_offset)

            pygame.display.update()
            self.clock.tick(60)


Game().run()
