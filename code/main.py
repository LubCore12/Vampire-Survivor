from settings import *
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.displayScreen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()

        self.player = Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), self.all_sprites)

        pygame.display.set_caption("Vampire Survivor")

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

