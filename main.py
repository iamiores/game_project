import sys
import pygame.color
from coin import Coin
from button import *
from building import *
from downloads import *
import math
from random import randint
pygame.init()

'''CLASSES'''


class Goblin(sprite.Sprite):
    # CONSTRUCTOR
    def __init__(self, goblin_image, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(pygame.image.load(goblin_image), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height
        self.speed = randint(3, 6)
        self.counter_idle = 0
        self.counter_right = 0
        self.counter_left = 0
        self.counter_attack_right = 0
        self.counter_attack_left = 0
        self.direction = 'right'
        self.health = 20
        self.follow = False
        self.attack_range = 10
        self.attack_power_num = 1
        self.attack_power = self.attack_power_num
        self.attacks = False
        self.is_hitbox_active = False

        self.pics_idle = ['images/monsters/goblin/goblin_idle_right_1.png', 'images/monsters/goblin/goblin_idle_right_2.png', 'images/monsters/goblin/goblin_idle_right_3.png', 'images/monsters/goblin/goblin_idle_right_4.png']
        self.pics_idle_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_idle]

        self.pics_attack_right = ['images/monsters/goblin/goblin_attack_right_1.png', 'images/monsters/goblin/goblin_attack_right_2.png', 'images/monsters/goblin/goblin_attack_right_3.png', 'images/monsters/goblin/goblin_attack_right_4.png']
        self.pics_attack_right_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_attack_right]

        self.pics_attack_left = ['images/monsters/goblin/goblin_attack_left_1.png', 'images/monsters/goblin/goblin_attack_left_2.png', 'images/monsters/goblin/goblin_attack_left_3.png', 'images/monsters/goblin/goblin_attack_left_4.png']
        self.pics_attack_left_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_attack_left]

        self.pics_right = ['images/monsters/goblin/goblin_walk_right_1.png', 'images/monsters/goblin/goblin_walk_right_2.png', 'images/monsters/goblin/goblin_walk_right_3.png']
        self.pics_right_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_right]

        self.pics_left = ['images/monsters/goblin/goblin_walk_left_1.png', 'images/monsters/goblin/goblin_walk_left_2.png', 'images/monsters/goblin/goblin_walk_left_3.png']
        self.pics_left_obj = [transform.scale(pygame.image.load(pic), (self.width, self.height)) for pic in self.pics_left]

    # ANIMATED FRAMES FOR MOVEMENT
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
                self.is_hitbox_active = False
            elif 5 <= self.counter_attack_right < 10:
                self.image = self.pics_attack_right_obj[1]
                self.is_hitbox_active = False
            elif 10 <= self.counter_attack_right < 15:
                self.image = self.pics_attack_right_obj[2]
                self.is_hitbox_active = False
            elif 15 <= self.counter_attack_right < 20:
                self.image = self.pics_attack_right_obj[3]
                self.is_hitbox_active = True
            elif self.counter_attack_right == 20:
                self.counter_attack_right = 0
                # lives -= self.attack_power
        else:
            self.counter_attack_right = 0

        if kind == 'attack left':
            self.counter_attack_left += 1
            if self.counter_attack_left < 5:
                self.image = self.pics_attack_left_obj[0]
                self.is_hitbox_active = False
            elif 5 <= self.counter_attack_left < 10:
                self.image = self.pics_attack_left_obj[1]
                self.is_hitbox_active = False
            elif 10 <= self.counter_attack_left < 15:
                self.image = self.pics_attack_left_obj[2]
                self.is_hitbox_active = False
            elif 15 <= self.counter_attack_left < 20:
                self.image = self.pics_attack_left_obj[3]
                self.is_hitbox_active = True
            elif self.counter_attack_left == 20:
                self.counter_attack_left = 0
                # lives -= self.attack_power
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

        if self.attacks:
            self.speed = 2
        else:
            self.speed = randint(3, 6)

    # COLLIDE WITH OBJECTS
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

    # MOVEMENT
    def update(self, target, target_y=None, target_x=None, start_x=None, end_x=None, start_y=None, end_y=None):
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery

        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist
        self.target_x = target_x if target_x is not None else float('-inf')
        self.target_y = target_y if target_y is not None else float('-inf')
        self.end_x = end_x if end_x is not None else float('inf')
        self.start_x = start_x if start_x is not None else float('inf')
        self.start_y = start_y if start_y is not None else float('inf')
        self.end_y = end_y if end_y is not None else float('inf')
        if dx > 0:
            self.direction = 'right'
        if dx < 0:
            self.direction = 'left'
        if self.follow:
            if self.direction == 'right':
                if dist <= self.attack_range:
                    self.attacks = True
                    self.animate('attack right')
                else:
                    self.attacks = False
                    self.animate('right')
                self.rect.x += dx * self.speed
                if dy > 0:
                    self.animate('right')
                    self.rect.y += dy * self.speed
                elif dy < 0:
                    self.animate('right')
                    self.rect.y += dy * self.speed

            if self.direction == 'left':
                if dist <= self.attack_range:
                    self.attacks = True
                    self.animate('attack left')
                else:
                    self.attacks = False
                    self.animate('left')
                self.rect.x += dx * self.speed
                if dy > 0:
                    self.animate('left')
                    self.rect.y += dy * self.speed
                elif dy < 0:
                    self.animate('left')
                    self.rect.y += dy * self.speed
        else:
            self.animate('stay')

    # SHOW ON SCREEN
    def show(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Boss(sprite.Sprite):
    # CONSTRUCTOR
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
        self.health = 80
        self.dead = False
        self.attack_power_num = 3
        self.attack_power = self.attack_power_num
        self.attacks = False
        self.is_hitbox_active = False
        self.was_roar = False

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

    # ANIMATED FRAMES FOR MOVEMENT
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
                self.is_hitbox_active = False
            elif 5 <= self.counter_attack_right < 10:
                self.image = self.pics_attack_right_obj[1]
                self.is_hitbox_active = False
            elif 10 <= self.counter_attack_right < 15:
                self.image = self.pics_attack_right_obj[2]
                self.is_hitbox_active = False
            elif 15 <= self.counter_attack_right < 20:
                self.image = self.pics_attack_right_obj[3]
                print('boss attacked!!!!!!!!!1', self.counter_attack_right)
                self.is_hitbox_active = True
            elif self.counter_attack_right == 20:
                self.counter_attack_right = 0
        else:
            self.counter_attack_right = 0

        if kind == 'attack left':
            self.counter_attack_left += 1
            if self.counter_attack_left < 5:
                self.image = self.pics_attack_left_obj[0]
                self.is_hitbox_active = False
            elif 5 <= self.counter_attack_left < 10:
                self.image = self.pics_attack_left_obj[1]
                self.is_hitbox_active = False
            elif 10 <= self.counter_attack_left < 15:
                self.image = self.pics_attack_left_obj[2]
                self.is_hitbox_active = False
            elif 15 <= self.counter_attack_left < 20:
                self.image = self.pics_attack_left_obj[3]
                self.is_hitbox_active = True

            elif self.counter_attack_left == 20:
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

        if self.attacks:
            self.speed = 2

        else:
            self.speed = 5

    # MOVEMENT
    def update(self, target, target_y, y):
        if target_y >= y:
            if not self.was_roar:
                boss_sound.play()
                self.was_roar = True
            if self.direction == 'left':
                if self.rect.colliderect(target.rect):
                    self.attacks = True
                    self.animate('attack left')
                else:
                    self.attacks = False
                    self.animate('left')
                self.rect.x -= self.speed
                if self.rect.x <= 340:
                    self.direction = 'right'
            elif self.direction == 'right':
                if self.rect.colliderect(target.rect):
                    self.attacks = True
                    self.animate('attack right')
                else:
                    self.attacks = False
                    self.animate('right')
                self.rect.x += self.speed
                if self.rect.x >= 610:
                    self.direction = 'left'
        else:
            self.animate('stay')
            self.was_roar = False

    # SHOW ON SCREEN
    def show(self, screen):
        if not self.dead:
            screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(sprite.Sprite):
    # CONSTRUCTOR
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
        self.attacking = False
        self.defending = False
        self.timer_attack = 0
        self.timer_defend = 0
        self.attack_amount = 0
        self.was_attacked_once = False

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

    # ANIMATED FRAMES FOR MOVEMENT
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

    # MOVEMENT
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

    # SET SPAWN COORDINATES
    def spawn(self, x, y):
        if not self.is_spawned:
            self.rect.x = x
            self.rect.y = y
            self.is_spawned = True

    # COLLIDE WITH OBJECTS
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

    # TRAPS REACTION
    def trap(self, group):
        global lives
        if not self.was_colliding:
            if any(self.rect.colliderect(group.rect) for group in group):
                lives -= 1
                self.was_colliding = True
        elif not any(self.rect.colliderect(group.rect) for group in group):
            self.was_colliding = False

    # EQUIP ARMOR
    def equip_armor(self, armor_name):
        self.armor = armor_name
        print(self.armor)

    # EQUIP WEAPON
    def equip_weapon(self, weapon_name):
        self.weapon = weapon_name
        print(self.weapon)

    # ATTACK FUNCTION
    def attack(self, monster):
        attack_properties = WEAPON_TABLE.get(self.weapon)
        attack_power = attack_properties
        if self.rect.colliderect(monster.rect) and not self.attacking:
            self.attacking = True
            monster.health -= attack_power
            hit_sound.play()
            print(f"You dealt {attack_power} damage to the target!")
            print(monster.health)

        if self.attacking:
            self.timer_attack += 1
            if self.timer_attack >= 20:
                self.attacking = False
                self.timer_attack = 0

    # DEFENCE FUNCTION
    def defend(self, monster):
        global lives
        defense_properties = ARMOR_TABLE.get(self.armor)
        defense_power = defense_properties
        damage = max(monster.attack_power - defense_power, 0)
        if self.rect.colliderect(monster.rect) and monster.attacks:
            if monster.is_hitbox_active and not self.was_attacked_once:
                lives -= damage
                print(f"{self.armor} provides defense against the monster!")
                self.was_attacked_once = True
            if not monster.is_hitbox_active:
                self.was_attacked_once = False


# WEAPONS
WEAPON_TABLE = {
    "no_weapon": 2,
    "knife": 5,
    "great_sword": 10,
    "steel_sword": 20,
    "axe": 12
}

# ARMORS
ARMOR_TABLE = {
    "no_armor": 0,
    "armor": 1,
    "great_armor": 2
}

'''FONTS'''
font1 = pygame.font.Font('fonts/Retro Gaming.ttf', 20)
font2 = pygame.font.Font('fonts/Retro Gaming.ttf', 14)

'''SETTINGS'''
w_width, w_height = 1000, 700
window = pygame.display.set_mode((w_width, w_height))
clock = pygame.time.Clock()
fps = 60
game = True
bg_image = transform.scale(pygame.image.load('images/bg.png'), (w_width, w_height))
pygame.display.set_caption('Roguelike')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
state = 'main menu'

'''ALTERNATES'''
lives = 5
energy = 5
coins = 0

# BOOL ALTERNATE
finished = False

victory_tut = False
defeat_tut = False
victory_lvl1 = False
defeat_lvl1 = False
victory_lvl2 = False
defeat_lvl2 = False
victory_lvl3 = False
defeat_lvl3 = False

# COUNTERS
kill_tut = 0
kill_lvl1 = 0
kill_lvl2 = 0
kill_lvl3 = 0
hatch_num_tut = 0
hatch_num_lvl1 = 0
hatch_num_lvl2 = 0
hatch_num_lvl3 = 0

'''GROUPS AND LISTS'''
lives_list = [live_0, live_1, live_2, live_3, live_4, live_5]
energy_list = [energy_0, energy_1, energy_2, energy_3, energy_4, energy_5]

all_sprites = sprite.Group()
coin_group = sprite.Group()
boss_group = sprite.Group()

'''STORE STUFF'''
price_num = {
    'armor_price_num': 2,
    'great_armor_price_num': 4,
    'great_sword_price_num': 2,
    'steel_sword_price_num': 6,
    'knife_price_num': 1,
    'axe_price_num': 3,
    'health_potion_price_num': [1, 1],
    'energy_potion_price_num': [1, 2]
}

armor_price = font1.render(str(price_num['armor_price_num']), True, pygame.color.Color('white'))
great_armor_price = font1.render(str(price_num['great_armor_price_num']), True, pygame.color.Color('white'))
great_sword_price = font1.render(str(price_num['great_sword_price_num']), True, pygame.color.Color('white'))
steel_sword_price = font1.render(str(price_num['steel_sword_price_num']), True, pygame.color.Color('white'))
knife_price = font1.render(str(price_num['knife_price_num']), True, pygame.color.Color('white'))
axe_price = font1.render(str(price_num['axe_price_num']), True, pygame.color.Color('white'))
health_potion_price = font1.render(str(price_num['health_potion_price_num'][0]), True, pygame.color.Color('white'))
energy_potion_price = font1.render(str(price_num['energy_potion_price_num'][0]), True, pygame.color.Color('white'))


'''CREATE OBJECTS'''
coin = Coin(x=240, y=33, width=27, height=27)
coin_in_store = Coin(x=240, y=33, width=27, height=27)
player = Player('images/player/male/male_WalkBack_1.png', 490, 133, 10, 28, 33)
player.equip_weapon('no_weapon')
player.equip_armor('no_armor')
boss = Boss('images/monsters/boss/boss_idle_left_1.png', 465, 500, 50, 60)
boss_group.add(boss)
coin_group.add(coin_in_store)
all_sprites.add(coin)
all_sprites.add(player)

'''SOUNDS & MUSIC'''
music = pygame.mixer.Sound('music/Crystal Caves v1_2.mp3')
collect_coin_sound = pygame.mixer.Sound('sounds/coin_collect.wav')
goblin_death_sound = pygame.mixer.Sound('sounds/goblin.mp3')
hit_sound = pygame.mixer.Sound('sounds/hit.mp3')
boss_sound = pygame.mixer.Sound('sounds/monster.mp3')

boss_sound.set_volume(0.1)
goblin_death_sound.set_volume(0.5)
hit_sound.set_volume(0.5)
music_volume = 0.4

'''MENU'''


def menu():
    global state, music_volume, game
    window.blit(bg_image, (0, 0))
    music.set_volume(music_volume)
    if state == 'main menu' and state != 'shop':
        if start_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'level menu'
        elif settings_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'settings'
        elif store_button.click(window, (41, 47, 75), (21, 24, 38)):
            window.blit(bg_image, (0, 0))
            state = 'store'
        elif exit_button.click(window, (41, 47, 75), (21, 24, 38)):
            game = False
            sys.exit()
    if state == 'settings':
        if add_volume_button.click(window, (41, 47, 75), (21, 24, 38)):
            music_volume += 0.1
        elif reduce_volume_button.click(window, (41, 47, 75), (21, 24, 38)):
            music_volume -= 0.1
        elif back_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'main menu'
    if state == 'level menu':
        if tutorial_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'tutorial'
        elif level_1_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'level 1'
        elif level_2_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'level 2'
        elif level_3_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'level 3'
        elif back_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'main menu'

'''STORE'''


def store():
    global state
    window.blit(bg_image, (0, 0))
    if back_button.click(window, (41, 47, 75), (21, 24, 38)):
        state = 'main menu'
    if armor_button.click(window, (41, 47, 75), (21, 24, 38)):
        state = 'armor store'
    elif swords_button.click(window, (41, 47, 75), (21, 24, 38)):
        state = 'swords store'
    elif potions_button.click(window, (41, 47, 75), (21, 24, 38)):
        state = 'potions store'
    # elif other_button.click(window):
    #     state = 'other store'

    pygame.display.update()
    clock.tick(fps)

'''LEVELS'''


def tutorial(screen):
    screen.fill((0, 0, 0))

    floor_tut(screen=screen)
    walls_tut(screen=screen)
    items_tut(screen=screen)
    screen.blit(hatch_tut[hatch_num_tut].image, (hatch_tut[hatch_num_tut].rect.x, hatch_tut[hatch_num_tut].rect.y))
    screen.blit(portal_tut.image, (portal_tut.rect.x, portal_tut.rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_1(screen):
    screen.fill((0, 0, 0))

    floor_level1(screen=screen)
    walls_level1(screen=screen)
    items_level1(screen=screen)
    screen.blit(hatch_lvl1[hatch_num_lvl1].image, (hatch_lvl1[hatch_num_lvl1].rect.x, hatch_lvl1[hatch_num_lvl1].rect.y))
    screen.blit(portal_lvl1.image, (portal_lvl1.rect.x, portal_lvl1.rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_2(screen):
    screen.fill((0, 0, 0))

    floor_level2(screen=screen)
    walls_level2(screen=screen)
    items_level2(screen=screen)
    screen.blit(hatch_lvl2[hatch_num_lvl2].image, (hatch_lvl2[hatch_num_lvl2].rect.x, hatch_lvl2[hatch_num_lvl2].rect.y))
    screen.blit(portal_lvl2.image, (portal_lvl2.rect.x, portal_lvl2.rect.y))
    pygame.display.update()
    clock.tick(fps)


def level_3(screen):
    screen.fill((0, 0, 0))

    floor_level3(screen=screen)
    walls_level3(screen=screen)
    items_level3(screen=screen)
    screen.blit(hatch_lvl3[hatch_num_lvl3].image, (hatch_lvl3[hatch_num_lvl3].rect.x, hatch_lvl3[hatch_num_lvl3].rect.y))
    screen.blit(portal_lvl3.image, (portal_lvl3.rect.x, portal_lvl3.rect.y))
    pygame.display.update()
    clock.tick(fps)


# TUTORIAL TIPS

def tutorial_text():
    howto_walk_fb = font2.render('Press W and S to walk forward and back.', True, pygame.color.Color('white'))
    howto_walk_lr = font2.render('Press A and D to walk left and right.', True, pygame.color.Color('white'))
    careful_line1 = font2.render('Walk carefully!', True, pygame.color.Color('white'))
    careful_line2 = font2.render('The spikes will injure you.', True, pygame.color.Color('white'))
    window.blit(howto_walk_fb, (100, 340))
    window.blit(howto_walk_lr, (100, 360))
    window.blit(careful_line1, (700, 370))
    window.blit(careful_line2, (660, 385))


# COORDINATES FOR PLAYER SPAWN
tut_x, tut_y = 130, 550
lvl1_x, lvl1_y = 860, 460
lvl2_x, lvl2_y = 210, 590
lvl3_x, lvl3_y = 480, 120


'''RESET'''


def reset_tutorial():
    global hatch_num_tut, coins, kill_tut, lives, energy, w_hatch_collided_tut, coin_amount_tut, finished, goblins_tut, tut_x, tut_y
    goblins_tut = goblins((695, 520), (605, 490), (665, 640))
    finished = False
    player.spawn(tut_x, tut_y)
    hatch_num_tut = 0
    kill_tut = 0
    energy = 5
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
    for goblin_x in goblins_tut:
        goblin_x.update(target=player, target_x=player.rect.x, target_y=player.rect.y, start_x=420, end_y=440)
        if goblin_x.target_x >= goblin_x.start_x:
            goblin_x.follow = True
        if goblin_x.target_y <= goblin_x.end_y:
            goblin_x.follow = False
        goblin_x.collide(collide_group_tut)
        goblin_x.show(window)


def reset_lvl1():
    global hatch_num_lvl1, coins, kill_lvl1, lives, energy, w_hatch_collided_lvl1, coin_amount_lvl1, finished, goblins_lvl1_1, goblins_lvl1_2, lvl1_x, lvl1_y
    goblins_lvl1_1 = goblins((507, 392), (440, 438))
    goblins_lvl1_2 = goblins((932, 175), (780, 80), (732, 112))
    player.spawn(lvl1_x, lvl1_y)
    finished = False
    hatch_num_lvl1 = 0
    kill_lvl1 = 0
    energy = 5
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
    for goblin_x in goblins_lvl1_1:
        goblin_x.update(target=player, target_x=player.rect.x, start_x=600)
        if goblin_x.target_x <= goblin_x.start_x:
            goblin_x.follow = True
        else:
            goblin_x.follow = False
        goblin_x.collide(collide_group_lvl1)
        goblin_x.show(window)
    for goblin_x in goblins_lvl1_2:
        goblin_x.update(target=player, target_x=player.rect.x, target_y=player.rect.y, start_y=270, end_x=630)
        if goblin_x.target_y <= goblin_x.start_y:
            goblin_x.follow = True
        if goblin_x.target_x <= goblin_x.end_x or goblin_x.target_y >= goblin_x.start_y:
            goblin_x.follow = False
        goblin_x.collide(collide_group_lvl1)
        goblin_x.show(window)


def reset_lvl2():
    global hatch_num_lvl2, coins, kill_lvl2, lives, energy, w_hatch_collided_lvl2, coin_amount_lvl2, finished, goblins_lvl2_1, goblins_lvl2_2, lvl2_x, lvl2_y
    goblins_lvl2_1 = goblins((352, 250), (293, 303), (125, 262))
    goblins_lvl2_2 = goblins((860, 237), (717, 275))
    player.spawn(lvl2_x, lvl2_y)
    finished = False
    hatch_num_lvl2 = 0
    kill_lvl2 = 0
    energy = 5
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
    for goblin_x in goblins_lvl2_1:
        goblin_x.update(target=player, target_x=player.rect.x, target_y=player.rect.y, start_y=370, end_x=430)
        if goblin_x.target_y <= goblin_x.start_y:
            goblin_x.follow = True
        if goblin_x.target_x >= goblin_x.end_x or goblin_x.target_y >= goblin_x.start_y:
            goblin_x.follow = False
        goblin_x.collide(collide_group_lvl2)
        goblin_x.show(window)
    for goblin_x in goblins_lvl2_2:
        goblin_x.update(target=player, target_x=player.rect.x, target_y=player.rect.y, start_x=555, end_y=370)
        if goblin_x.target_x >= goblin_x.start_x:
            goblin_x.follow = True
        if goblin_x.target_y >= goblin_x.end_y or goblin_x.target_x <= goblin_x.start_x:
            goblin_x.follow = False
        goblin_x.collide(collide_group_lvl2)
        goblin_x.show(window)


def reset_lvl3():
    global hatch_num_lvl3, coins, kill_lvl3, lives, energy, w_hatch_collided_lvl3, coin_amount_lvl3, finished, lvl3_x, lvl3_y
    player.spawn(lvl3_x, lvl3_y)
    player.trap(traps_group_lvl3)
    player.collide(collide_group_lvl3)
    boss.show(window)
    boss.update(player, player.rect.y, 345)
    finished = False
    hatch_num_lvl3 = 0
    kill_lvl3 = 0
    energy = 5
    if boss.health == 0:
        if player.rect.colliderect(hatch_lvl3[0]):
            w_hatch_collided_lvl3 = True
            hatch_num_lvl3 = 1
        if w_hatch_collided_lvl3:
            for coin in coins_lvl3:
                coin.update()
                coin.draw(window)
                if player.rect.colliderect(coin.rect):
                    collect_coin_sound.play()
                    coin.kill()
                    coin_amount_lvl3 -= 1
                    coins += 1
                elif coin_amount_lvl3 == 0:
                    w_hatch_collided_lvl3 = False


'''OTHER FUNCTIONS'''


def create_coin(*coordinates):
    coins_x = sprite.Group()
    for x, y in coordinates:
        coin_x = Coin(x, y, 20, 20)
        coins_x.add(coin_x)
    return coins_x


def goblins(*coordinates):
    goblins_x = sprite.Group()
    for x, y in coordinates:
        goblin = Goblin('images/monsters/goblin/goblin_idle_right_1.png', x, y, 30, 35)
        goblins_x.add(goblin)
    return goblins_x


def create_showcases(*coordinates):
    showcases_x = []
    for x, y in coordinates:
        showcase = For_Level_Building(x, y, 250, 230, 'store_items/showcase.png')
        showcases_x.append(showcase)
    return showcases_x


def next_level(kind, killed, in_all, coin_amount):
    global finished, state
    window.blit(black_scr, (0, 0))
    coin_n = Coin(540, 312, 27, 27)
    mid_kills = in_all // 2

    if kind == 'defeat':
        if killed < mid_kills:
            window.blit(one_star, (472, 225))
        elif killed == mid_kills:
            window.blit(one_star, (512, 225))
            window.blit(one_star, (442, 225))
        elif killed > mid_kills:
            window.blit(one_star, (472, 225))
            window.blit(one_star, (412, 225))
            window.blit(one_star, (532, 225))
        window.blit(defeat_flag, (420, 140))
    elif kind == 'victory':
        if killed < mid_kills:
            window.blit(one_star, (472, 225))
        elif killed == mid_kills:
            window.blit(one_star, (512, 225))
            window.blit(one_star, (442, 225))
        elif killed > mid_kills:
            window.blit(one_star, (472, 225))
            window.blit(one_star, (412, 225))
            window.blit(one_star, (532, 225))
        window.blit(victory_flag, (420, 140))
    coin_n.draw(window)
    coin_n.update()
    window.blit(skull_killed, (415, 300))
    coins_end = font1.render(': ' + str(coin_amount), True, pygame.color.Color('white'))
    killed_end = font1.render(': ' + str(killed) + '/' + str(in_all), True, pygame.color.Color('white'))
    window.blit(coins_end, (555, 300))
    window.blit(killed_end, (452, 300))


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
w_hatch_collided_lvl3 = False
coins_lvl3 = create_coin((465, 470), (500, 455), (515, 475), (493, 507))
coin_amount_lvl3 = 4

# SHOWCASE STUFF
armor_showcases = create_showcases((290, 200), (460, 200))
swords_showcases = create_showcases((125, 200), (290, 200), (460, 200), (625, 200))
potions_showcases = create_showcases((290, 200), (460, 200))

# GOBLINS STUFF
goblins_tut = goblins((695, 520), (605, 490), (665, 640))
goblins_lvl1_1 = goblins((507, 392), (440, 438))
goblins_lvl1_2 = goblins((932, 175), (780, 80), (732, 112))
goblins_lvl2_1 = goblins((352, 250), (293, 303), (125, 262))
goblins_lvl2_2 = goblins((860, 237), (717, 275))


# music.play()
'''GAME CYCLE'''


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
            armor_showcase.update(screen=window)
        window.blit(armor, (373, 250))
        window.blit(great_armor, (543, 250))
        if buy_armor_button.click(window, (51, 63, 92), (41, 47, 75)):
            if coins >= price_num['armor_price_num']:
                player.equip_armor('armor')
                coins -= price_num['armor_price_num']
            else:
                print('Not enough cash')
        if buy_great_armor_button.click(window, (51, 63, 92), (41, 47, 75)):
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
            swords_showcase.update(screen=window)
        window.blit(great_sword, (207, 250))
        window.blit(axe, (373, 250))
        window.blit(knife, (543, 250))
        window.blit(steel_sword, (707, 250))
        if buy_great_sword_button.click(window, (51, 63, 92), (41, 47, 75)):
            if coins >= price_num['great_sword_price_num']:
                player.equip_weapon('great_sword')
                coins -= price_num['great_sword_price_num']
            else:
                print('Not enough cash')
        if buy_knife_button.click(window, (51, 63, 92), (41, 47, 75)):
            if coins >= price_num['axe_price_num']:
                player.equip_weapon('axe')
                coins -= price_num['axe_price_num']
            else:
                print('Not enough cash')
        if buy_axe_button.click(window, (51, 63, 92), (41, 47, 75)):
            if coins >= price_num['knife_price_num']:
                player.equip_weapon('knife')
                coins -= price_num['knife_price_num']
            else:
                print('Not enough cash')
        if buy_steel_sword_button.click(window, (51, 63, 92), (41, 47, 75)):
            if coins >= price_num['steel_sword_price_num']:
                player.equip_weapon('steel_sword')
                coins -= price_num['steel_sword_price_num']
            else:
                print('Not enough cash')
        window.blit(great_sword_price, (245, 220))
        window.blit(axe_price, (410, 220))
        window.blit(knife_price, (580, 220))
        window.blit(steel_sword_price, (745, 220))
    if state == 'potions store':
        window.blit(bg_image, (0, 0))
        for potions_showcase in potions_showcases:
            potions_showcase.update(screen=window)
        window.blit(health_potion, (385, 250))
        window.blit(energy_potion, (555, 250))
        if buy_health_potion_button.click(window, (51, 63, 92), (41, 47, 75)):
            if lives < 5:
                if coins >= price_num['health_potion_price_num'][0]:
                    lives += price_num['health_potion_price_num'][1]
                    coins -= price_num['health_potion_price_num'][0]
                else:
                    print('Not enough cash')
        if buy_energy_potion_button.click_(window, (51, 63, 92), (41, 47, 75)):
            if energy < 5:
                if coins >= price_num['energy_potion_price_num'][0]:
                    energy += price_num['energy_potion_price_num'][1]
                    coins -= price_num['energy_potion_price_num'][0]
                else:
                    print('Not enough cash')
        window.blit(health_potion_price, (415, 220))
        window.blit(energy_potion_price, (585, 220))
    if state == 'store' or state == 'armor store' or state == 'swords store' or state == 'potions store':
        coin_group.draw(window)
        coin_group.update()
        if back_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'main menu'
        if armor_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'armor store'
        elif swords_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'swords store'
        elif potions_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'potions store'

    # LEVELS STATE
    if state == 'tutorial':
        if victory_tut:
            finished = True
            next_level('victory', kill_tut, 3, coins)
            if menu_button.click(window, (41, 47, 75), (21, 24, 38)):
                state = 'main menu'
                finished = False
                reset_tutorial()
            elif retry_button_1.click(window, (41, 47, 75), (21, 24, 38)):
                reset_tutorial()
                coins = 0
                lives = 5
                finished = False
                victory_tut = False
                state = 'level menu'
            elif next_button.click(window, (41, 47, 75), (21, 24, 38)):
                finished = False
                player.spawn(lvl1_x, lvl1_y)
                state = 'level menu'
        if defeat_tut:
            finished = True
            next_level('defeat', kill_tut, 3, coins)
            if menu_button.click(window, (41, 47, 75), (21, 24, 38)):
                state = 'main menu'
                finished = False
                reset_tutorial()
            elif retry_button_2.click(window, (41, 47, 75), (21, 24, 38)):
                reset_tutorial()
                lives = 5
                coins = 0
                finished = False
                defeat_tut = False
        if lives != 0:
            if not finished:
                tutorial(window)
                tutorial_text()
                player.spawn(tut_x, tut_y)
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
                for goblin_x in goblins_tut:
                    goblin_x.update(target=player, target_x=player.rect.x, target_y=player.rect.y, start_x=420, end_y=440)
                    if goblin_x.target_x >= goblin_x.start_x:
                        goblin_x.follow = True
                    if goblin_x.target_y <= goblin_x.end_y or goblin_x.target_x <= goblin_x.start_x:
                        goblin_x.follow = False
                    player.attack(goblin_x)
                    if goblin_x.health <= 0:
                        goblin_x.kill()
                        goblin_death_sound.play()
                        kill_tut += 1
                    player.defend(goblin_x)
                    goblin_x.collide(collide_group_tut)
                    goblin_x.show(window)
                if player.rect.colliderect(portal_tut.rect):
                    victory_tut = True
                if lives <= 0:
                    defeat_tut = True

    if state == 'level 1':
        if victory_lvl1:
            finished = True
            next_level('victory', kill_lvl1, 5, coins)
            if menu_button.click(window, (41, 47, 75), (21, 24, 38)):
                state = 'main menu'
                finished = False
                reset_lvl1()
            elif retry_button_1.click(window, (41, 47, 75), (21, 24, 38)):
                reset_lvl1()
                coins = 0
                lives = 5
                state = 'level menu'
                finished = False
                victory_lvl1 = False
            elif next_button.click(window, (41, 47, 75), (21, 24, 38)):
                finished = False
                player.spawn(lvl2_x, lvl2_y)
                state = 'level menu'
        if defeat_lvl1:
            finished = True
            next_level('defeat', kill_lvl1, 5, coins)
            if menu_button.click(window, (41, 47, 75), (21, 24, 38)):
                state = 'main menu'
                finished = False
                reset_lvl1()
            elif retry_button_2.click(window, (41, 47, 75), (21, 24, 38)):
                reset_lvl1()
                coins = 0
                lives = 5
                finished = False
                defeat_lvl1 = False
        if lives != 0:
            if not finished:
                level_1(window)
                player.spawn(lvl1_x, lvl1_y)
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
                for goblin_x in goblins_lvl1_1:
                    goblin_x.update(target=player, target_x=player.rect.x, start_x=600)
                    if goblin_x.target_x <= goblin_x.start_x:
                        goblin_x.follow = True
                    else:
                        goblin_x.follow = False
                    player.attack(goblin_x)
                    if goblin_x.health <= 0:
                        goblin_x.kill()
                        goblin_death_sound.play()
                        kill_lvl1 += 1
                    player.defend(goblin_x)
                    goblin_x.collide(collide_group_lvl1)
                    goblin_x.show(window)
                for goblin_x in goblins_lvl1_2:
                    goblin_x.update(target=player, target_x=player.rect.x, target_y=player.rect.y, start_y=270, end_x=630)
                    if goblin_x.target_y <= goblin_x.start_y:
                        goblin_x.follow = True
                    if goblin_x.target_x <= goblin_x.end_x or goblin_x.target_y >= goblin_x.start_y:
                        goblin_x.follow = False
                    player.attack(goblin_x)
                    if goblin_x.health <= 0:
                        goblin_x.kill()
                        goblin_death_sound.play()
                        kill_lvl1 += 1
                    player.defend(goblin_x)
                    goblin_x.collide(collide_group_lvl1)
                    goblin_x.show(window)
            if player.rect.colliderect(portal_lvl1.rect):
                victory_lvl1 = True
            if lives <= 0:
                defeat_lvl1 = True

    if state == 'level 2':
        if victory_lvl2:
            finished = True
            next_level('victory', kill_lvl2, 5, coins)
            if menu_button.click(window, (41, 47, 75), (21, 24, 38)):
                state = 'main menu'
                finished = False
                reset_lvl2()
            elif retry_button_1.click(window, (41, 47, 75), (21, 24, 38)):
                reset_lvl2()
                lives = 5
                coins = 0
                state = 'level menu'
                finished = False
                victory_lvl2 = False
                player.spawn(lvl2_x, lvl2_y)
            elif next_button.click(window, (41, 47, 75), (21, 24, 38)):
                finished = False
                state = 'level menu'
        if defeat_lvl2:
            finished = True
            next_level('defeat', kill_lvl2, 5, coins)
            if menu_button.click(window, (41, 47, 75), (21, 24, 38)):
                state = 'main menu'
                finished = False
                reset_lvl2()
            elif retry_button_2.click(window, (41, 47, 75), (21, 24, 38)):
                reset_lvl2()
                lives = 5
                coins = 0
                finished = False
                defeat_lvl2 = False
        if lives != 0:
            if not finished:
                level_2(window)
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
                for goblin_x in goblins_lvl2_1:
                    goblin_x.update(target=player, target_x=player.rect.x, target_y=player.rect.y, start_y=370, end_x=430)
                    if goblin_x.target_y <= goblin_x.start_y:
                        goblin_x.follow = True
                    if goblin_x.target_x >= goblin_x.end_x or goblin_x.target_y >= goblin_x.start_y:
                        goblin_x.follow = False
                    player.attack(goblin_x)
                    if goblin_x.health <= 0:
                        goblin_x.kill()
                        goblin_death_sound.play()
                        kill_lvl2 += 1
                    player.defend(goblin_x)
                    goblin_x.collide(collide_group_lvl2)
                    goblin_x.show(window)
                for goblin_x in goblins_lvl2_2:
                    goblin_x.update(target=player, target_x=player.rect.x, target_y=player.rect.y, start_x=555, end_y=370)
                    if goblin_x.target_x >= goblin_x.start_x:
                        goblin_x.follow = True
                    if goblin_x.target_y >= goblin_x.end_y or goblin_x.target_x <= goblin_x.start_x:
                        goblin_x.follow = False
                    player.attack(goblin_x)
                    if goblin_x.health <= 0:
                        goblin_death_sound.play()
                        kill_lvl2 += 1
                        goblin_x.kill()
                    player.defend(goblin_x)
                    goblin_x.collide(collide_group_lvl2)
                    goblin_x.show(window)
            if player.rect.colliderect(portal_lvl2.rect):
                victory_lvl2 = True
            if lives <= 0:
                defeat_lvl2 = True

    if state == 'level 3':
        if victory_lvl3:
            finished = True
            next_level('victory', kill_lvl3, 1, coins)
            if menu_button.click(window, (41, 47, 75), (21, 24, 38)):
                state = 'main menu'
                finished = False
                reset_lvl3()
            elif retry_button_1.click(window, (41, 47, 75), (21, 24, 38)):
                reset_lvl3()
                coins = 0
                lives = 5
                state = 'level menu'
                finished = False
                victory_lvl3 = False
        if defeat_lvl3:
            finished = True
            next_level('defeat', kill_lvl3, 1, coins)
            if menu_button.click(window, (41, 47, 75), (21, 24, 38)):
                state = 'main menu'
                finished = False
                reset_lvl3()
        if lives != 0:
            if not finished:
                level_3(window)
                player.spawn(480, 120)
                player.trap(traps_group_lvl3)
                player.collide(collide_group_lvl3)
                boss_group.draw(window)
                boss_group.update(player, player.rect.y, 345)
                if boss.health > 0:
                    player.attack(boss)
                    player.defend(boss)
                if boss.health <= 0:
                    kill_lvl3 += 1
                    boss.kill()
                    if player.rect.colliderect(hatch_lvl3[0]):
                        w_hatch_collided_lvl3 = True
                        hatch_num_lvl3 = 1
                    if w_hatch_collided_lvl3:
                        for coin in coins_lvl3:
                            coin.update()
                            coin.draw(window)
                            if player.rect.colliderect(coin.rect):
                                collect_coin_sound.play()
                                coin.kill()
                                coin_amount_lvl3 -= 1
                                coins += 1
                            elif coin_amount_lvl3 == 0:
                                w_hatch_collided_lvl3 = False
                    if player.rect.colliderect(portal_lvl3.rect):
                        victory_lvl3 = True
            if lives <= 0:
                defeat_lvl3 = True

    if state == 'tutorial' or state == 'level 1' or state == 'level 2' or state == 'level 3':
        if not finished:
            all_sprites.update()
            all_sprites.draw(window)
        if home_button.click(window, (41, 47, 75), (21, 24, 38)):
            state = 'level menu'
    if state == 'tutorial' or state == 'level 1' or state == 'level 2' or state == 'level 3' or state == 'store' or state == 'armor store' or state == 'swords store' or state == 'potions store':
        if not finished:
            window.blit(lives_list[lives], (10, 0))
            window.blit(energy_list[energy], (120, 24))
            window.blit(money, (255, 20))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    text = font1.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))
    window.blit(text, (10, 680))

    pygame.display.update()
    clock.tick(fps)