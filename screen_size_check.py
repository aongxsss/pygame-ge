import pygame, os

pygame.init()
info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
print(f"SCREEN_WIDTH: {info.current_w}, SCREEN_HEIGHT: {info.current_h}")