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