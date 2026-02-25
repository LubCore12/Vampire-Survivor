from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../images/player/down/0.png').convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.direction = pygame.Vector2()
        self.speed = 1000

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time

    def update(self, delta_time):
        self.input()
        self.move(delta_time)

