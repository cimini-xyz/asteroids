import pygame
from constants import *
from circleshape import CircleShape
import random
from globalhue import reset_asteroid_split_flash_remaining, reset_asteroid_kill_flash_remaining
from screenfx import reset_screen_shake_asteroid_kill, reset_screen_shake_asteroid_split
from draw.circle import draw_circle


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)

    def draw(self, screen):
        draw_circle(
            screen,
            self.color,
            self.position,
            0,
            self.radius
        )
        
    def update(self, dt):
        self.position += self.velocity * dt
        

    def split(self, dt):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            reset_asteroid_kill_flash_remaining()
            reset_screen_shake_asteroid_kill()
            return
        random_angle = random.uniform(20, 50)
        new_vector_a = self.velocity.rotate(random_angle)
        new_vector_b = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_a = Asteroid(self.position[0],self.position[1],new_radius)
        asteroid_b = Asteroid(self.position[0],self.position[1],new_radius)
        asteroid_a.velocity = new_vector_a * 1.2
        asteroid_b.velocity = new_vector_b * 1.2
        reset_asteroid_split_flash_remaining()
        reset_screen_shake_asteroid_split()