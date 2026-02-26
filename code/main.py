from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
import os


class Game:
    def __init__(self):
        pygame.init()
        self.displayScreen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.main_dir = os.path.split(os.path.abspath(__file__))[0]

        pygame.display.set_caption("Vampire Survivor")

        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        self.player = Player((500, 300), self.all_sprites, self.collision_sprites)

    def setup(self):
        game_map = load_pygame(os.path.join(self.main_dir, '..', 'data', 'maps', 'world.tmx'))

        for x, y, image in game_map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in game_map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for collision in game_map.get_layer_by_name("Collisions"):
            CollisionSprite((collision.x, collision.y), pygame.Surface((collision.width, collision.height)), self.collision_sprites)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(delta_time)

            self.displayScreen.fill('black')

            self.all_sprites.draw(self.displayScreen)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
