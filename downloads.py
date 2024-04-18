import pygame
from pygame import *
pygame.init()


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
health_potion = transform.scale(pygame.image.load('store_items/health_potion.png'), (66, 88))
energy_potion = transform.scale(pygame.image.load('store_items/energy_potion.png'), (66, 88))

defeat_flag = transform.scale(pygame.image.load('images/defeat.png'), (151, 88))
victory_flag = transform.scale(pygame.image.load('images/victory.png'), (151, 88))
one_star = transform.scale(pygame.image.load('images/star.png'), (75, 70))
two_star = transform.scale(pygame.image.load('images/star.png'), (75, 70))
three_star = transform.scale(pygame.image.load('images/star.png'), (75, 70))
skull_killed = transform.scale(pygame.image.load('images/killed.png'), (75, 65))
# black_scr = transform.scale(pygame.image.load('images/black_scr.jpg'), (w_width, w_height))
# black_scr.set_alpha(200)
