import pygame
from circleshape import CircleShape
from constants import *
from globalhue import get_ghost_image_color
from draw.circle import draw_circle

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.color = (255,255,255)
        self.visible_radius = SHOT_RADIUS
        self.rotation = 0

    def draw(self, screen):
        draw_circle(
            screen,
            'white',
            self.position,
            0,
            self.visible_radius
        )

    def update(self, dt):
        self.position += self.velocity * dt
