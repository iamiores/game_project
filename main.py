import pygame
from pygame import *

pygame.init()

class MainSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Wall(sprite.Sprite):
    def __init__(self, wall_x, wall_y, wall_width, wall_height, file_image):
        super().__init__()
        self.file = file_image
        self.image = transform.scale(image.load(self.file), (wall_width, wall_height))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Floor(sprite.Sprite):
    def __init__(self, floor_x, floor_y, floor_width, floor_height, image_name):
        super().__init__()
        self.file_name = image_name
        self.image = transform.scale(image.load(self.file_name), (floor_width, floor_height))
        self.rect = self.image.get_rect()
        self.rect.x = floor_x
        self.rect.y = floor_y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# FONTS
font1 = pygame.font.Font(None, 20)

# SETTINGS
w_width, w_height = 1000, 700
window = pygame.display.set_mode((w_width, w_height))
clock = pygame.time.Clock()
fps = 60
game = True

# FUNCTIONS

def walls_tut():
    # spawn
    from levels import LEVEL_1

    for key, value in LEVEL_1.items():
        w = Wall(*value)
        w.update()

    w16_x = 50
    for i in range(3):
        w16 = Wall(w16_x, 311, 200, 12, 'images/walls/back_wall.jpg')
        w16.update()
        w16_x += 153
    w19 = Wall(635, 311, 225, 12, 'images/walls/back_wall.jpg')
    w19.update()
    w17 = Wall(50, 75, 15, 247, 'images/walls/left_wall.jpg')
    w17.update()
    w18_x = 65
    for i in range(4):
        w18 = Wall(w18_x, 75, 200, 55, 'images/walls/front_wall.jpg')
        w18.update()
        w18_x += 198
    w20 = Wall(859, 75, 15, 248, 'images/walls/right_wall.jpg')
    w20.update()

def floor_tut():
    f1_x = 50
    for i in range(2):
        f1 = Floor(f1_x, 495, 110, 76, 'images/floor/floor.jpg')
        f1.update()
        f1_x += 89
    f2_x = 50
    for i in range(2):
        f2 = Floor(f2_x, 572, 110, 78, 'images/floor/floor.jpg')
        f2.update()
        f2_x += 89

def tutorial():
    window.fill((0, 0, 0))  # Очищаем экран

    floor_tut()  # Отрисовываем пол
    walls_tut()  # Отрисовываем стены

    # Отрисовка всех спрайтов
    all_sprites.draw(window)

    # Отображаем содержимое на экране
    pygame.display.flip()

    # Ограничиваем частоту кадров
    clock.tick(fps)

def first_lvl():
    window.fill((0, 0, 0))
    window.blit(text, (10, 10))

    floor_tut()
    pygame.display.update()
    clock.tick(fps)

from coin import Coin

# Создание объекта монеты
coin = Coin(x=250, y=210, width=40, height=40)

# Добавление монеты в список спрайтов
all_sprites = sprite.Group()
all_sprites.add(coin)

while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False

    clock.tick(fps)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    text = font1.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))

    tutorial()

    all_sprites.update()  # Обновление всех спрайтов

pygame.quit()
