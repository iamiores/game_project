import sys
import pygame
from pygame import *
from coin import Coin
from goblin import Goblin
from button import Button
import math
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

    def show(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Boss(sprite.Sprite):
    def __init__(self, boss_image, boss_x, boss_y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(pygame.image.load(boss_image), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = boss_x
        self.rect.y = boss_y
        self.rect.width = width
        self.rect.height = height
        self.speed = 5
        self.counter_idle = 0
        self.counter_right = 0
        self.counter_left = 0
        self.counter_attack_right = 0
        self.counter_attack_left = 0
        self.direction = 'left'
        self.health = 100

        self.pics_idle = ['images/monsters/boss/boss_idle_left_1.png', 'images/monsters/boss/boss_idle_left_2.png', 'images/monsters/boss/boss_idle_left_3.png', 'images/monsters/boss/boss_idle_left_4.png']
        self.pics_idle_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_idle]

        self.pics_attack_right = ['images/monsters/boss/boss_attack_right_1.png', 'images/monsters/boss/boss_attack_right_2.png', 'images/monsters/boss/boss_attack_right_3.png', 'images/monsters/boss/boss_attack_right_4.png', 'images/monsters/boss/boss_attack_right_5.png']
        self.pics_attack_right_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_attack_right]

        self.pics_attack_left = ['images/monsters/boss/boss_attack_left_1.png', 'images/monsters/boss/boss_attack_left_2.png', 'images/monsters/boss/boss_attack_left_3.png', 'images/monsters/boss/boss_attack_left_4.png', 'images/monsters/boss/boss_attack_left_5.png']
        self.pics_attack_left_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_attack_left]

        self.pics_right = ['images/monsters/boss/boss_walk_right_1.png', 'images/monsters/boss/boss_walk_right_2.png', 'images/monsters/boss/boss_walk_right_3.png']
        self.pics_right_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_right]

        self.pics_left = ['images/monsters/boss/boss_walk_left_1.png', 'images/monsters/boss/boss_walk_left_2.png', 'images/monsters/boss/boss_walk_left_3.png']
        self.pics_left_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_left]

    def animate(self, kind):
        global lives
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
                lives -= 1
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
                lives -= 1
                self.counter_attack_left = 0
        else:
            self.counter_attack_left = 0

        if kind == 'right':
            self.direction = 'right'
            self.counter_right += 1
            if self.counter_right < 5:
                self.image = self.pics_right_obj[0]
            elif 5 <= self.counter_right < 10:
                self.image = self.pics_right_obj[1]
            elif 10 <= self.counter_right < 15:
                self.image = self.pics_right_obj[2]

            elif self.counter_right == 15:
                self.counter_right = 0
        else:
            self.counter_right = 0

        if kind == 'left':
            self.direction = 'left'
            self.counter_left += 1
            if self.counter_left < 5:
                self.image = self.pics_left_obj[0]
            elif 5 <= self.counter_left < 10:
                self.image = self.pics_left_obj[1]
            elif 10 <= self.counter_left < 15:
                self.image = self.pics_left_obj[2]

            elif self.counter_left == 15:
                self.counter_left = 0
        else:
            self.counter_left = 0

        if kind == 'attack right' or kind == 'attack left':
            self.speed = 1
        else:
            self.speed = 5

    def update(self, target, target_y, y):
        if target_y >= y:
            if self.direction == 'left':
                if self.rect.colliderect(target.rect):
                    self.animate('attack left')
                else:
                    self.animate('left')
                self.rect.x -= self.speed
                if self.rect.x <= 340:
                    self.direction = 'right'
            elif self.direction == 'right':
                if self.rect.colliderect(target.rect):
                    self.animate('attack right')
                else:
                    self.animate('right')
                self.rect.x += self.speed
                if self.rect.x >= 610:
                    self.direction = 'left'
        else:
            self.animate('stay')

    def show(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.speed = player_speed
        self.was_colliding = False
        self.armor = "no_armor"
        self.weapon = "no_weapon"
        self.is_spawned = False
        self.width = width
        self.height = height
        self.image = transform.scale(pygame.image.load(player_image), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.width = width
        self.rect.height = height
        self.rect.x = player_x
        self.rect.y = player_y
        self.counter_right = 0
        self.counter_left = 0
        self.counter_forward = 0
        self.counter_backward = 0
        self.direction = None
        self.pics_stay = ['images/player/male/male_WalkForward_1.png', 'images/player/male/male_WalkBack_1.png', 'images/player/male/male_WalkLeft_1.png', 'images/player/male/male_WalkRight_3.png']
        self.pics_stay_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_stay]

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
            if self.direction == 'forward':
                self.image = self.pics_stay_obj[0]
            elif self.direction == 'back':
                self.image = self.pics_stay_obj[1]
            elif self.direction == 'right':
                self.image = self.pics_stay_obj[3]
            elif self.direction == 'left':
                self.image = self.pics_stay_obj[2]
            else:
                self.image = self.pics_stay_obj[1]

        if kind == 'right':
            self.direction = 'right'
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
            self.direction = 'left'
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
            self.direction = 'forward'
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
            self.direction = 'back'
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
        elif keys[K_a]:
            self.rect.x -= self.speed
            self.animate('left')

        elif keys[K_w]:
            self.rect.y -= self.speed
            self.animate('forward')

        elif keys[K_s]:
            self.rect.y += self.speed
            self.animate('back')

        else:
            self.animate('stay')

    def spawn(self, x, y):
        if not self.is_spawned:
            self.rect.x = x
            self.rect.y = y
            self.is_spawned = True

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

    def equip_armor(self, armor_name):
        self.armor = armor_name
        print(self.armor)

    def equip_weapon(self, weapon_name):
        self.weapon = weapon_name
        print(self.weapon)

    def attack(self, target):
        if self.weapon == "no_weapon":
            print("You don't have any weapon equipped!")

        attack_properties = WEAPON_TABLE.get(self.weapon)
        if attack_properties:
            attack_power, attack_range = attack_properties
            distance = math.sqrt((self.rect.x - target.rect.x) ** 2 + (self.rect.y - target.rect.y) ** 2)
            if distance <= attack_range:
                target.health -= attack_power
                print(f"You dealt {attack_power} damage to the target!")
                print(target.health)
            else:
                print("Target is out of range!")
        else:
            print("Weapon not found in the weapon table!")


WEAPON_TABLE = {
    # attack, range
    "no_weapon": [5, 5],
    "knife": [10, 5],
    "great_sword": [15, 5],
    "steel_sword": [20, 10],
    "bow": [20, 10],
    "axe": [15, 10]
}

ARMOR_TABLE = {
    # defence, magic_defence
    "no_armor": [0, 30],
    "armor": [50, 80],
    "great_armor": [100, 30]
}




class For_Level_Building(sprite.Sprite):
    def __init__(self, x, y, width, height, file_image):
        super().__init__()
        self.file = file_image
        self.image = transform.scale(pygame.image.load(self.file), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# FONTS
font1 = pygame.font.Font('fonts/Retro Gaming.ttf', 20)
font2 = pygame.font.Font('fonts/Retro Gaming.ttf', 14)

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
finished = False

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

armor = transform.scale(pygame.image.load('store_items/armor.png'), (92, 92))
great_armor = transform.scale(pygame.image.load('store_items/great_armor.png'), (92, 92))
great_sword = transform.scale(pygame.image.load('store_items/great_sword.png'), (92, 92))
steel_sword = transform.scale(pygame.image.load('store_items/steel_sword.png'), (92, 92))
axe = transform.scale(pygame.image.load('store_items/axe.png'), (90, 92))
bow = transform.scale(pygame.image.load('store_items/bow.png'), (92, 92))
health_potion = transform.scale(pygame.image.load('store_items/health_potion.png'), (76, 92))
energy_potion = transform.scale(pygame.image.load('store_items/energy_potion.png'), (66, 88))


# GROUPS, LISTS ETC
lives_list = [live_0, live_1, live_2, live_3, live_4, live_5]
energy_list = [energy_0, energy_1, energy_2, energy_3, energy_4, energy_5]

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


all_sprites = sprite.Group()

# BUTTONS
start_button = Button(450, 255, 110, 45, 'START')
settings_button = Button(427, 310, 155, 45, 'SETTINGS')
store_button = Button(450, 365, 110, 45, 'STORE')
exit_button = Button(460, 420, 90, 45, 'QUIT')
add_volume_button = Button(415, 300, 50, 45, '+')
reduce_volume_button = Button(515, 300, 50, 45, '-')
back_button = Button(460, 475, 95, 45, 'BACK')
back_button_2 = Button(460, 465, 95, 45, 'BACK')

tutorial_button = Button(425, 180, 155, 45, 'TUTORIAL')
level_1_button = Button(260, 300, 125, 45, 'LEVEL 1')
level_2_button = Button(440, 300, 125, 45, 'LEVEL 2')
level_3_button = Button(620, 300, 125, 45, 'LEVEL 3')
home_button = Button(900, 5, 95, 50, 'HOME')

armor_button = Button(300, 150, 110, 50, 'ARMOR')
swords_button = Button(440, 150, 130, 50, 'SWORDS')
potions_button = Button(600, 150, 140, 50, 'POTIONS')

buy_armor_button = Button(380, 365, 77, 47, 'BUY')
buy_great_armor_button = Button(550, 365, 77, 47, 'BUY')
buy_great_sword_button = Button(215, 365, 77, 47, 'BUY')
buy_steel_sword_button = Button(715, 365, 77, 47, 'BUY')
buy_bow_button = Button(380, 365, 77, 47, 'BUY')
buy_axe_button = Button(550, 365, 77, 47, 'BUY')
buy_health_potion_button = Button(380, 365, 77, 47, 'BUY')
buy_energy_potion_button = Button(550, 365, 77, 47, 'BUY')
price_num = {
    'armor_price_num': 2,
    'great_armor_price_num': 4,
    'great_sword_price_num': 2,
    'steel_sword_price_num': 4,
    'bow_price_num': 5,
    'axe_price_num': 3,
    'health_potion_price_num': [1, 1],
    'energy_potion_price_num': [1, 2]
}

armor_price = font1.render(str(price_num['armor_price_num']), True, pygame.color.Color('white'))
great_armor_price = font1.render(str(price_num['great_armor_price_num']), True, pygame.color.Color('white'))
great_sword_price = font1.render(str(price_num['great_sword_price_num']), True, pygame.color.Color('white'))
steel_sword_price = font1.render(str(price_num['steel_sword_price_num']), True, pygame.color.Color('white'))
bow_price = font1.render(str(price_num['bow_price_num']), True, pygame.color.Color('white'))
axe_price = font1.render(str(price_num['axe_price_num']), True, pygame.color.Color('white'))
health_potion_price = font1.render(str(price_num['health_potion_price_num'][0]), True, pygame.color.Color('white'))
energy_potion_price = font1.render(str(price_num['energy_potion_price_num'][0]), True, pygame.color.Color('white'))


# OBJECTS
coin = Coin(x=240, y=33, width=27, height=27)
player = Player('images/player/male/male_WalkBack_1.png', 490, 133, 5, 28, 33)
boss = Boss('images/monsters/boss/boss_idle_left_1.png', 465, 500, 50, 60)
goblin = Goblin('images/monsters/goblin/goblin_idle_right_1.png', 695, 520, 30, 20)
all_sprites.add(coin)
all_sprites.add(player)

portal_tut = For_Level_Building(200, 175, 50, 80, 'images/items/portal.png')
portal_lvl1 = For_Level_Building(150, 110, 50, 80, 'images/items/portal.png')
portal_lvl2 = For_Level_Building(550, 540, 50, 80, 'images/items/portal.png')
portal_lvl3 = For_Level_Building(470, 585, 40, 60, 'images/items/portal.png')

# SOUNDS
music = pygame.mixer.Sound('music/Crystal Caves v1_2.mp3')
collect_coin_sound = pygame.mixer.Sound('sounds/coin_collect.wav')
music_volume = 0.4


# WALLS
def walls_tut():
    from levels import wall_tuts
    for keys, value in wall_tuts.items():
        w = For_Level_Building(*value)
        collide_group_tut.add(w)
        w.update()
        # pygame.draw.rect(window, (255, 0, 0), w.rect, 1)


def walls_level1():
    from levels import wall_lvl1
    for keys, value in wall_lvl1.items():
        w = For_Level_Building(*value)
        collide_group_lvl1.add(w)
        w.update()
        # pygame.draw.rect(window, (255, 0, 0), w.rect, 1)


def walls_level2():
    from levels import wall_lvl2
    for keys, value in wall_lvl2.items():
        w = For_Level_Building(*value)
        collide_group_lvl2.add(w)
        w.update()
        # pygame.draw.rect(window, (255, 0, 0), w.rect, 1)


def walls_level3():
    from levels import wall_lvl3
    for keys, value in wall_lvl3.items():
        w = For_Level_Building(*value)
        collide_group_lvl3.add(w)
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
        collide_group_tut.add(i)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, values in trap_tuts.items():
        t = For_Level_Building(*values)
        t.update()
        traps_group_tut.add(t)
        # pygame.draw.rect(window, (255, 0, 0), t.rect, 1)
    closed_hatch = For_Level_Building(574, 205, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(574, 205, 43, 35, 'images/items/open_hatch.png')
    hatch_tut.append(closed_hatch)
    hatch_tut.append(opened_hatch)


def items_level1():
    from levels import item_lvl1, trap_lvl1
    for keys, values in item_lvl1.items():
        i = For_Level_Building(*values)
        i.update()
        collide_group_lvl1.add(i)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, values in trap_lvl1.items():
        t = For_Level_Building(*values)
        t.update()
        traps_group_lvl1.add(t)
        # pygame.draw.rect(window, (255, 0, 0), t.rect, 1)
    closed_hatch = For_Level_Building(370, 140, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(370, 140, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl1.append(closed_hatch)
    hatch_lvl1.append(opened_hatch)


def items_level2():
    from levels import item_lvl2, trap_lvl2
    for keys, values in item_lvl2.items():
        i = For_Level_Building(*values)
        i.update()
        collide_group_lvl2.add(i)
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, value in trap_lvl2.items():
        t = For_Level_Building(*value)
        t.update()
        traps_group_lvl2.add(t)
        # pygame.draw.rect(window, (255, 0, 0), t.rect, 1)
    closed_hatch = For_Level_Building(740, 575, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(740, 575, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl2.append(closed_hatch)
    hatch_lvl2.append(opened_hatch)


def items_level3():
    from levels import item_lvl3, trap_lvl3
    for keys, value in item_lvl3.items():
        i = For_Level_Building(*value)
        collide_group_lvl3.add(i)
        i.update()
        # pygame.draw.rect(window, (255, 0, 0), i.rect, 1)
    for keys, value in trap_lvl3.items():
        t = For_Level_Building(*value)
        traps_group_lvl3.add(t)
        t.update()
        # pygame.draw.rect(window, (255, 0, 0), t.rect, 1)
    closed_hatch = For_Level_Building(472, 470, 43, 35, 'images/items/closed_hatch.png')
    opened_hatch = For_Level_Building(472, 470, 43, 35, 'images/items/open_hatch.png')
    hatch_lvl3.append(closed_hatch)
    hatch_lvl3.append(opened_hatch)


# LEVELS
def menu():
    global state, music_volume, game
    window.blit(bg_image, (0, 0))
    music.set_volume(music_volume)
    if state == 'main menu' and state != 'shop':
        if start_button.click(window):
            state = 'level menu'
        elif settings_button.click(window):
            state = 'settings'
        elif store_button.click(window):
            window.blit(bg_image, (0, 0))
            state = 'store'
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
        elif level_2_button.click(window):
            state = 'level 2'
        elif level_3_button.click(window):
            state = 'level 3'
        elif back_button.click(window):
            state = 'main menu'


def store():
    global state
    window.blit(bg_image, (0, 0))
    if back_button.click(window):
        state = 'main menu'
    if armor_button.click(window):
        state = 'armor store'
    elif swords_button.click(window):
        state = 'swords store'
    elif potions_button.click(window):
        state = 'potions store'
    # elif other_button.click(window):
    #     state = 'other store'

    pygame.display.update()
    clock.tick(fps)


#    money = font1.render(": " + str(coins), True, pygame.color.Color('white'))
def tutorial_text():
    howto_walk_fb = font2.render('Press W and S to walk forward and back.', True, pygame.color.Color('white'))
    howto_walk_lr = font2.render('Press A and D to walk left and right.', True, pygame.color.Color('white'))
    # careful = font2.render(f'Walk carefully!' + '\n' + 'The spikes will injure you.', True, pygame.color.Color('white'))
    careful_line1 = font2.render('Walk carefully!', True, pygame.color.Color('white'))
    careful_line2 = font2.render('The spikes will injure you.', True, pygame.color.Color('white'))
    window.blit(howto_walk_fb, (100, 340))
    window.blit(howto_walk_lr, (100, 360))
    window.blit(careful_line1, (700, 370))
    window.blit(careful_line2, (660, 385))


def tutorial():
    window.fill((0, 0, 0))

    floor_tut()
    walls_tut()
    items_tut()
    window.blit(hatch_tut[hatch_num_tut].image, (hatch_tut[hatch_num_tut].rect.x, hatch_tut[hatch_num_tut].rect.y))
    window.blit(portal_tut.image, (portal_tut.rect.x, portal_tut.rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_1():
    window.fill((0, 0, 0))

    floor_level1()
    walls_level1()
    items_level1()
    window.blit(hatch_lvl1[hatch_num_lvl1].image, (hatch_lvl1[hatch_num_lvl1].rect.x, hatch_lvl1[hatch_num_lvl1].rect.y))
    window.blit(portal_lvl1.image, (portal_lvl1.rect.x, portal_lvl1.rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_2():
    window.fill((0, 0, 0))

    floor_level2()
    walls_level2()
    items_level2()
    window.blit(hatch_lvl2[hatch_num_lvl2].image, (hatch_lvl2[hatch_num_lvl2].rect.x, hatch_lvl2[hatch_num_lvl2].rect.y))
    window.blit(portal_lvl2.image, (portal_lvl2.rect.x, portal_lvl2.rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_3():
    window.fill((0, 0, 0))

    floor_level3()
    walls_level3()
    items_level3()
    window.blit(hatch_lvl3[hatch_num_lvl3].image, (hatch_lvl3[hatch_num_lvl3].rect.x, hatch_lvl3[hatch_num_lvl3].rect.y))
    window.blit(portal_lvl3.image, (portal_lvl3.rect.x, portal_lvl3.rect.y))
    pygame.display.update()
    clock.tick(fps)


# SOME FUNCTIONS
def create_coin(*coordinates):
    coins_x = sprite.Group()
    for x, y in coordinates:
        coin_x = Coin(x, y, 20, 20)
        coins_x.add(coin_x)
    return coins_x


def create_showcases(*coordinates):
    showcasess = []
    for x, y in coordinates:
        showcase = For_Level_Building(x, y, 250, 230, 'store_items/showcase.png')
        showcasess.append(showcase)
    return showcasess

# COIN STUFF
w_hatch_collided_tut = False
coins_tut = create_coin((576, 234), (618, 211), (614, 243))
coin_amount_tut = 3
w_hatch_collided_lvl1 = False
coins_lvl1 = create_coin((388, 173), (362, 164), (374, 179), (358, 182))
coin_amount_lvl1 = 4
w_hatch_collided_lvl2 = False
coins_lvl2 = create_coin((749, 560), (788, 577), (737, 615), (766, 590))
coin_amount_lvl2 = 4

# SHOWCASE STUFF
armor_showcases = create_showcases((290, 200), (460, 200))
swords_showcases = create_showcases((125, 200), (290, 200), (460, 200), (625, 200))
potions_showcases = create_showcases((290, 200), (460, 200))


# music.play()
# MAIN CYCLE
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
            sys.exit()
    money = font1.render(": " + str(coins), True, pygame.color.Color('white'))
    # MENU STATE
    if state == 'main menu' or state == 'level menu' or state == 'settings':
        menu()
        player.is_spawned = False
    elif state == 'store':
        store()
    # SHOP STATE
    if state == 'armor store':
        window.blit(bg_image, (0, 0))
        for armor_showcase in armor_showcases:
            armor_showcase.update()
        window.blit(armor, (373, 250))
        window.blit(great_armor, (543, 250))
        if buy_armor_button.click_1(window):
            if coins >= price_num['armor_price_num']:
                player.equip_armor('armor')
                coins -= price_num['armor_price_num']
            else:
                print('Not enough cash')
        if buy_great_armor_button.click_1(window):
            if coins >= price_num['great_armor_price_num']:
                player.equip_armor('great_armor')
                coins -= price_num['great_armor_price_num']
            else:
                print('Not enough cash')
        window.blit(armor_price, (410, 220))
        window.blit(great_armor_price, (580, 220))
    if state == 'swords store':
        window.blit(bg_image, (0, 0))
        for swords_showcase in swords_showcases:
            swords_showcase.update()
        window.blit(great_sword, (207, 250))
        window.blit(axe, (373, 250))
        window.blit(bow, (543, 250))
        window.blit(steel_sword, (707, 250))
        if buy_great_sword_button.click_1(window):
            if coins >= price_num['great_sword_price_num']:
                player.equip_weapon('great_sword')
                coins -= price_num['great_sword_price_num']
            else:
                print('Not enough cash')
        if buy_bow_button.click_1(window):
            if coins >= price_num['axe_price_num']:
                player.equip_weapon('axe')
                coins -= price_num['axe_price_num']
            else:
                print('Not enough cash')
        if buy_axe_button.click_1(window):
            if coins >= price_num['bow_price_num']:
                player.equip_weapon('bow')
                coins -= price_num['bow_price_num']
            else:
                print('Not enough cash')
        if buy_steel_sword_button.click_1(window):
            if coins >= price_num['steel_sword_price_num']:
                player.equip_weapon('steel_sword')
                coins -= price_num['steel_sword_price_num']
            else:
                print('Not enough cash')
        window.blit(great_sword_price, (245, 220))
        window.blit(axe_price, (410, 220))
        window.blit(bow_price, (580, 220))
        window.blit(steel_sword_price, (745, 220))
    if state == 'potions store':
        window.blit(bg_image, (0, 0))
        for potions_showcase in potions_showcases:
            potions_showcase.update()
        window.blit(health_potion, (380, 250))
        window.blit(energy_potion, (555, 250))
        if buy_health_potion_button.click_1(window):
            if lives < 5:
                if coins >= price_num['health_potion_price_num'][0]:
                    lives += price_num['health_potion_price_num'][1]
                    coins -= price_num['health_potion_price_num'][0]
                else:
                    print('Not enough cash')
        if buy_energy_potion_button.click_1(window):
            if energy < 5:
                if coins >= price_num['energy_potion_price_num'][0]:
                    lives += price_num['energy_potion_price_num'][1]
                    coins -= price_num['energy_potion_price_num'][0]
                else:
                    print('Not enough cash')
        window.blit(health_potion_price, (415, 220))
        window.blit(energy_potion_price, (585, 220))
    if state == 'armor store' or state == 'swords store' or state == 'potions store':
        if back_button.click(window):
            state = 'main menu'
        if armor_button.click(window):
            state = 'armor store'
        elif swords_button.click(window):
            state = 'swords store'
        elif potions_button.click(window):
            state = 'potions store'
    # LEVELS STATE
    if state == 'tutorial':
        tutorial()
        tutorial_text()
        player.spawn(130, 550)
        player.trap(traps_group_tut)
        player.collide(collide_group_tut)
        if player.rect.colliderect(hatch_tut[0]):
            w_hatch_collided_tut = True
            hatch_num_tut = 1
        if w_hatch_collided_tut:
            for coin in coins_tut:
                coin.update()
                coin.draw(window)
                if player.rect.colliderect(coin.rect):
                    collect_coin_sound.play()
                    coin.kill()
                    coin_amount_tut -= 1
                    coins += 1
                elif coin_amount_tut == 0:
                    w_hatch_collided_tut = False
        if player.rect.colliderect(portal_tut.rect):
            player.spawn(860, 460)
            state = 'level 1'
    if state == 'level 1':
        level_1()
        player.spawn(860, 460)
        player.trap(traps_group_lvl1)
        player.collide(collide_group_lvl1)
        if player.rect.colliderect(hatch_lvl1[0]):
            w_hatch_collided_lvl1 = True
            hatch_num_lvl1 = 1
        if w_hatch_collided_lvl1:
            for coin in coins_lvl1:
                coin.update()
                coin.draw(window)
                if player.rect.colliderect(coin.rect):
                    collect_coin_sound.play()
                    coin.kill()
                    coin_amount_lvl1 -= 1
                    coins += 1
                elif coin_amount_lvl1 == 0:
                    w_hatch_collided_lvl1 = False
        if player.rect.colliderect(portal_lvl1.rect):
            player.spawn(210, 590)
            state = 'level 2'
    if state == 'level 2':
        level_2()
        player.spawn(210, 590)
        player.trap(traps_group_lvl2)
        player.collide(collide_group_lvl2)
        if player.rect.colliderect(hatch_lvl2[0]):
            w_hatch_collided_lvl2 = True
            hatch_num_lvl2 = 1
        if w_hatch_collided_lvl2:
            for coin in coins_lvl2:
                coin.update()
                coin.draw(window)
                if player.rect.colliderect(coin.rect):
                    collect_coin_sound.play()
                    coin.kill()
                    coin_amount_lvl2 -= 1
                    coins += 1
                elif coin_amount_lvl2 == 0:
                    w_hatch_collided_lvl2 = False
        if player.rect.colliderect(portal_lvl2.rect):
            player.spawn(480, 120)
            state = 'level 3'
    if state == 'level 3':
        level_3()
        player.spawn(480, 120)
        player.trap(traps_group_lvl3)
        player.collide(collide_group_lvl3)
    if state == 'tutorial' or state == 'level 1' or state == 'level 2' or state == 'level 3':
        if not finished:
            all_sprites.update()  # Обновление всех спрайтов
        all_sprites.draw(window)  # Отображение всех спрайтов
    if state == 'tutorial' or state == 'level 1' or state == 'level 2' or state == 'level 3' or state == 'store' or state == 'armor store' or state == 'swords store' or state == 'potions store':
        window.blit(lives_list[lives], (10, 0))
        window.blit(energy_list[energy], (120, 24))
        window.blit(money, (255, 20))
        if home_button.click(window):
            state = 'level menu'

    if state == 'tutorial':
        goblin.show(window)
        goblin.update(player.rect, lives, target_x=player.rect.x, x=422)
        goblin.collide(collide_group_tut)
    if state == 'level 3':
        boss.show(window)
        boss.update(player, player.rect.y, 345)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    text = font1.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))
    window.blit(text, (10, 680))

    pygame.display.update()
    clock.tick(fps)