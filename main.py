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
hatch_num_tut = 0
hatch_num_lvl1 = 0
hatch_num_lvl2 = 0

# GROUPS, LISTS ETC
hatch_tut = []
hatch_lvl1 = []
hatch_lvl2 = []
collide_group = sprite.Group()
traps_group = sprite.Group()


# WALLS
def walls_tut():
    from levels import wall_tuts
    for key, value in wall_tuts.items():
        w = Wall(*value)
        collide_group.add(w)
        w.update()


def walls_level1():
    from levels import wall_lvl1
    for key, value in wall_lvl1.items():
        w = Wall(*value)
        collide_group.add(w)
        w.update()


def walls_level2():
    from levels import wall_lvl2
    for key, value in wall_lvl2.items():
        w = Wall(*value)
        collide_group.add(w)
        w.update()


# FLOORS
def floor_tut():
    from levels import floor_tuts
    for key, value in floor_tuts.items():
        f = Floor(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (263, 525, 160, 60))
    pygame.draw.rect(window, (43, 35, 52), (555, 323, 80, 140))


def floor_level1():
    from levels import floor_lvl1
    for key, value in floor_lvl1.items():
        f = Floor(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (596, 427, 161, 60))
    pygame.draw.rect(window, (43, 35, 52), (835, 266, 70, 121))
    pygame.draw.rect(window, (43, 35, 52), (512, 113, 141, 67))


def floor_level2():
    from levels import floor_lvl2
    for key, value in floor_lvl2.items():
        f = Floor(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (180, 372, 80, 144))
    pygame.draw.rect(window, (43, 35, 52), (422, 212, 150, 60))
    pygame.draw.rect(window, (43, 35, 52), (720, 370, 85, 123))


# ITEMS
def items_tut():
    from levels import item_tuts, trap_tuts
    for key, values in item_tuts.items():
        i = Item(*values)
        i.update()
        collide_group.add(i)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for key, values in trap_tuts.items():
        t = Item(*values)
        t.update()
        traps_group.add(t)
        # pygame.draw.rect(window, (255, 0, 0), s.rect, 1)
    closed_hatch = Item(574, 205, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = Item(574, 205, 43, 35, 'images/items/open_hatch.png')
    hatch_tut.append(closed_hatch)
    hatch_tut.append(opened_hatch)
    portal = Item(140, 175, 50, 80, 'images/items/portal.png')
    window.blit(portal.image, (portal.rect.x, portal.rect.y))


def items_level1():
    from levels import item_lvl1, trap_lvl1
    for key, values in item_lvl1.items():
        i = Item(*values)
        i.update()
        collide_group.add(i)
    for key, values in trap_lvl1.items():
        t = Item(*values)
        t.update()
        traps_group.add(t)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    closed_hatch = Item(370, 140, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = Item(370, 140, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl1.append(closed_hatch)
    hatch_lvl1.append(opened_hatch)
    portal = Item(170, 110, 50, 80, 'images/items/portal.png')
    window.blit(portal.image, (portal.rect.x, portal.rect.y))


def items_level2():
    from levels import item_lvl2, trap_lvl2
    for key, values in item_lvl2.items():
        i = Item(*values)
        i.update()
        collide_group.add(i)
    for key, value in trap_lvl2.items():
        t = Item(*value)
        t.update()
        traps_group.add(t)
    closed_hatch = Item(740, 575, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = Item(740, 575, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl2.append(closed_hatch)
    hatch_lvl2.append(opened_hatch)
    portal = Item(550, 540, 50, 80, 'images/items/portal.png')
    window.blit(portal.image, (portal.rect.x, portal.rect.y))


# LEVELS
def tutorial():
    window.fill((0, 0, 0))
    window.blit(text, (10, 10))

    floor_tut()
    walls_tut()
    items_tut()
    window.blit(hatch_tut[hatch_num_tut].image, (hatch_tut[hatch_num_tut].rect.x, hatch_tut[hatch_num_tut].rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_1():
    window.fill((0, 0, 0))
    window.blit(text, (10, 0))

    floor_level1()
    walls_level1()
    items_level1()
    window.blit(hatch_lvl1[hatch_num_lvl1].image, (hatch_lvl1[hatch_num_lvl1].rect.x, hatch_lvl1[hatch_num_lvl1].rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_2():
    window.fill((0, 0, 0))
    window.blit(text, (10, 0))

    floor_level2()
    walls_level2()
    items_level2()
    window.blit(hatch_lvl2[hatch_num_lvl2].image, (hatch_lvl2[hatch_num_lvl2].rect.x, hatch_lvl2[hatch_num_lvl2].rect.y))
    pygame.display.update()
    clock.tick(fps)


# MAIN CYCLE
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    text = font1.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))

    # tutorial()
    # level_1()
    level_2()

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


