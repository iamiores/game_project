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


class Boss(MainSprite):
    def __init__(self, boss_image, boss_x, boss_y, boss_speed, width, height):
        super().__init__(boss_image, boss_x, boss_y, boss_speed)
        self.rect.width = width
        self.rect.height = height
        self.width = width
        self.height = height
        self.counter_idle = 0
        self.counter_right = 0
        self.counter_left = 0
        self.counter_attack_right = 0
        self.counter_attack_left = 0

        self.pics_idle = ['images/monsters/boss/boss_idle_left_1.png', 'images/monsters/boss/boss_idle_left_2.png', 'images/monsters/boss/boss_idle_left_3.png', 'images/monsters/boss/boss_idle_left_4.png']
        self.pics_idle_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_idle]

        self.pics_attack_right = ['images/monsters/boss/boss_attack_right_1.png', 'images/monsters/boss/boss_attack_right_2.png', 'images/monsters/boss/boss_attack_right_3.png', 'images/monsters/boss/boss_attack_right_4.png', 'images/monsters/boss/boss_attack_right_5.png']
        self.pics_attack_right_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_attack_right]

        self.pics_attack_left = ['images/monsters/boss/boss_attack_left_1.png', 'images/monsters/boss/boss_attack_left_2.png', 'images/monsters/boss/boss_attack_left_3.png', 'images/monsters/boss/boss_attack_left_4.png', 'images/monsters/boss/boss_attack_left_5.png']
        self.pics_attack_left_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_attack_left]

        self.pics_right = ['images/monsters/boss/boss_walk_right_1.png', 'images/monsters/boss/boss_walk_right_1.png', 'images/monsters/boss/boss_walk_right_2.png','images/monsters/boss/boss_walk_right_3.png']
        self.pics_right_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_right]

        self.pics_left = ['images/monsters/boss/boss_walk_left_1.png', 'images/monsters/boss/boss_walk_left_2.png', 'images/monsters/boss/boss_walk_right_2.png','images/monsters/boss/boss_walk_left_3.png']
        self.pics_left_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_left]

    def animate(self, kind):
        if kind == 'stay':
            self.counter_idle += 1
            if self.counter_idle < 5:
                self.image = self.pics_idle_obj[0]
            elif 5 <= self.counter_idle < 10:
                self.image = self.pics_idle_obj[1]
            elif 10 <= self.counter_idle < 15:
                self.image = self.pics_idle_obj[2]
            elif 15 <= self.counter_idle < 20:
                self.image = self.pics_idle_obj[3]

            elif self.counter_idle == 20:
                self.counter_idle = 0
        else:
            self.counter_idle = 0

        if kind == 'attack right':
            self.counter_attack_right += 1
            if self.counter_attack_right < 5:
                self.image = self.pics_attack_right_obj[0]
            elif 5 <= self.counter_attack_right < 10:
                self.image = self.pics_attack_right_obj[1]
            elif 10 <= self.counter_attack_right < 15:
                self.image = self.pics_attack_right_obj[2]
            elif 15 <= self.counter_attack_right < 20:
                self.image = self.pics_attack_right_obj[3]

            elif self.counter_attack_right == 20:
                self.counter_attack_right = 0
        else:
            self.counter_attack_right = 0

        if kind == 'attack left':
            self.counter_attack_left += 1
            if self.counter_attack_left < 5:
                self.image = self.pics_attack_left_obj[0]
            elif 5 <= self.counter_attack_left < 10:
                self.image = self.pics_attack_left_obj[1]
            elif 10 <= self.counter_attack_left < 15:
                self.image = self.pics_attack_left_obj[2]
            elif 15 <= self.counter_attack_left < 20:
                self.image = self.pics_attack_left_obj[3]

            elif self.counter_attack_left == 20:
                self.counter_attack_left = 0
        else:
            self.counter_attack_left = 0

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

        if kind == 'attack left':
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

    def update(self, target_x, target_y, target):
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y

        # Переслідування
        if dx != 0 or dy != 0:
            if abs(dx) > abs(dy):  # Перевірка, чи більша різниця по горизонталі
                if dx > 0:
                    self.animate('right')
                else:
                    self.animate('left')
        else:
            self.animate('stay')

        if pygame.sprite.collide_rect(self, target):
            self.animate('attack left')

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
    def __init__(self, button_x, button_y, button_width, button_height, text):
        self.width = button_width
        self.height = button_height
        self.x = button_x
        self.y = button_y
        self.clicked = False
        self.inactive_color = (21, 24, 38)
        self.active_color = (41, 47, 75)
        self.border_radius = 20
        self.text = text

    def click_with_action(self, screen, action=None):
        mouse_controller = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x < mouse_controller[0] < self.x + self.width and self.y < mouse_controller[1] < self.y + self.height:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height), border_radius=self.border_radius)
            if click[0]:
                if action is not None:
                    action()
                    button_click_sound.play()
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height), border_radius=self.border_radius)

        create_text(screen, self.text, x=self.x + 10, y=self.y + 10)

    def click(self, screen):
        mouse_controller = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x < mouse_controller[0] < self.x + self.width and self.y < mouse_controller[1] < self.y + self.height:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height), border_radius=self.border_radius)
            if click[0]:
                button_click_sound.play()
                return True
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height), border_radius=self.border_radius)

        create_text(screen, self.text, x=self.x + 10, y=self.y + 10)


