import pygame

from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
import os
from groups import AllSprites
from random import choice


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
        self.enemy_sprites = pygame.sprite.Group()

        self.load_images()
        self.game_map = load_pygame(os.path.join(self.main_dir, '..', 'data', 'maps', 'world.tmx'))

        self.setup()

        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        self.enemy_names = ['bat', 'blob', 'skeleton']
        self.enemy_event = pygame.event.custom_type()
        self.enemy_list = list(filter(lambda x: x.name == 'Enemy', self.game_map.get_layer_by_name("Entities")))
        self.enemy_spawn_time = 500

        pygame.time.set_timer(self.enemy_event, self.enemy_spawn_time)

        self.shoot_sound = pygame.mixer.Sound(os.path.join(self.main_dir, '..', 'audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        self.impact_sound = pygame.mixer.Sound(os.path.join(self.main_dir, '..', 'audio', 'impact.ogg'))
        self.impact_sound.set_volume(0.2)
        self.music = pygame.mixer.Sound(os.path.join(self.main_dir, '..', 'audio', 'music.wav'))
        self.music.set_volume(0.05)
        self.music.play(loops=-1)


    def load_images(self):
        self.bullet_surf = pygame.image.load(os.path.join(self.main_dir, '..', 'images', 'gun', 'bullet.png')).convert_alpha()

        self.enemy_frames = {
            'bat': [],
            'blob': [],
            'skeleton': []
        }

        for enemy in self.enemy_frames:
            for _, _, file_names in os.walk(os.path.join(self.main_dir, '..', 'images', 'enemies', enemy)):
                for file_name in sorted(file_names, key=lambda x: int(x.split('.')[0])):
                    surf = pygame.image.load(
                        os.path.join(self.main_dir, '..', 'images', 'enemies', enemy, file_name)).convert_alpha()
                    self.enemy_frames[enemy].append(surf)

    def input(self):
        mouse_keys = pygame.mouse.get_just_pressed()

        if mouse_keys[0] and self.can_shoot:
            Bullet(self.gun, self.bullet_surf, (self.all_sprites, self.bullet_sprites), self.enemy_sprites)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.shoot_sound.play()

    def gun_timer(self):
        if not self.can_shoot:
            curent_time = pygame.time.get_ticks()

            if curent_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        for x, y, image in self.game_map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in self.game_map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for collision in self.game_map.get_layer_by_name("Collisions"):
            CollisionSprite((collision.x, collision.y), pygame.Surface((collision.width, collision.height)), self.collision_sprites)

        for entity in self.game_map.get_layer_by_name("Entities"):
            if entity.name == "Player":
                self.player = Player((entity.x, entity.y), self.all_sprites, self.collision_sprites, self.enemy_sprites)
                self.gun = Gun(self.player, self.all_sprites)

    def kill_enemies(self):
        for bullet in self.bullet_sprites:
            collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, dokill=False, collided=collide_mask)

            if collision_sprites:
                for sprite in collision_sprites:
                    sprite.destroy()
                bullet.kill()
                self.impact_sound.play()

    def kill_player(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, dokill=False, collided=collide_mask):
            self.running = False

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    enemy = choice(self.enemy_list)

                    pygame.time.set_timer(self.enemy_event, int(self.enemy_spawn_time))

                    while (pygame.Vector2((enemy.x, enemy.y)) - pygame.Vector2(self.player.rect.center)).magnitude() < 1000:
                        enemy = choice(self.enemy_list)

                    enemy_type = self.enemy_frames[choice(self.enemy_names)]
                    Enemy((enemy.x, enemy.y), enemy_type, self.player, (self.all_sprites, self.enemy_sprites), self.enemy_sprites, self.collision_sprites)

            self.gun_timer()
            self.input()
            self.kill_player()
            self.kill_enemies()

            if self.enemy_spawn_time > 200:
                self.enemy_spawn_time -= 1 * delta_time