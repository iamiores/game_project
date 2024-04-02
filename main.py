import sys
import pygame
from pygame import *
from coin import Coin
pygame.init()


class MainSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(pygame.image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.was_colliding = False

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def collide(self, group):
        for group in group:
            if self.rect.colliderect(group.rect):
                if self.rect.top < group.rect.bottom < self.rect.bottom:
                    self.rect.y += 1
                elif self.rect.bottom > group.rect.top > self.rect.top:
                    self.rect.y -= 1
                elif self.rect.left < group.rect.right < self.rect.right:
                    self.rect.x += 1
                elif self.rect.right > group.rect.left > self.rect.left:
                    self.rect.x -= 1

    def trap(self, group):
        global lives
        if not self.was_colliding:
            if any(self.rect.colliderect(group.rect) for group in group):
                lives -= 1
                self.was_colliding = True
        elif not any(self.rect.colliderect(group.rect) for group in group):
            self.was_colliding = False


class Player(MainSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.rect.width = width
        self.rect.height = height
        self.width = width
        self.height = height
        self.counter_right = 0
        self.counter_left = 0
        self.counter_forward = 0
        self.counter_backward = 0
        self.pics_stay = transform.scale(pygame.image.load('images/player/male/male_WalkBack_1.png'), (self.width, self.height))

        self.pics_right = ['images/player/male/male_WalkRight_2.png', 'images/player/male/male_WalkRight_1.png', 'images/player/male/male_WalkRight_3.png', 'images/player/male/male_WalkRight_1.png']
        self.pics_right_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_right]

        self.pics_left = ['images/player/male/male_WalkLeft_2.png', 'images/player/male/male_WalkLeft_1.png', 'images/player/male/male_WalkLeft_3.png', 'images/player/male/male_WalkLeft_1.png']
        self.pics_left_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_left]

        self.pics_forward = ['images/player/male/male_WalkForward_2.png', 'images/player/male/male_WalkForward_1.png', 'images/player/male/male_WalkForward_3.png', 'images/player/male/male_WalkForward_1.png']
        self.pics_forward_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_forward]

        self.pics_back = ['images/player/male/male_WalkBack_2.png', 'images/player/male/male_WalkBack_1.png', 'images/player/male/male_WalkBack_3.png', 'images/player/male/male_WalkBack_1.png']
        self.pics_back_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_back]

    def animate(self, kind):
        if kind == 'stay':
            self.image = self.pics_stay

        if kind == 'right':
            self.counter_right += 1
            if self.counter_right < 5:
                self.image = self.pics_right_obj[0]
            elif 5 <= self.counter_right < 10:
                self.image = self.pics_right_obj[1]
            elif 10 <= self.counter_right < 15:
                self.image = self.pics_right_obj[2]
            elif 15 <= self.counter_right < 20:
                self.image = self.pics_right_obj[3]

            elif self.counter_right == 20:
                self.counter_right = 0
        else:
            self.counter_right = 0

        if kind == 'left':
            self.counter_left += 1
            if self.counter_left < 5:
                self.image = self.pics_left_obj[0]
            elif 5 <= self.counter_left < 10:
                self.image = self.pics_left_obj[1]
            elif 10 <= self.counter_left < 15:
                self.image = self.pics_left_obj[2]
            elif 15 <= self.counter_left < 20:
                self.image = self.pics_left_obj[3]

            elif self.counter_left == 20:
                self.counter_left = 0
        else:
            self.counter_left = 0

        if kind == 'forward':
            self.counter_forward += 1
            if self.counter_forward  < 5:
                self.image = self.pics_forward_obj[0]
            elif 5 <= self.counter_forward  < 10:
                self.image = self.pics_forward_obj[1]
            elif 10 <= self.counter_forward  < 15:
                self.image = self.pics_forward_obj[2]
            elif 15 <= self.counter_forward  < 20:
                self.image = self.pics_forward_obj[3]

            elif self.counter_forward  == 20:
                self.counter_forward  = 0
        else:
            self.counter_forward = 0

        if kind == 'back':
            self.counter_backward += 1
            if self.counter_backward < 5:
                self.image = self.pics_back_obj[0]
            elif 5 <= self.counter_backward < 10:
                self.image = self.pics_back_obj[1]
            elif 10 <= self.counter_backward < 15:
                self.image = self.pics_back_obj[2]
            elif 15 <= self.counter_backward < 20:
                self.image = self.pics_back_obj[3]

            elif self.counter_backward == 20:
                self.counter_backward = 0
        else:
            self.counter_backward = 0

    def update(self):
        keys = key.get_pressed()
        if keys[K_d]:
            self.rect.x += self.speed
            self.animate('right')
        if keys[K_a]:
            self.rect.x -= self.speed
            self.animate('left')

        if keys[K_w]:
            self.rect.y -= self.speed
            self.animate('forward')

        if keys[K_s]:
            self.rect.y += self.speed
            self.animate('back')

        if keys[K_d] or keys[K_a] or keys[K_w] or keys[K_s]:
            self.write_file()
        else:
            self.animate('stay')

    def write_file(self):
        with open('file.txt', 'w') as f:
            f.write(str(self.rect.x) + '\n')
            f.write(str(self.rect.y))