def create_text(screen, text, x, y, font_color=(0, 0, 0), font_size=25):
    text = pygame.font.Font('fonts/Retro Gaming.ttf', font_size).render(text, True, font_color)
    screen.blit(text, (x, y))


# FONTS
font1 = pygame.font.Font('fonts/Retro Gaming.ttf', 20)

# SETTINGS
w_width, w_height = 1000, 700
window = pygame.display.set_mode((w_width, w_height))
clock = pygame.time.Clock()
fps = 60
game = True
bg_image = transform.scale(pygame.image.load('bg.png'), (w_width, w_height))

# ALTERNATES
hatch_num_tut = 0
hatch_num_lvl1 = 0
hatch_num_lvl2 = 0
hatch_num_lvl3 = 0

lives = 5
energy = 5
coins = 0

state = 'main menu'

# LOADS
live_0 = transform.scale(pygame.image.load('images/lives/lives_0.png'), (100, 45))
live_1 = transform.scale(pygame.image.load('images/lives/lives_1.png'), (100, 45))
live_2 = transform.scale(pygame.image.load('images/lives/lives_2.png'), (100, 45))
live_3 = transform.scale(pygame.image.load('images/lives/lives_3.png'), (100, 45))
live_4 = transform.scale(pygame.image.load('images/lives/lives_4.png'), (100, 45))
live_5 = transform.scale(pygame.image.load('images/lives/lives_5.png'), (100, 45))

energy_0 = transform.scale(pygame.image.load('images/energy/energy_0.png'), (90, 20))
energy_1 = transform.scale(pygame.image.load('images/energy/energy_1.png'), (90, 20))
energy_2 = transform.scale(pygame.image.load('images/energy/energy_2.png'), (90, 20))
energy_3 = transform.scale(pygame.image.load('images/energy/energy_3.png'), (90, 20))
energy_4 = transform.scale(pygame.image.load('images/energy/energy_4.png'), (90, 20))
energy_5 = transform.scale(pygame.image.load('images/energy/energy_5.png'), (90, 20))


# GROUPS, LISTS ETC
lives_list = [live_0, live_1, live_2, live_3, live_4, live_5]
energy_list = [energy_0, energy_1, energy_2, energy_3, energy_4, energy_5]

hatch_tut = []
hatch_lvl1 = []
hatch_lvl2 = []
hatch_lvl3 = []
collide_group = sprite.Group()
traps_group = sprite.Group()

all_sprites = sprite.Group()

# OBJECTS
start_button = Button(440, 240, 110, 50, 'START')
settings_button = Button(410, 300, 170, 50, 'SETTINGS')
exit_button = Button(445, 360, 95, 50, 'QUIT')
add_volume_button = Button(400, 300, 60, 50, '+')
reduce_volume_button = Button(500, 300, 60, 50, '-')
back_button = Button(450, 425, 95, 50, 'BACK')

