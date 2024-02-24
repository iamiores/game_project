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
    # spawn
    w1 = Wall(50, 650, 200, 12, 'images/walls/back_wall.jpg')
    w1.update()
    w2 = Wall(35, 442, 15, 220, 'images/walls/left_wall.jpg')
    w2.update()
    w3 = Wall(50, 442, 200, 55, 'images/walls/front_wall.jpg')
    w3.update()
    w4 = Wall(250, 442, 15, 85, 'images/walls/half1-right_wall.jpg')
    w4.update()
    w5 = Wall(250, 578, 15, 85, 'images/walls/half2-right_wall.jpg')
    w5.update()
    # corridor 1
    w6 = Wall(264, 482,  160, 45, 'images/walls/front_wall.jpg')
    w6.update()
    w7 = Wall(264, 578, 160, 12, 'images/walls/back_wall.jpg')
    w7.update()
    # corridor 2
    w14 = Wall(540, 321, 15, 100, 'images/walls/half1-left_wall.jpg')
    w14.update()
    w15 = Wall(635, 321, 15, 100, 'images/walls/half1-right_wall.jpg')
    w15.update()
    # battle
    w8 = Wall(420, 418, 15, 110, 'images/walls/half1-left_wall.jpg')
    w8.update()
    w9 = Wall(420, 577, 15, 110, 'images/walls/half2-left_wall.jpg')
    w9.update()
    w10 = Wall(435, 419, 120, 55, 'images/walls/left-front_wall.jpg')
    w10.update()
    w11 = Wall(635, 419, 120, 55, 'images/walls/right-front_wall.jpg')
    w11.update()
    w12 = Wall(755, 419, 15, 267, 'images/walls/right_wall.jpg')
    w12.update()
    w13 = Wall(435, 674, 320, 12, 'images/walls/back_wall.jpg')
    w13.update()
    #



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