class For_Level_Building(sprite.Sprite):
    def __init__(self, wall_x, wall_y, wall_width, wall_height, file_image):
        super().__init__()
        self.file = file_image
        self.image = transform.scale(pygame.image.load(self.file), (wall_width, wall_height))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

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

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def button_click(self):
        mouse_controller = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_controller):
            if click[0] and not self.clicked:
                self.clicked = True
                return True
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
hatch_num_lvl3 = 0

lives = 5
energy = 5

button_show_state = 'main menu'


# GROUPS, LISTS ETC
hatch_tut = []
hatch_lvl1 = []
hatch_lvl2 = []
hatch_lvl3 = []
collide_group = sprite.Group()
traps_group = sprite.Group()
all_sprites = sprite.Group()

# OBJECTS

coin = Coin(x=500, y=136, width=20, height=20)
player = Player('images/player/male/male_WalkBack_1.png', 450, 200, 6, 28, 33)

all_sprites.add(coin)
all_sprites.add(player)


# WALLS
def walls_tut():
    from levels import wall_tuts
    for keys, value in wall_tuts.items():
        w = For_Level_Building(*value)
        collide_group.add(w)
        w.update()


def walls_level1():
    from levels import wall_lvl1
    for keys, value in wall_lvl1.items():
        w = For_Level_Building(*value)
        collide_group.add(w)
        w.update()


def walls_level2():
    from levels import wall_lvl2
    for keys, value in wall_lvl2.items():
        w = For_Level_Building(*value)
        collide_group.add(w)
        w.update()


def walls_level3():
    from levels import wall_lvl3
    for keys, value in wall_lvl3.items():
        w = For_Level_Building(*value)
        collide_group.add(w)
        w.update()
        # pygame.draw.rect(window, (255, 0, 0), w.rect, 1)


# FLOORS
def floor_tut():
    from levels import floor_tuts
    for keys, value in floor_tuts.items():
        f = For_Level_Building(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (263, 525, 160, 60))
    pygame.draw.rect(window, (43, 35, 52), (555, 323, 80, 140))


def floor_level1():
    from levels import floor_lvl1
    for keys, value in floor_lvl1.items():
        f = For_Level_Building(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (596, 427, 161, 60))
    pygame.draw.rect(window, (43, 35, 52), (835, 266, 70, 121))
    pygame.draw.rect(window, (43, 35, 52), (512, 113, 141, 67))


def floor_level2():
    from levels import floor_lvl2
    for keys, value in floor_lvl2.items():
        f = For_Level_Building(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (180, 372, 80, 144))
    pygame.draw.rect(window, (43, 35, 52), (422, 212, 150, 60))
    pygame.draw.rect(window, (43, 35, 52), (720, 370, 85, 123))


def floor_level3():
    from levels import floor_lvl3
    for keys, value in floor_lvl3.items():
        f = For_Level_Building(*value)
        f.update()
    pygame.draw.rect(window, (43, 35, 52), (455, 236, 82, 120))


