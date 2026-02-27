from settings import *
from math import atan2, degrees


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.is_ground = True


class Bullet(pygame.sprite.Sprite):
    def __init__(self, gun, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.gun_direction = gun.player_direction
        self.rect = self.image.get_rect(center=gun.rect.center + self.gun_direction * 50)
        self.bullet_speed = 1200

        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000

    def update(self, delta_time):
        self.rect.center += self.gun_direction * delta_time * self.bullet_speed

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()


class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        self.main_dir = os.path.split(os.path.abspath(__file__))[0]

        super().__init__(groups)

        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(1, 0)

        self.gun_surf = pygame.image.load(os.path.join(self.main_dir, '..', 'images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center=self.player.rect.center + self.player_direction * self.distance)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

        self.player_direction = pygame.Vector2(mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90

        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, -angle, 1)
            self.image = pygame.transform.flip(self.image, False, True)


