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
        self.sounds["continue_sounds"] = pygame.mixer.Sound("assets/sounds/continue_sounds.mp3")
        self.sounds['15sec'] = pygame.mixer.Sound("assets/sounds/15sec.mp3")
        self.alert_time_sound = False 
        self.sounds["Applause"] = pygame.mixer.Sound("assets/sounds/Applause.mp3")
        self.sounds["Applause"].set_volume(0.5) 
        self.end_sound_played = False 

    def reset(self):
        self.hand_tracking = HandTracking()
        self.hands = []  # List of Hand objects
        self.rms = []
        self.rms_spawn_timer = 0
        self.rick_delay_timer = time.time() + 10
        self.scores = {
            "Pink": 0,
            "Red": 0,
            "Yellow": 0,
            "Purple": 0,
            "Blue": 0
        }
        self.end_sound_played = False
        self.game_start_time = time.time()
        self.initial_delay = 10

    def spawn_rms(self):
        t = time.time()
        # Only start spawning after the initial delay
        if (t - self.game_start_time) < self.initial_delay:
            return
            
        if t > self.rms_spawn_timer:
            self.rms_spawn_timer = t + MORTY_SPAWN_TIME
            # increase the probability that the rm will be a rick over time
            elapsed_time = t - self.game_start_time - self.initial_delay  # Adjust elapsed time to account for delay
            nb = (GAME_DURATION-self.time_left)/GAME_DURATION * 100 / 2  # increase from 0 to 50 during all the game (linear)
            if random.randint(0, 100) < nb:
                self.rms.append(Rick())
            else:
                self.rms.append(Morty())
            # spawn another morty after the half of the game
            if self.time_left < GAME_DURATION/2:
                self.rms.append(Morty())
    def load_camera(self):
        _, self.frame = self.cap.read()
        # width =  1250
        # height = 700
        width =  800
        height = 600
        self.frame = cv2.resize(self.frame, (width, height))  
    def set_hand_positions(self):
        self.frame = self.hand_tracking.scan_hands(self.frame)
        hands_positions, hands_closed = self.hand_tracking.get_hands_data()
        tracked_hands = self.hand_tracking.tracked_hands

        # สร้าง map ของ position กับ hand_id จาก tracked_hands
        position_to_id = {}
        for i, pos in enumerate(hands_positions):
            screen_x, screen_y = pos
            rel_x, rel_y = screen_x/SCREEN_WIDTH, screen_y/SCREEN_HEIGHT
            for tracked_pos, tracked_id in tracked_hands.items():
                if abs(tracked_pos[0] - rel_x) < 0.1 and abs(tracked_pos[1] - rel_y) < 0.1:
                    position_to_id[pos] = tracked_id
                    break
        # จัดการกับ hands list
        new_hands = []
        for i, (pos, is_closed) in enumerate(zip(hands_positions, hands_closed)):
            hand_id = position_to_id.get(pos, i)  # ไม่ต้องทำ modulo ที่นี่
            
            # หา hand เดิมที่มี id ตรงกัน
            existing_hand = None
            for hand in self.hands:
                if hand.hand_id == hand_id % 5:  # เทียบ hand_id หลัง modulo
                    existing_hand = hand
                    break
            
            # ถ้าไม่มี hand เดิม สร้างใหม่
            if existing_hand is None:
                hand = Hand(hand_id=hand_id)  # Hand class จะจัดการ modulo เอง
            else:
                hand = existing_hand
                
            # อัพเดตตำแหน่งและสถานะ
            hand.rect.center = pos
            hand.left_click = is_closed
            if is_closed:
                hand.image = hand.image_smaller.copy()
            else:
                hand.image = hand.orig_image.copy()
            new_hands.append(hand)

        self.hands = new_hands
    def draw(self):
        
        # Draw the background
        self.background.draw(self.surface)
        
        # Draw the rms
        for rm in self.rms:
            rm.draw(self.surface)
        
        # Draw all hands
        for hand in self.hands:
            hand.draw(self.surface)
        
        y_offset = 20
        for color, score in self.scores.items():
            if score > 0:  
                ui.draw_text(self.surface, f"{color} Score: {score}", 
                        (5, y_offset), SCORE_COLORS[color],  
                        font=FONTS["small"], shadow=False)
                y_offset += 35
    
    # Draw the time left
        timer_text_color = (255, 255, 255) if self.time_left < 5 else COLORS["timer"]
        ui.draw_text(self.surface, f"Time left: {self.time_left}", 
                    (SCREEN_WIDTH//1.4, 5), timer_text_color, 
                font=FONTS["medium"], shadow=False)
            

    def game_time_update(self):
        self.time_left = max(round(GAME_DURATION - (time.time() - self.game_start_time), 1), 0)
        if self.time_left == 16 and not self.alert_time_sound:
            self.sounds["15sec"].play()
            self.alert_time_sound = True
        
    def update(self):
        self.load_camera()
        self.set_hand_positions()
        self.game_time_update()
        self.draw()

        if self.time_left > 0:
            self.spawn_rms()
            for hand in self.hands:
                hand_color = hand.get_color()
                score = hand.kill_rms(self.rms, self.scores[hand_color], self.sounds)
                self.scores[hand_color] = score
            for rm in self.rms:
                rm.move()


        else:
            if not self.end_sound_played:  
                self.sounds["Applause"].play() 
                self.end_sound_played = True

            shadow = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) 
            # shadow.fill((6, 2, 38)) 
            shadow.set_alpha(100)  
            self.surface.blit(shadow, (0, 0))

            # x_scores_rect = SCREEN_WIDTH // 2 - 300 #  SCREEN_WIDTH // 2 - 200
            # y_scores_rect = 100 # 250
            # width_scores_rect = 600 # 400
            # height_scores_rect = 600 # 300

            x_scores_rect = SCREEN_WIDTH * 0.32 #  SCREEN_WIDTH // 2 - 200
            y_scores_rect = SCREEN_HEIGHT * 0.20 # 250
            width_scores_rect = 650 # 400
            height_scores_rect = 550 # 300
            scores_rect = pygame.Rect(x_scores_rect, y_scores_rect, width_scores_rect, height_scores_rect) # กรอบ Top Scorers
            pygame.draw.rect(self.surface, (6, 2, 38), scores_rect, border_radius=30)  # วาดพื้นหลังกรอบ 
            pygame.draw.rect(self.surface, (189, 173, 0), scores_rect, width=10, border_radius=30)  # วาดกรอบ 

            sorted_scores = sorted([(color, score) for color, score in self.scores.items() if score > 0],
                                 key=lambda x: x[1], reverse=True)
            
            padding = 80
            center_x = SCREEN_WIDTH // 2.05
            y_start = y_scores_rect + padding 

            ui.draw_text_with_outline(
                    surface=self.surface,
                    text="Top Scorers",
                    pos=(center_x, y_start),
                    main_color=COLORS["buttons"]["default"],
                    outline_color=(255, 255, 255),
                    font=FONTS["score_board_top"],
                    pos_mode="center",
                    outline_width=3
            )
            rank_colors = {
                i: SCORE_COLORS[color] for i, (color, _) in enumerate(sorted_scores[:5])
            }
            
            for i, (color, score) in enumerate(sorted_scores[:5]):
                y_pos = y_start + 70 + (i * 55) 
                rank_text = ["1st", "2nd", "3rd", "4th", "5th"][i]
                text = f"{rank_text}: {color} - {score}"
                ui.draw_text(self.surface, text,
                           (center_x, y_pos),
                           rank_colors[i],
                           font=FONTS["score_board_by_color"],
                           pos_mode="center")
            # # Continue button
            padding_continue_button = 20
            center_x = SCREEN_WIDTH // 2 - BUTTONS_SIZES[0] // 1.7
            button_y = SCREEN_HEIGHT * 0.58
            if ui.button(self.surface, center_x, button_y+padding_continue_button, "Continue", click_sound=self.sounds["continue_sounds"]):
                return "menu"
        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)