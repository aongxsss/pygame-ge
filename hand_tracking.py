import cv2
import mediapipe as mp
from settings import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=5, 
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

class HandTracking:
    def __init__(self):
        self.hands_positions = []  # List to store multiple hands' positions
        self.hands_closed = []     # List to track whether each hand is closed
        self.results = None

    def scan_hands(self, image):
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        self.results = hands.process(image)  
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.hands_positions = []
        self.hands_closed = []
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Get the center position of the hand (landmark 9 - center of the palm)
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                self.hands_positions.append((int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)))
                
                # Check if the hand is closed (comparing y-tip with y-center)
                x_tip, y_tip = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y  # Tip of the index finger
                is_closed = y_tip > y
                self.hands_closed.append(is_closed)
                
                # Draw the hand landmarks
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
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
