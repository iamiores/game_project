import pygame
from pygame import *

pygame.init()

class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < W - 85:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < H - 85:
            self.rect.y += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color_r, color_g, color_b, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_r, color_g, color_b))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        draw.rect(window, (self.color_r, self.color_g, self.color_b), (self.rect.x, self.rect.y, self.width, self.height))


W, H = 800, 600

window = pygame.display.set_mode((W, H))
display.set_caption("roguelike")

background_image = pygame.image.load('images/walls/bg.jpg')
background_rect = background_image.get_rect()

font = pygame.font.Font(None, 20)

background_x = 0
background_y = 0

speed = 7
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if keys[pygame.K_LEFT]:
        background_x += speed
    if keys[pygame.K_RIGHT]:
        background_x -= speed
    if keys[pygame.K_UP]:
        background_y += speed
    if keys[pygame.K_DOWN]:
        background_y -= speed

    text = font.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))

    window.fill((0, 0, 0))

    window.blit(background_image, (background_x, background_y))
    window.blit(text, (10, 10))
    pygame.display.update()
    clock.tick(30)
