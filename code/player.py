from pygame.sprite import collide_mask

from settings import *
from collision import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, enemies):
        super().__init__(groups)

        self.main_dir = os.path.split(os.path.abspath(__file__))[0]

        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(os.path.join(self.main_dir, '..', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)
        self.direction = pygame.Vector2()
        self.speed = 300

        self.collision_sprites = collision_sprites
        self.enemies = enemies

    def load_images(self):
        self.frames = {
            'left': [],
            'right': [],
            'up': [],
            'down': []
        }

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in os.walk(os.path.join(self.main_dir, '..', 'images', 'player', state)):
                for file_name in sorted(file_names, key=lambda x: int(x.split('.')[0])):
                    full_path = os.path.join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys and self.frame_index == 0:
            self.frame_index += 1

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

        self.rect.center = self.hitbox_rect.center

    def move(self, delta_time):
        self.hitbox_rect.centerx += self.direction.x * self.speed * delta_time
        Collision.collision('horizontal', self.direction, self.hitbox_rect, self.collision_sprites)
        self.hitbox_rect.centery += self.direction.y * self.speed * delta_time
        Collision.collision('vertical', self.direction, self.hitbox_rect, self.collision_sprites)

    def animate(self, delta_time):
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        self.frame_index = self.frame_index + 5 * delta_time if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, delta_time):
        self.input()
        self.move(delta_time)
        self.animate(delta_time)
