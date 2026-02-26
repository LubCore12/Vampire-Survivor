from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        self.main_dir = os.path.split(os.path.abspath(__file__))[0]

        self.image = pygame.image.load(os.path.join(self.main_dir, '..', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, -50)
        self.direction = pygame.Vector2()
        self.speed = 300

        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

        self.rect.center = self.hitbox_rect.center

    def move(self, delta_time):
        self.hitbox_rect.centerx += self.direction.x * self.speed * delta_time
        self.collision('horizontal')
        self.hitbox_rect.centery += self.direction.y * self.speed * delta_time
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom


    def update(self, delta_time):
        self.input()
        self.move(delta_time)

