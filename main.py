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
    def __init__(self, floor_x, floor_y, image_name):
        super().__init__()
        self.file_name = image_name
        self.image = transform.scale(image.load(self.file_name), (65, 65))
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
    wall1_x = 50
    for i in range(0, 2):
        w1 = Wall(wall1_x, 450, 150, 10,'back_wall.jpg')
        wall1_x += 50
        w1.update()
    wall2_y = 260
    for i in range(1):
        w2 = Wall(35, wall2_y, 15, 200, 'left_wall.jpg')
        wall2_y += 50
        w2.update()
    for i in range()


def tutorial():
    global game
    while game:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        text = font1.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))

        window.fill((0, 0, 0))
        window.blit(text, (10, 10))

        walls_tut()

        pygame.display.update()
        clock.tick(fps)


tutorial()