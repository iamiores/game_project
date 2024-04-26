import os
import pygame
from pygame import sprite


class Coin(sprite.Sprite):
    @staticmethod
    def get_image_paths():
        # Отримати поточний каталог
        current_directory = os.path.join(os.path.dirname(__file__), "images")

        # Список імен файлів, які ви хочете завантажити (замініть на ваші імена файлів)
        selected_files = ["coin_1.png", "coin_2.png", "coin_3.png", "coin_4.png", "coin_5.png", "coin_6.png",
                          "coin_7.png",
                          "coin_8.png"]

        # Створіть список шляхів до вибраних файлів
        image_paths = [os.path.join(current_directory, f) for f in selected_files if
                       os.path.isfile(os.path.join(current_directory, f))]
        return image_paths

    def __init__(self, x, y, width, height):
        super().__init__()
        self.images = [pygame.image.load(path) for path in self.get_image_paths()]   # Список анімаційних кадрів
        self.current_index = 0  # Індекс поточного кадру
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.images[self.current_index],(self.width, self.height)) # Поточний кадр зображення
        self.rect = self.image.get_rect(center=(x, y))   # Розташування монети на екрані
        self.animation_speed = 0.2 # Швидкість анімації (у секундах)
        self.last_update = pygame.time.get_ticks() # Час останнього оновлення кадру

    def update(self):
        # Оновлення анімації монети
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 1000:  # Перетворимо швидкість у мілісекунди
            self.current_index = (self.current_index + 1) % len(self.images) # Перехід до наступного кадру
            self.image = pygame.transform.scale(self.images[self.current_index],
                                                (self.width, self.height))  # Оновлення зображення
            self.last_update = current_time  # Оновлюємо час останнього кадру

    def draw(self, screen):
        # Відображення монети на екрані
        screen.blit(self.image, self.rect)

