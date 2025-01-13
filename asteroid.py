import pygame
from constants import *
from circleshape import CircleShape
import random
from globalhue import reset_asteroid_split_flash_remaining, reset_asteroid_kill_flash_remaining
from draw.asteroid import draw_asteroid, asteroid
from vfx.screenshake.manager import ScreenShakeManager
from devicemanager import retrigger_asteroid_kill, retrigger_asteroid_split

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)
        self.points = asteroid(self.radius, 20)

    def draw(self, screen):
        draw_asteroid(
            screen,
            self.color,
            self.position,
            0,
            self.radius,
            self.points
        )
        #draw_circle(
        #    screen,
        #    self.color,
        #    self.position,
        #    0,
        #    self.radius
        #)
        
    def update(self, dt):
        self.position += self.velocity * dt
        

    def split(self, dt):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            retrigger_asteroid_kill()
            #reset_screen_shake_asteroid_kill()
            ScreenShakeManager.get_instance().send_impulse('asteroid_kill')
            return
        random_angle = random.uniform(20, 50)
        new_vector_a = self.velocity.rotate(random_angle)
        new_vector_b = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_a = Asteroid(self.position[0],self.position[1],new_radius)
        asteroid_b = Asteroid(self.position[0],self.position[1],new_radius)
        asteroid_a.velocity = new_vector_a * 1.2
        asteroid_b.velocity = new_vector_b * 1.2
        retrigger_asteroid_split()
        #reset_asteroid_split_flash_remaining()
        #reset_screen_shake_asteroid_split()
        ScreenShakeManager.get_instance().send_impulse('asteroid_split')