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


class Item(sprite.Sprite):
    def __init__(self, item_x, item_y, item_width, item_height, file_image):
        super().__init__()
        self.file = file_image
        self.image = transform.scale(image.load(self.file), (item_width, item_height))
        self.rect = self.image.get_rect()
        self.rect.x = item_x
        self.rect.y = item_y

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


# WALLS

walls_tut_group = sprite.Group()


def walls_tut():
    from levels import wall_tuts
    for key, value in wall_tuts.items():
        w = Wall(*value)
        walls_tut_group.add(w)
        w.update()


# FLOORS

def floor_tut():
    from levels import floor_tuts
    for key, value in floor_tuts.items():
        f = Floor(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (263, 525, 160, 60))
    pygame.draw.rect(window, (43, 35, 52), (555, 323, 80, 140))


# ITEMS
def items_tut():
    from levels import item_tuts
    for key, values in item_tuts.items():
        i = Item(*values)
        i.update()


# LEVELS

def tutorial():

    window.fill((0, 0, 0))
    window.blit(text, (10, 10))

    floor_tut()
    walls_tut()
    items_tut()
    pygame.display.update()
    clock.tick(fps)


# def first_lvl():
#     window.fill((0, 0, 0))
#     window.blit(text, (10, 10))
#
#     floor_tut()
#     walls_tut_2()
#     pygame.display.update()
#     clock.tick(fps)


while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    text = font1.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))

    tutorial()

    # collision on end level
    # LEVEL_NUMBER = 0

    # LEVEL_NAMES = [
    # tutorial(),
    # first_lvl(),
    # second_lvl()
    # ]

    # if pygame.event == 'endlevel':
    #    show two buttons: next_level and back
    #    if next_level == 'pressed':
    #        LEVEL_NUMBER += 1
    #        loadnew level with
    #           LEVEL_NAMES[LEVEL_NUMBER]
    #    if back == 'pressed':
    #        LEVEL_NUMBER = 0
    #         return to menu
    #


