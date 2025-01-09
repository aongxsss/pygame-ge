import pygame
pygame.init()
info = pygame.display.Info()
WINDOW_NAME = "Galactic Defenders"
GAME_TITLE = WINDOW_NAME
# SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 900
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 750

FPS = 90
DRAW_FPS = True
# sizes
BUTTONS_SIZES = (240, 90)
HAND_SIZE = 180
HAND_HITBOX_SIZE = (60, 80)
MORTY_SIZES = (80, 80)
MORTY_SIZE_RANDOMIZE = (1,2) # for each new morty, it will multiply the size with an random value beteewn X and Y
RICKS_SIZES = (100, 100)
RICK_SIZE_RANDOMIZE = (1.2, 1.5)
# drawing
DRAW_HITBOX = False # will draw all the hitbox
# animation
ANIMATION_SPEED = 0.09 # the frame of the deities will change every X sec # Default is 0.09
# ANIMATION_SPEED = 0.3
# difficulty
GAME_DURATION = 70 # the game will last X sec
MORTY_SPAWN_TIME = 0.5 # Default is 1
MORTY_MOVE_SPEED = {"min": 6, "max": 8} # Default is 1 {"min": 1, "max": 6}
RICK_PENALITY = 1 # will remove X of the score of the player (if he kills an rick)
# colors
COLORS = {"title": (255, 255, 255), "score": (255, 255, 255),"final_score": (255, 215, 0), "timer": (255, 255, 255),
            "buttons": {"default": (56, 67, 209), "second":  (87, 99, 255),
                        "text": (255, 255, 255), "shadow": (0, 0, 0)}} # second is the color when the mouse is on the button
# sounds / music
MUSIC_VOLUME = 0.5 # value between 0 and 1
SOUNDS_VOLUME = 0.2
# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font("assets/font/alata-regular.ttf", 35)
# FONTS["medium"] = pygame.font.Font(None, 65)
FONTS["medium"] = pygame.font.Font("assets/font/alata-regular.ttf", 55)
FONTS["score_board_top"] = pygame.font.Font("assets/font/SansSerifExbFLF.otf", 60)
FONTS["score_board_by_color"] = pygame.font.Font("assets/font/SansSerifExbFLF.otf", 40)
# FONTS["medium"] = pygame.font.Font("assets/font/Basic-Regular.otf", 55)
FONTS["big"] = pygame.font.Font("assets/font/alata-regular.ttf", 110)

SCORE_COLORS = {
            "Pink": (255, 122, 210),   
            "Red": (240, 64, 20),       
            "Yellow": (255, 199, 26),   
            "Purple": (191, 53, 217),   
            "Blue": (0, 163, 255)       
        }