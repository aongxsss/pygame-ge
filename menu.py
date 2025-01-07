import pygame
import sys
from settings import *
from background import Background
import ui
import image
class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background('assets/images/background/menu_bg.png')
        self.click_sound = pygame.mixer.Sound(f"assets/sounds/hey_whatup.mp3")
    def draw(self):
        self.background.draw(self.surface)
    def update(self):
        self.draw()
        center_x = SCREEN_WIDTH // 2 - BUTTONS_SIZES[0] // 2
        center_x_of_start = center_x-120
        if ui.button(self.surface, center_x_of_start, 650, "Start", click_sound=self.click_sound):
            return "game"
        if ui.button(self.surface, center_x_of_start+BUTTONS_SIZES[1]*3, 650, "Quit", click_sound=self.click_sound):
            pygame.quit()
            sys.exit()
