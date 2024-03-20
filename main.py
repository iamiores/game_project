import sys

import pygame
from pygame import *
pygame.init()


class MainSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(pygame.image.load(player_image), (65, 65))
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
        self.image = transform.scale(pygame.image.load(self.file), (wall_width, wall_height))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Floor(sprite.Sprite):
    def __init__(self, floor_x, floor_y, floor_width, floor_height, image_name):
        super().__init__()
        self.file_name = image_name
        self.image = transform.scale(pygame.image.load(self.file_name), (floor_width, floor_height))
        self.rect = self.image.get_rect()
        self.rect.x = floor_x
        self.rect.y = floor_y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Item(sprite.Sprite):
    def __init__(self, item_x, item_y, item_width, item_height, file_image):
        super().__init__()
        self.file = file_image
        self.image = transform.scale(pygame.image.load(self.file), (item_width, item_height))
        self.rect = self.image.get_rect()
        self.rect.x = item_x
        self.rect.y = item_y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Button:
    def __init__(self, button_x, button_y, button_width, button_height, button_image):
        self.file = button_image
        self.image = transform.scale(pygame.image.load(self.file), (button_width, button_height))
        self.rect = self.image.get_rect()
        self.rect.x = button_x
        self.rect.y = button_y
        self.clicked = False
        self.click_time = 0

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def button_click(self):
        mouse_controller = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_controller):
            if click[0] and not self.clicked:
                self.clicked = True
                self.click_time = pygame.time.get_ticks()
                if pygame.time.get_ticks() - self.click_time <= 500:
                    return True
                self.click_time = 0
        else:
            self.clicked = False
        return False


# FONTS
font1 = pygame.font.Font(None, 20)

# SETTINGS
w_width, w_height = 1000, 700
window = pygame.display.set_mode((w_width, w_height))
clock = pygame.time.Clock()
fps = 60
game = True

# ALTERNATES
hatch_num_tut = 0
hatch_num_lvl1 = 0
hatch_num_lvl2 = 0

lives = 5
energy = 5

button_show_state = 'main menu'
image = pygame.image.load('images/possible_background.png')
image = pygame.transform.scale(image, (w_width, w_height))


# GROUPS, LISTS ETC
hatch_tut = []
hatch_lvl1 = []
hatch_lvl2 = []
collide_group = sprite.Group()
traps_group = sprite.Group()


# WALLS
def walls_tut():
    from levels import wall_tuts
    for keys, value in wall_tuts.items():
        w = Wall(*value)
        collide_group.add(w)
        w.update()


def walls_level1():
    from levels import wall_lvl1
    for keys, value in wall_lvl1.items():
        w = Wall(*value)
        collide_group.add(w)
        w.update()


def walls_level2():
    from levels import wall_lvl2
    for keys, value in wall_lvl2.items():
        w = Wall(*value)
        collide_group.add(w)
        w.update()


def walls_level3():
    from levels import wall_lvl3
    for keys, value in wall_lvl3.items():
        w = Wall(*value)
        collide_group.add(w)
        w.update()


# FLOORS
def floor_tut():
    from levels import floor_tuts
    for keys, value in floor_tuts.items():
        f = Floor(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (263, 525, 160, 60))
    pygame.draw.rect(window, (43, 35, 52), (555, 323, 80, 140))


def floor_level1():
    from levels import floor_lvl1
    for keys, value in floor_lvl1.items():
        f = Floor(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (596, 427, 161, 60))
    pygame.draw.rect(window, (43, 35, 52), (835, 266, 70, 121))
    pygame.draw.rect(window, (43, 35, 52), (512, 113, 141, 67))


def floor_level2():
    from levels import floor_lvl2
    for keys, value in floor_lvl2.items():
        f = Floor(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (180, 372, 80, 144))
    pygame.draw.rect(window, (43, 35, 52), (422, 212, 150, 60))
    pygame.draw.rect(window, (43, 35, 52), (720, 370, 85, 123))


def floor_level3():
    from levels import floor_lvl3
    for keys, value in floor_lvl3.items():
        f = Floor(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (455, 236, 82, 120))


# ITEMS
def items_tut():
    from levels import item_tuts, trap_tuts
    for keys, values in item_tuts.items():
        i = Item(*values)
        i.update()
        collide_group.add(i)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, values in trap_tuts.items():
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
    for keys, values in item_lvl1.items():
        i = Item(*values)
        i.update()
        collide_group.add(i)
    for keys, values in trap_lvl1.items():
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
    for keys, values in item_lvl2.items():
        i = Item(*values)
        i.update()
        collide_group.add(i)
    for keys, value in trap_lvl2.items():
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
def menu():
    global button_show_state
    start_button = Button(435, 240, 120, 50, 'images/buttons/start.png')
    settings_button = Button(435, 300, 120, 50, 'images/buttons/settings.png')
    exit_button = Button(435, 360, 120, 50, 'images/buttons/exit.png')
    store_button = Button(450, 240, 60, 50, 'images/buttons/store.png')
    add_volume_button = Button(400, 300, 60, 50, 'images/buttons/more_volume.png')
    reduce_volume_button = Button(500, 300, 60, 50, 'images/buttons/less_volume.png')
    pause_button = None
    back_to_menu_button = None
    window.blit(image, (0, 0))
    if button_show_state == 'main menu':
        start_button.draw()
        settings_button.draw()
        exit_button.draw()
        pygame.draw.rect(window, (255, 0, 0), start_button.rect, 1)
        pygame.draw.rect(window, (255, 0, 0), settings_button.rect, 1)
        pygame.draw.rect(window, (255, 0, 0), exit_button.rect, 1)
        if start_button.button_click():
            button_show_state = 'menu'
        elif settings_button.button_click():
            button_show_state = 'settings'
    if button_show_state == 'settings':
        window.blit(image, (0, 0))
        store_button.draw()
        add_volume_button.draw()
        reduce_volume_button.draw()
        pygame.draw.rect(window, (255, 0, 0), store_button.rect, 1)
        pygame.draw.rect(window, (255, 0, 0), add_volume_button.rect, 1)
        pygame.draw.rect(window, (255, 0, 0), reduce_volume_button.rect, 1)
        if reduce_volume_button.button_click():
            button_show_state = 'main menu'


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


def level_3():
    window.fill((0, 0, 0))
    window.blit(text, (10, 0))

    floor_level3()
    walls_level3()
    pygame.display.update()
    clock.tick(fps)


# MAIN CYCLE
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
            sys.exit()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    text = font1.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))

    # tutorial()
    # level_1()
    # level_2()
    level_3()
    # menu()

    pygame.display.update()
    clock.tick(fps)

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


