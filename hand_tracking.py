import cv2
import mediapipe as mp
from settings import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2, 
    min_detection_confidence=0.2,
    min_tracking_confidence=0.2
)

class HandTracking:
    def __init__(self):
        self.hands_positions = []  # List to store multiple hands' positions
        self.hands_closed = []     # List to track whether each hand is closed
        self.results = None
        # self.hand_ids = {}  # Dictionary to store hand IDs based on position
        # self.next_id = 0 # Counter for assigning new hand IDs
        # self.hand_states = {}
        self.tracked_hands = {}  # Dictionary to maintain hand tracking consistency
        self.next_id = 0
        

    def get_hand_id(self, x, y):
        # Find the closest existing hand ID within a threshold
        threshold = 0.2  # Adjust this value based on your needs
        min_dist = float('inf')
        closest_id = None
        
        for pos, hand_id in self.hand_ids.items():
            old_x, old_y = pos
            dist = ((x - old_x) ** 2 + (y - old_y) ** 2) ** 0.5
            if dist < min_dist and dist < threshold:
                min_dist = dist
                closest_id = hand_id
                
        if closest_id is not None:
            old_pos = next(pos for pos, id_ in self.hand_ids.items() if id_ == closest_id)
            del self.hand_ids[old_pos]
            self.hand_ids[(x, y)] = closest_id
            return closest_id
        else:
            new_id = self.next_id
            self.hand_ids[(x, y)] = new_id
            self.next_id = (self.next_id + 1) % 5
            return new_id
        
    def scan_hands(self, image):
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        self.results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.hands_positions = []
        self.hands_closed = []
        current_hands = set()
        
        if self.results.multi_hand_landmarks:
            detected_hands = []
            # สร้าง set ของ IDs ที่ใช้งานอยู่
            used_ids = set(self.tracked_hands.values())
            
            for hand_landmarks in self.results.multi_hand_landmarks:
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                screen_x, screen_y = int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)
                
                hand_found = False
                # ตรวจสอบมือที่มีอยู่แล้ว
                for tracked_pos, hand_id in list(self.tracked_hands.items()):
                    old_x, old_y = tracked_pos
                    if abs(x - old_x) < 0.2 and abs(y - old_y) < 0.2:
                        del self.tracked_hands[tracked_pos]
                        self.tracked_hands[(x, y)] = hand_id
                        hand_found = True
                        break
                
                # ถ้าเป็นมือใหม่
                if not hand_found:
                    # หา ID ที่ว่างอยู่
                    available_id = 0
                    while available_id in used_ids and available_id < 5:
                        available_id += 1
                    
                    # ถ้ายังมี ID ว่างอยู่
                    if available_id < 5:
                        self.tracked_hands[(x, y)] = available_id
                        used_ids.add(available_id)
                
                # เช็คว่ามือกำหรือไม่
                y_tip = hand_landmarks.landmark[12].y
                is_closed = y_tip > y
                
                try:
                    hand_id = self.tracked_hands[(x, y)]
                except KeyError:
                    print("Key not found:", (x, y))
                    continue

                detected_hands.append((
                    hand_id,
                    (screen_x, screen_y),
                    is_closed
                ))

                # detected_hands.append((
                #     self.tracked_hands[(x, y)],
                #     (screen_x, screen_y),
                #     is_closed
                # ))

                current_hands.add((x, y))
                
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

            # ลบมือที่ไม่ได้ถูกตรวจจับแล้ว
            self.tracked_hands = {pos: id_ for pos, id_ in self.tracked_hands.items() 
                                if pos in current_hands}

            # เรียงตาม ID
            detected_hands.sort(key=lambda x: x[0])
            
            # อัพเดตตำแหน่งและสถานะ
            for _, pos, closed in detected_hands:
                self.hands_positions.append(pos)
                self.hands_closed.append(closed)

        # ถ้าไม่พบมือ
        if not self.results.multi_hand_landmarks:
            self.tracked_hands.clear()

        return image

    def get_hands_data(self):
        return self.hands_positions, self.hands_closed
    def get_hand_center(self):
        return (self.hand_x, self.hand_y)
    def display_hand(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(1)
    def is_hand_closed(self):
        pass
