from settings import *
from player import Player
from sprites import *

from random import randint


class Game:
    def __init__(self):
        pygame.init()
        self.displayScreen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.display.set_caption("Vampire Survivor")

        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.player = Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), self.all_sprites, self.collision_sprites)

        for i in range(6):
            pos = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            size = randint(60, 100), randint(60, 100)

            CollisionSprite(pos, size, (self.all_sprites, self.collision_sprites))

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