# ITEMS
def items_tut():
    from levels import item_tuts, trap_tuts
    for keys, values in item_tuts.items():
        i = For_Level_Building(*values)
        i.update()
        collide_group.add(i)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, values in trap_tuts.items():
        t = For_Level_Building(*values)
        t.update()
        traps_group.add(t)
        # pygame.draw.rect(window, (255, 0, 0), s.rect, 1)
    closed_hatch = For_Level_Building(574, 205, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(574, 205, 43, 35, 'images/items/open_hatch.png')
    hatch_tut.append(closed_hatch)
    hatch_tut.append(opened_hatch)
    portal = For_Level_Building(140, 175, 50, 80, 'images/items/portal.png')
    window.blit(portal.image, (portal.rect.x, portal.rect.y))


def items_level1():
    from levels import item_lvl1, trap_lvl1
    for keys, values in item_lvl1.items():
        i = For_Level_Building(*values)
        i.update()
        collide_group.add(i)
    for keys, values in trap_lvl1.items():
        t = For_Level_Building(*values)
        t.update()
        traps_group.add(t)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    closed_hatch = For_Level_Building(370, 140, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(370, 140, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl1.append(closed_hatch)
    hatch_lvl1.append(opened_hatch)
    portal = For_Level_Building(170, 110, 50, 80, 'images/items/portal.png')
    window.blit(portal.image, (portal.rect.x, portal.rect.y))


def items_level2():
    from levels import item_lvl2, trap_lvl2
    for keys, values in item_lvl2.items():
        i = For_Level_Building(*values)
        i.update()
        collide_group.add(i)
    for keys, value in trap_lvl2.items():
        t = For_Level_Building(*value)
        t.update()
        traps_group.add(t)
    closed_hatch = For_Level_Building(740, 575, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(740, 575, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl2.append(closed_hatch)
    hatch_lvl2.append(opened_hatch)
    portal = For_Level_Building(550, 540, 50, 80, 'images/items/portal.png')
    window.blit(portal.image, (portal.rect.x, portal.rect.y))


def items_level3():
    from levels import item_lvl3, trap_lvl3
    for keys, value in item_lvl3.items():
        i = For_Level_Building(*value)
        collide_group.add(i)
        i.update()
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, value in trap_lvl3.items():
        t = For_Level_Building(*value)
        traps_group.add(t)
        t.update()
        # pygame.draw.rect(window, (255, 0, 0), t.rect, 1)
    closed_hatch = For_Level_Building(472, 470, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(472, 470, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl3.append(closed_hatch)
    hatch_lvl3.append(opened_hatch)
    portal = For_Level_Building(470, 585, 40, 60, 'images/items/portal.png')
    window.blit(portal.image, (portal.rect.x, portal.rect.y))


# LEVELS
# def menu():
#     global button_show_state
#     start_button = Button(435, 240, 120, 50, 'images/buttons/start.png')
#     settings_button = Button(435, 300, 120, 50, 'images/buttons/settings.png')
#     exit_button = Button(435, 360, 120, 50, 'images/buttons/exit.png')
#     store_button = Button(450, 240, 60, 50, 'images/buttons/store.png')
#     add_volume_button = Button(400, 300, 60, 50, 'images/buttons/more_volume.png')
#     reduce_volume_button = Button(500, 300, 60, 50, 'images/buttons/less_volume.png')
#     pause_button = None
#     back_to_menu_button = None
#     window.blit(image, (0, 0))
#     if button_show_state == 'main menu':
#         start_button.draw()
#         settings_button.draw()
#         exit_button.draw()
#         pygame.draw.rect(window, (255, 0, 0), start_button.rect, 1)
#         pygame.draw.rect(window, (255, 0, 0), settings_button.rect, 1)
#         pygame.draw.rect(window, (255, 0, 0), exit_button.rect, 1)
#         if start_button.button_click():
#             button_show_state = 'menu'
#         elif settings_button.button_click():
#             button_show_state = 'settings'
#     if button_show_state == 'settings':
#         window.blit(image, (0, 0))
#         store_button.draw()
#         add_volume_button.draw()
#         reduce_volume_button.draw()
#         pygame.draw.rect(window, (255, 0, 0), store_button.rect, 1)
#         pygame.draw.rect(window, (255, 0, 0), add_volume_button.rect, 1)
#         pygame.draw.rect(window, (255, 0, 0), reduce_volume_button.rect, 1)
#         if reduce_volume_button.button_click():
#             button_show_state = 'main menu'


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
    items_level3()
    # window.blit(hatch_lvl3[hatch_num_lvl3].image, (hatch_lvl3[hatch_num_lvl3].rect.x, hatch_lvl3[hatch_num_lvl3].rect.y))
    pygame.display.update()
    clock.tick(fps)


try:
    with open('file.txt', 'r') as f:
        player.rect.x = int(f.readline().replace('\n', ''))
        player.rect.y = int(f.readline().replace('\n', ''))
except:
    player.write_file()


# MAIN CYCLE
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
            sys.exit()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    text = font1.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))

    tutorial()
    # level_1()
    # level_2()
    # level_3()

    all_sprites.update()  # Обновление всех спрайтов
    all_sprites.draw(window)  # Отображение всех спрайтов
    player.collide(collide_group)
    player.trap(traps_group)
    # pygame.draw.rect(window, (255, 0, 0), player.rect, 1)
    # print(lives)
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