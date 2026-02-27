from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
import os
from groups import AllSprites


class Game:
    def __init__(self):
        pygame.init()
        self.displayScreen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        pygame.display.set_caption("Vampire Survivor")

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.load_images()

        self.setup()

        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

    def load_images(self):
        self.bullet_surf = pygame.image.load(os.path.join(self.main_dir, '..', 'images', 'gun', 'bullet.png')).convert_alpha()

    def input(self):
        mouse_keys = pygame.mouse.get_just_pressed()

        if mouse_keys[0] and self.can_shoot:
            Bullet(self.gun, self.bullet_surf, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            curent_time = pygame.time.get_ticks()

            if curent_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        game_map = load_pygame(os.path.join(self.main_dir, '..', 'data', 'maps', 'world.tmx'))

        for x, y, image in game_map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in game_map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for collision in game_map.get_layer_by_name("Collisions"):
            CollisionSprite((collision.x, collision.y), pygame.Surface((collision.width, collision.height)), self.collision_sprites)

        for entity in game_map.get_layer_by_name("Entities"):
            if entity.name == "Player":
                self.player = Player((entity.x, entity.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.gun_timer()
            self.input()
            self.all_sprites.update(delta_time)

            self.displayScreen.fill('black')

            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
