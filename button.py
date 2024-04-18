import pygame
from pygame import *
pygame.init()


class Button:
    def __init__(self, button_x, button_y, button_width, button_height, text):
        self.width = button_width
        self.height = button_height
        self.x = button_x
        self.y = button_y
        self.clicked = False
        self.inactive_color = (21, 24, 38)
        self.active_color = (41, 47, 75)
        self.inactive_color_1 = (41, 47, 75)
        self.active_color_1 = (51, 63, 92)
        self.border_radius = 20
        self.text = text
        self.is_clicked = False

    def click(self, screen):
        mouse_controller = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x < mouse_controller[0] < self.x + self.width and self.y < mouse_controller[1] < self.y + self.height:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height),
                             border_radius=self.border_radius)
            if click[0] and not self.is_clicked:
                self.is_clicked = True
                button_click_sound.play()
                return True
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height),
                             border_radius=self.border_radius)
            self.is_clicked = False

        create_text(screen, self.text, x=self.x + 15, y=self.y + 10)

    def click_1(self, screen):
        mouse_controller = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x < mouse_controller[0] < self.x + self.width and self.y < mouse_controller[1] < self.y + self.height:
            pygame.draw.rect(screen, self.active_color_1, (self.x, self.y, self.width, self.height),
                             border_radius=self.border_radius)
            if click[0] and not self.is_clicked:
                self.is_clicked = True
                button_click_sound.play()
                return True
        else:
            pygame.draw.rect(screen, self.inactive_color_1, (self.x, self.y, self.width, self.height),
                             border_radius=self.border_radius)
            self.is_clicked = False

        create_text(screen, self.text, x=self.x + 15, y=self.y + 10)


def create_text(screen, text, x, y, font_color=(0, 0, 0), font_size=20):
    text = pygame.font.Font('fonts/Retro Gaming.ttf', font_size).render(text, True, font_color)
    screen.blit(text, (x, y))

button_click_sound = pygame.mixer.Sound('sounds/Menu Selection Click.wav')

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
home_button = Button(900, 5, 95, 45, 'HOME')
menu_button = Button(500, 420, 95, 45, 'MENU')
next_button = Button(590, 360, 95, 45, 'NEXT')
retry_button_1 = Button(415, 365, 95, 45, 'RETRY')
retry_button_2 = Button(500, 365, 95, 45, 'RETRY')

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