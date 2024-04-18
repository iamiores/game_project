import pygame
from pygame import *
pygame.init()

hatch_tut = []
hatch_lvl1 = []
hatch_lvl2 = []
hatch_lvl3 = []
collide_group_tut = sprite.Group()
collide_group_lvl1 = sprite.Group()
collide_group_lvl2 = sprite.Group()
collide_group_lvl3 = sprite.Group()
traps_group_tut = sprite.Group()
traps_group_lvl1 = sprite.Group()
traps_group_lvl2 = sprite.Group()
traps_group_lvl3 = sprite.Group()


class For_Level_Building(sprite.Sprite):
    def __init__(self, x, y, width, height, file_image):
        super().__init__()
        self.file = file_image
        self.image = transform.scale(pygame.image.load(self.file), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


portal_tut = For_Level_Building(200, 175, 50, 80, 'images/items/portal.png')
portal_lvl1 = For_Level_Building(150, 110, 50, 80, 'images/items/portal.png')
portal_lvl2 = For_Level_Building(550, 540, 50, 80, 'images/items/portal.png')
portal_lvl3 = For_Level_Building(470, 585, 40, 60, 'images/items/portal.png')


def walls_tut(screen):
    from levels import wall_tuts
    for keys, value in wall_tuts.items():
        w = For_Level_Building(*value)
        collide_group_tut.add(w)
        w.update(screen=screen)
        # pygame.draw.rect(window, (255, 0, 0), w.rect, 1)


def walls_level1(screen):
    from levels import wall_lvl1
    for keys, value in wall_lvl1.items():
        w = For_Level_Building(*value)
        collide_group_lvl1.add(w)
        w.update(screen=screen)
        # pygame.draw.rect(window, (255, 0, 0), w.rect, 1)


def walls_level2(screen):
    from levels import wall_lvl2
    for keys, value in wall_lvl2.items():
        w = For_Level_Building(*value)
        collide_group_lvl2.add(w)
        w.update(screen=screen)
        # pygame.draw.rect(window, (255, 0, 0), w.rect, 1)


def walls_level3(screen):
    from levels import wall_lvl3
    for keys, value in wall_lvl3.items():
        w = For_Level_Building(*value)
        collide_group_lvl3.add(w)
        w.update(screen=screen)
        # pygame.draw.rect(window, (255, 0, 0), w.rect, 1)


# FLOORS
def floor_tut(screen):
    from levels import floor_tuts
    for keys, value in floor_tuts.items():
        f = For_Level_Building(*value)
        f.update(screen=screen)
    pygame.draw.rect(screen, (43, 35, 52), (263, 525, 160, 60))
    pygame.draw.rect(screen, (43, 35, 52), (555, 323, 80, 140))


def floor_level1(screen):
    from levels import floor_lvl1
    for keys, value in floor_lvl1.items():
        f = For_Level_Building(*value)
        f.update(screen=screen)
    pygame.draw.rect(screen, (43, 35, 52), (596, 427, 161, 60))
    pygame.draw.rect(screen, (43, 35, 52), (835, 266, 70, 121))
    pygame.draw.rect(screen, (43, 35, 52), (512, 113, 141, 67))


def floor_level2(screen):
    from levels import floor_lvl2
    for keys, value in floor_lvl2.items():
        f = For_Level_Building(*value)
        f.update(screen=screen)
    pygame.draw.rect(screen, (43, 35, 52), (180, 372, 80, 144))
    pygame.draw.rect(screen, (43, 35, 52), (422, 212, 150, 60))
    pygame.draw.rect(screen, (43, 35, 52), (720, 370, 85, 123))


def floor_level3(screen):
    from levels import floor_lvl3
    for keys, value in floor_lvl3.items():
        f = For_Level_Building(*value)
        f.update(screen=screen)
    pygame.draw.rect(screen, (43, 35, 52), (455, 236, 82, 120))


# ITEMS
def items_tut(screen):
    from levels import item_tuts, trap_tuts
    for keys, values in item_tuts.items():
        i = For_Level_Building(*values)
        i.update(screen=screen)
        collide_group_tut.add(i)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, values in trap_tuts.items():
        t = For_Level_Building(*values)
        t.update(screen=screen)
        traps_group_tut.add(t)
        # pygame.draw.rect(window, (255, 0, 0), t.rect, 1)
    closed_hatch = For_Level_Building(574, 205, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(574, 205, 43, 35, 'images/items/open_hatch.png')
    hatch_tut.append(closed_hatch)
    hatch_tut.append(opened_hatch)


def items_level1(screen):
    from levels import item_lvl1, trap_lvl1
    for keys, values in item_lvl1.items():
        i = For_Level_Building(*values)
        i.update(screen=screen)
        collide_group_lvl1.add(i)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, values in trap_lvl1.items():
        t = For_Level_Building(*values)
        t.update(screen=screen)
        traps_group_lvl1.add(t)
        # pygame.draw.rect(window, (255, 0, 0), t.rect, 1)
    closed_hatch = For_Level_Building(370, 140, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(370, 140, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl1.append(closed_hatch)
    hatch_lvl1.append(opened_hatch)


def items_level2(screen):
    from levels import item_lvl2, trap_lvl2
    for keys, values in item_lvl2.items():
        i = For_Level_Building(*values)
        i.update(screen=screen)
        collide_group_lvl2.add(i)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, value in trap_lvl2.items():
        t = For_Level_Building(*value)
        t.update(screen=screen)
        traps_group_lvl2.add(t)
        # pygame.draw.rect(window, (255, 0, 0), t.rect, 1)
    closed_hatch = For_Level_Building(740, 575, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(740, 575, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl2.append(closed_hatch)
    hatch_lvl2.append(opened_hatch)


def items_level3(screen):
    from levels import item_lvl3, trap_lvl3
    for keys, value in item_lvl3.items():
        i = For_Level_Building(*value)
        collide_group_lvl3.add(i)
        i.update(screen=screen)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, value in trap_lvl3.items():
        t = For_Level_Building(*value)
        traps_group_lvl3.add(t)
        t.update(screen=screen)
        # pygame.draw.rect(window, (255, 0, 0), t.rect, 1)
    closed_hatch = For_Level_Building(472, 470, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(472, 470, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl3.append(closed_hatch)
    hatch_lvl3.append(opened_hatch)
