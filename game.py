import pygame
import time
import random
from settings import *
from background import Background
from hand import Hand
from hand_tracking import HandTracking
from morty import Morty
from rick import Rick
import cv2
import ui
class Game:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background('assets/images/background/game_bg.png')
        self.cap = cv2.VideoCapture(1)
        self.sounds = {}
        self.sounds["im_out"] = pygame.mixer.Sound("assets/sounds/im_out.mp3")
    def reset(self):
        self.hand_tracking = HandTracking()
        self.hands = []  # List of Hand objects
        self.rms = []
        self.rms_spawn_timer = 0
        self.score = 0
        self.game_start_time = time.time()

    def spawn_rms(self):
        t = time.time()
        if t > self.rms_spawn_timer:
            self.rms_spawn_timer = t + MORTY_SPAWN_TIME
            # increase the probability that the rm will be a rick over time
            nb = (GAME_DURATION-self.time_left)/GAME_DURATION * 100  / 2  # increase from 0 to 50 during all  the game (linear)
            if random.randint(0, 100) < nb:
                self.rms.append(Rick())
            else:
                self.rms.append(Morty())
            # spawn a other morty after the half of the game
            if self.time_left < GAME_DURATION/2:
                self.rms.append(Morty())
    def load_camera(self):
        _, self.frame = self.cap.read()
        # width = 800 
        # height = 550  
        # self.frame = cv2.resize(self.frame, (width, height))  
    def set_hand_positions(self):
        self.frame = self.hand_tracking.scan_hands(self.frame)
        hands_positions, hands_closed = self.hand_tracking.get_hands_data()
        
        # Ensure the number of `Hand` objects matches the detected hands
        while len(self.hands) < len(hands_positions):
            new_hand_id = len(self.hands)  # This will automatically use the correct image based on order
            self.hands.append(Hand(hand_id=new_hand_id))
            
        while len(self.hands) > len(hands_positions):
            self.hands.pop()
            
        # Update positions and states for existing hands
        for i, hand in enumerate(self.hands):
            hand.rect.center = hands_positions[i]
            hand.left_click = hands_closed[i]
            if hand.left_click:
                hand.image = hand.image_smaller.copy()
            else:
                hand.image = hand.orig_image.copy()
    def draw(self):
    # Draw the background
        self.background.draw(self.surface)
        
        # Draw the rms
        for rm in self.rms:
            rm.draw(self.surface)
        
        # Draw all hands
        for hand in self.hands:
            hand.draw(self.surface)
        
        if self.time_left > 0:
            # Draw the score during gameplay
            ui.draw_text(self.surface, f"Score : {self.score}", (5, 5), 
                        COLORS["score"], font=FONTS["medium"], shadow=False)
            
            # Draw the time left
            timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"]
            ui.draw_text(self.surface, f"Time left : {self.time_left}", 
                        (SCREEN_WIDTH//2 + 200, 5), timer_text_color, 
                        font=FONTS["medium"], shadow=False)
        else:
            # Draw the final score in the center when game is over
            ui.draw_text(self.surface, f"Final Score: {self.score}", 
                        (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50), 
                        COLORS["final_score"], font=FONTS["big"], 
                        pos_mode="center", shadow=True)
        

    def game_time_update(self):
        self.time_left = max(round(GAME_DURATION - (time.time() - self.game_start_time), 1), 0)
        
    def update(self):
        self.load_camera()
        self.set_hand_positions()
        self.game_time_update()
        self.draw()
        
        if self.time_left > 0:
            self.spawn_rms()
            for hand in self.hands:
                self.score = hand.kill_rms(self.rms, self.score, self.sounds)
            for rm in self.rms:
                rm.move()
        else:
            # Add some spacing below the score for the continue button
            if ui.button(self.surface, 
                        SCREEN_WIDTH//2 - BUTTONS_SIZES[0]//2,  # Center horizontally
                        SCREEN_HEIGHT//2 + 50,                  # Below the score
                        "Continue", 
                        click_sound=self.sounds["im_out"]):
                return "menu"
                
        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)
