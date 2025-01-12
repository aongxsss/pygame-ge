import pygame
import random
import image
from settings import *
from aliens_b import aliens_b
aliens_aImgs = ['assets/images/aliens_a/Aliens_A_.png', 'assets/images/aliens_a/Aliens_A_.png', 'assets/images/aliens_a/Aliens_A_.png']
class aliens_a(aliens_b):
    def __init__(self):
        random_size_value = random.uniform(aliens_a_SIZE_RANDOMIZE[0], aliens_a_SIZE_RANDOMIZE[1])
        size = (int(aliens_aS_SIZES[0] * random_size_value), int(aliens_aS_SIZES[1] * random_size_value))
        moving_direction, start_pos = self.define_spawn_pos(size)
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.2, size[1]//1.2)
        aliens_aImg = random.choice(aliens_aImgs)
        self.images = [image.load(aliens_aImg, size=size, flip=moving_direction=="right") for nb in range(1, 10)] # load the images
        self.current_frame = 0
        self.animation_timer = 0
    def kill(self, aliens_a): # remove aliens_a from the list
        aliens_a.remove(self)
        # return -aliens_a_PENALITY
        return 3