tutorial_button = Button(410, 180, 170, 50, 'TUTORIAL')
level_1_button = Button(250, 280, 130, 50, 'LEVEL 1')
level_2_button = Button(430, 280, 130, 50, 'LEVEL 2')
level_3_button = Button(610, 280, 130, 50, 'LEVEL 3')
store_button = Button(450, 240, 60, 50, '🛒')

coin = Coin(x=240, y=33, width=27, height=27)
player = Player('images/player/male/male_WalkBack_1.png', 450, 200, 6, 28, 33)
all_sprites.add(coin)
all_sprites.add(player)

# SOUNDS
music = pygame.mixer.Sound('music/Crystal Caves v1_2.mp3')
music_volume = 0.4
button_click_sound = pygame.mixer.Sound('sounds/Menu Selection Click.wav')


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
def menu():
    global state, music_volume, game
    if state != 'game':
        window.blit(bg_image, (0, 0))
    music.set_volume(music_volume)
    if state == 'main menu':
        if start_button.click(window):
            state = 'level menu'
        elif settings_button.click(window):
            state = 'settings'
        elif exit_button.click(window):
            game = False
            sys.exit()
    if state == 'settings':
        if add_volume_button.click(window):
            music_volume += 0.1
        elif reduce_volume_button.click(window):
            music_volume -= 0.1
        elif back_button.click(window):
            state = 'main menu'
    if state == 'level menu':
        if tutorial_button.click(window):
            state = 'tutorial'
        elif level_1_button.click(window):
            state = 'level 1'
            level_1()
        elif level_2_button.click(window):
            state = 'level 2'
            level_2()
        elif level_3_button.click(window):
            state = 'level 3'
            level_3()
        elif back_button.click(window):
            state = 'main menu'


def tutorial():
    window.fill((0, 0, 0))

    floor_tut()
    walls_tut()
    items_tut()
    window.blit(hatch_tut[hatch_num_tut].image, (hatch_tut[hatch_num_tut].rect.x, hatch_tut[hatch_num_tut].rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_1():
    window.fill((0, 0, 0))

    floor_level1()
    walls_level1()
    items_level1()
    window.blit(hatch_lvl1[hatch_num_lvl1].image, (hatch_lvl1[hatch_num_lvl1].rect.x, hatch_lvl1[hatch_num_lvl1].rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_2():
    window.fill((0, 0, 0))

    floor_level2()
    walls_level2()
    items_level2()
    window.blit(hatch_lvl2[hatch_num_lvl2].image, (hatch_lvl2[hatch_num_lvl2].rect.x, hatch_lvl2[hatch_num_lvl2].rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_3():
    window.fill((0, 0, 0))

    floor_level3()
    walls_level3()
    items_level3()
    window.blit(hatch_lvl3[hatch_num_lvl3].image, (hatch_lvl3[hatch_num_lvl3].rect.x, hatch_lvl3[hatch_num_lvl3].rect.y))
    pygame.display.update()
    clock.tick(fps)


# try:
#     with open('file.txt', 'r') as f:
#         player.rect.x = int(f.readline().replace('\n', ''))
#         player.rect.y = int(f.readline().replace('\n', ''))
# except:
#     player.write_file()

# music.play()
# MAIN CYCLE
money = font1.render(": " + str(coins), True, pygame.color.Color('white'))
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
            sys.exit()

    if state == 'main menu' or state == 'level menu' or state == 'settings':
        menu()
    if state == 'tutorial':
        tutorial()
    if state == 'level 1':
        level_1()
    if state == 'level 2':
        level_2()
    if state == 'level 3':
        level_3()
    if state == 'tutorial' or state == 'level 1' or state == 'level 2' or state == 'level 3':
        window.blit(money, (255, 20))
        all_sprites.update()  # Обновление всех спрайтов
        all_sprites.draw(window)  # Отображение всех спрайтов
        player.collide(collide_group)
        player.trap(traps_group)
        window.blit(lives_list[lives], (10, 0))
        window.blit(energy_list[energy], (120, 24))
    # tutorial()
    # level_1()
    # level_2()
    # level_3()
    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # text = font1.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))


    # pygame.draw.rect(window, (255, 0, 0), player.rect, 1)
    # print(lives)

    # window.blit(energy_list[energy], (15, 60))

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