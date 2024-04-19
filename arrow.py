import pygame
import math
from pygame import *
pygame.init()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, shooter, targets_group):
        super().__init__()
        self.original_image = pygame.transform.scale(pygame.image.load('store_items/narrow.png'), (12, 12))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = shooter.rect.center  # Початкова позиція стріли - центр стрільця
        self.targets_group = targets_group
        self.target = None
        self.speed = 5  # Швидкість руху стріли

    def find_nearest_target(self):
        min_distance = float('inf')
        nearest_target = None
        for target in self.targets_group:
            distance = math.hypot(self.rect.centerx - target.rect.centerx, self.rect.centery - target.rect.centery)
            if distance < min_distance:
                min_distance = distance
                nearest_target = target
        return nearest_target

    def update(self, attack):
        if not self.target or not pygame.sprite.spritecollide(self, self.targets_group, False):
            self.target = self.find_nearest_target()
        if self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx /= distance
                dy /= distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            angle = math.degrees(math.atan2(-dy, dx))  # Обчислюємо кут повороту
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)  # Оновлюємо положення стріли після повороту
            if self.rect.colliderect(self.target.rect):
                self.target.health -= attack
                self.kill()
