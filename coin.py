import os
import pygame
from pygame import sprite


class Coin(sprite.Sprite):
    @staticmethod
    def get_image_paths():
        # Получить текущий каталог
        current_directory = os.path.join(os.path.dirname(__file__), "images")

        # Список имен файлов, которые вы хотите загрузить (замените на ваши имена файлов)
        selected_files = ["coin_1.png", "coin_2.png", "coin_3.png", "coin_4.png", "coin_5.png", "coin_6.png",
                          "coin_7.png",
                          "coin_8.png"]

        # Создайте список путей к выбранным файлам
        image_paths = [os.path.join(current_directory, f) for f in selected_files if
                       os.path.isfile(os.path.join(current_directory, f))]
        return image_paths

    def __init__(self, x, y, width, height):
        super().__init__()
        self.images = [pygame.image.load(path) for path in self.get_image_paths()]  # Список анимационных кадров
        self.current_index = 0  # Индекс текущего кадра
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.images[self.current_index],(self.width, self.height))  # Текущий кадр изображения
        self.rect = self.image.get_rect(center=(x, y))  # Расположение монеты на экране
        self.animation_speed = 0.2 # Скорость анимации (в секундах)
        self.last_update = pygame.time.get_ticks()  # Время последнего обновления кадра

    def update(self):
        # Обновление анимации монеты
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 1000:  # Преобразуем скорость в миллисекунды
            self.current_index = (self.current_index + 1) % len(self.images)  # Переход к следующему кадру
            self.image = pygame.transform.scale(self.images[self.current_index],
                                                (self.width, self.height))  # Обновление изображения
            self.last_update = current_time  # Обновляем время последнего кадра

    def draw(self, screen):
        # Отображение монеты на экране
        screen.blit(self.image, self.rect)

