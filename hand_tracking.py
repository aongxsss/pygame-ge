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
        self.hand_ids = {}  # Dictionary to store hand IDs based on position
        self.next_id = 0 # Counter for assigning new hand IDs
        self.hand_states = {}
        

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

        detected_hands = []
        self.hand_states.clear()  # Clear previous hand states
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                screen_x, screen_y = int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)
                
                # Get stable hand ID for this position
                hand_id = self.get_hand_id(x, y)
                
                # Check if hand is closed
                y_tip = hand_landmarks.landmark[12].y
                is_closed = y_tip > y
                
                # Store hand data with its ID
                detected_hands.append((hand_id, (screen_x, screen_y), is_closed))
                
                # Draw landmarks
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
            
            # Sort by hand ID to maintain consistent order
            detected_hands.sort(key=lambda x: x[0])
            
            # Update positions and states lists
            self.hands_positions = []
            self.hands_closed = []
            self.hand_states = {}
            
            for hand_id, pos, is_closed in detected_hands:
                self.hands_positions.append(pos)
                self.hands_closed.append(is_closed)
                self.hand_states[hand_id] = is_closed
            
        # Clean up old positions
        current_positions = set((x, y) for x, y in self.hand_ids.keys())
        positions_to_remove = []
        for pos in current_positions:
            if not any(abs(x - pos[0]) < 0.2 and abs(y - pos[1]) < 0.2 
                      for x, y in ((p[0]/SCREEN_WIDTH, p[1]/SCREEN_HEIGHT) 
                                 for p in self.hands_positions)):
                positions_to_remove.append(pos)
        
        for pos in positions_to_remove:
            del self.hand_ids[pos]

        return image



    def get_hands_data(self):
        return self.hands_positions, [self.hand_states.get(i, False) for i in range(len(self.hands_positions))]

    def get_hand_center(self):
        return (self.hand_x, self.hand_y)
    def display_hand(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(1)
    def is_hand_closed(self):
        pass
