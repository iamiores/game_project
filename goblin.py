import pygame
from pygame import *
pygame.init()
import math


class Goblin(sprite.Sprite):
    def __init__(self, goblin_image, goblin_x, goblin_y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(pygame.image.load(goblin_image), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = goblin_x
        self.rect.y = goblin_y
        self.rect.width = width
        self.rect.height = height
        self.speed = 5
        self.counter_idle = 0
        self.counter_right = 0
        self.counter_left = 0
        self.counter_attack_right = 0
        self.counter_attack_left = 0
        self.direction = 'right'
        self.health = 100

        self.pics_idle = ['images/monsters/goblin/goblin_idle_right_1.png', 'images/monsters/goblin/goblin_idle_right_2.png', 'images/monsters/goblin/goblin_idle_right_3.png', 'images/monsters/goblin/goblin_idle_right_4.png']
        self.pics_idle_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_idle]

        self.pics_attack_right = ['images/monsters/goblin/goblin_attack_right_1.png', 'images/monsters/goblin/goblin_attack_right_2.png', 'images/monsters/goblin/goblin_attack_right_3.png', 'images/monsters/goblin/goblin_attack_right_4.png']
        self.pics_attack_right_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_attack_right]

        self.pics_attack_left = ['images/monsters/goblin/goblin_attack_left_1.png', 'images/monsters/goblin/goblin_attack_left_2.png', 'images/monsters/goblin/goblin_attack_left_3.png', 'images/monsters/goblin/goblin_attack_left_4.png']
        self.pics_attack_left_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_attack_left]

        self.pics_right = ['images/monsters/goblin/goblin_walk_right_1.png', 'images/monsters/goblin/goblin_walk_right_2.png', 'images/monsters/goblin/goblin_walk_right_3.png']
        self.pics_right_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_right]

        self.pics_left = ['images/monsters/goblin/goblin_walk_left_1.png', 'images/monsters/goblin/goblin_walk_left_2.png', 'images/monsters/goblin/goblin_walk_left_3.png']
        self.pics_left_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_left]

    def animate(self, kind, target_lives):
        self.target_lives = target_lives
        # print(kind)
        print(target_lives)
        if kind == 'stay':
            self.counter_idle += 1
            if self.counter_idle < 5:
                self.image = self.pics_idle_obj[0]
            elif 5 <= self.counter_idle < 10:
                self.image = self.pics_idle_obj[1]
            elif 10 <= self.counter_idle < 15:
                self.image = self.pics_idle_obj[2]
            elif 15 <= self.counter_idle < 20:
                self.image = self.pics_idle_obj[3]

            elif self.counter_idle == 20:
                self.counter_idle = 0
        else:
            self.counter_idle = 0

        if kind == 'attack right':
            self.counter_attack_right += 1
            if self.counter_attack_right < 5:
                self.image = self.pics_attack_right_obj[0]
            elif 5 <= self.counter_attack_right < 10:
                self.image = self.pics_attack_right_obj[1]
            elif 10 <= self.counter_attack_right < 15:
                self.image = self.pics_attack_right_obj[2]
            elif 15 <= self.counter_attack_right < 20:
                self.image = self.pics_attack_right_obj[3]

            elif self.counter_attack_right == 20:
                self.target_lives -= 1
                self.counter_attack_right = 0
        else:
            self.counter_attack_right = 0

        if kind == 'attack left':
            self.counter_attack_left += 1
            if self.counter_attack_left < 5:
                self.image = self.pics_attack_left_obj[0]
            elif 5 <= self.counter_attack_left < 10:
                self.image = self.pics_attack_left_obj[1]
            elif 10 <= self.counter_attack_left < 15:
                self.image = self.pics_attack_left_obj[2]
            elif 15 <= self.counter_attack_left < 20:
                self.image = self.pics_attack_left_obj[3]

            elif self.counter_attack_left == 20:
                self.target_lives -= 1
                self.counter_attack_left = 0
        else:
            self.counter_attack_left = 0

        if kind == 'right':
            self.direction = 'right'
            self.counter_right += 1
            if self.counter_right < 5:
                self.image = self.pics_right_obj[0]
            elif 5 <= self.counter_right < 10:
                self.image = self.pics_right_obj[1]
            elif 10 <= self.counter_right < 15:
                self.image = self.pics_right_obj[2]

            elif self.counter_right == 15:
                self.counter_right = 0
        else:
            self.counter_right = 0

        if kind == 'left':
            self.direction = 'left'
            self.counter_left += 1
            if self.counter_left < 5:
                self.image = self.pics_left_obj[0]
            elif 5 <= self.counter_left < 10:
                self.image = self.pics_left_obj[1]
            elif 10 <= self.counter_left < 15:
                self.image = self.pics_left_obj[2]

            elif self.counter_left == 15:
                self.counter_left = 0
        else:
            self.counter_left = 0

        if kind == 'attack right' or kind == 'attack left':
            self.speed = 2
        else:
            self.speed = 5

    def collide(self, group):
        for group in group:
            if self.rect.colliderect(group.rect):
                if self.rect.top < group.rect.bottom < self.rect.bottom:
                    self.rect.y += 1
                elif self.rect.bottom > group.rect.top > self.rect.top:
                    self.rect.y -= 1
                elif self.rect.left < group.rect.right < self.rect.right:
                    self.rect.x += 1
                elif self.rect.right > group.rect.left > self.rect.left:
                    self.rect.x -= 1

    def update(self, player, player_lives, target_y=None, target_x=None, x=None, y=None):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist

        target_x = target_x if target_x is not None else float('-inf')
        target_y = target_y if target_y is not None else float('-inf')
        x = x if x is not None else float('inf')
        y = y if y is not None else float('inf')
        if dx > 0:
            self.direction = 'right'
        if target_x >= x or target_y >= y:
            if self.direction == 'right':
                if self.rect.colliderect(player.rect):
                    self.animate('attack right', player_lives)
                else:
                    self.animate('right', player_lives)
                self.rect.x += dx * self.speed
                if dy > 0:
                    self.animate('right', player_lives)
                    self.rect.y += dy * self.speed
                elif dy < 0:
                    self.animate('right', player_lives)
                    self.rect.y += dy * self.speed

            if dx < 0:
                self.direction = 'left'

            if self.direction == 'left':
                if self.rect.colliderect(player.rect):
                    self.animate('attack left', player_lives)
                else:
                    self.animate('left', player_lives)
                self.rect.x += dx * self.speed
                if dy > 0:
                    self.animate('left', player_lives)
                    self.rect.y += dy * self.speed
                elif dy < 0:
                    self.animate('left', player_lives)
                    self.rect.y += dy * self.speed
        else:
            self.animate('stay', player_lives)

    def show(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))