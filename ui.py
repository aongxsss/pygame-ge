import pygame
from settings import *
def draw_text(surface, text, pos, color, font=FONTS["medium"], pos_mode="top_left",
                shadow=False, shadow_color=(10,0,0), shadow_offset=2):
    label = font.render(text, 1, color)
    label_rect = label.get_rect()
    if pos_mode == "top_left":
        label_rect.x, label_rect.y = pos
    elif pos_mode == "center":
        label_rect.center = pos
    if shadow:
        label_shadow = font.render(text, 1, shadow_color)
        surface.blit(label_shadow, (label_rect.x - shadow_offset, label_rect.y + shadow_offset))
    surface.blit(label, label_rect) 

def draw_text_with_outline(surface, text, pos, main_color, outline_color, font=FONTS["score_board_top"], 
                           pos_mode="top_left", shadow=False, shadow_color=(10, 0, 0), 
                           shadow_offset=2, outline_width=2):
    # วาดข้อความพร้อมขอบสี
    label = font.render(text, 1, main_color)
    label_rect = label.get_rect()
    
    if pos_mode == "top_left":
        label_rect.x, label_rect.y = pos
    elif pos_mode == "center":
        label_rect.center = pos

    # วาดข้อความรอบๆ ด้วยสี outline
    for dx in [-outline_width, 0, outline_width]:
        for dy in [-outline_width, 0, outline_width]:
            if dx == 0 and dy == 0:  # ข้ามการวาดตรงกลาง
                continue
            label_outline = font.render(text, 1, outline_color)
            surface.blit(label_outline, (label_rect.x + dx, label_rect.y + dy))
    
    # วาดข้อความ shadow (ถ้ามี)
    if shadow:
        label_shadow = font.render(text, 1, shadow_color)
        surface.blit(label_shadow, (label_rect.x - shadow_offset, label_rect.y + shadow_offset))
    
    # วาดข้อความหลัก
    surface.blit(label, label_rect)


def button(surface, pos_x, pos_y, text=None,click_sound=None):
    rect = pygame.Rect((pos_x, pos_y), BUTTONS_SIZES) 
    # rect = pygame.Rect((SCREEN_WIDTH//2 - BUTTONS_SIZES[0]//2, pos_y), BUTTONS_SIZES)
    border_radius = 15
    on_button = False
    if rect.collidepoint(pygame.mouse.get_pos()):
        color = COLORS["buttons"]["second"]
        on_button = True
    else:
        color = COLORS["buttons"]["default"]

   
    pygame.draw.rect(surface, COLORS["buttons"]["shadow"], (rect.x - 6, rect.y - 6, rect.w, rect.h), border_radius=border_radius) 
    pygame.draw.rect(surface, color, rect,border_radius=border_radius) 
    if text is not None:
 
        draw_text(surface, text, rect.center, COLORS["buttons"]["text"], pos_mode="center",
                    shadow=True, shadow_color=COLORS["buttons"]["shadow"])
    if on_button and pygame.mouse.get_pressed()[0]: 
        if click_sound is not None: 
            click_sound.play()
        return True
