from circleshape import CircleShape
from constants import SCREEN_BACKGROUND_MODIFIER
import pygame

class Planet(CircleShape):
    sat_modifier = -0.1
    val_modifier = SCREEN_BACKGROUND_MODIFIER + 0.162
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)
        self.sat_modifier = Planet.sat_modifier
        self.val_modifier = Planet.val_modifier
    
        
    def update(self, dt):
        self.position[0] -= dt * 100
        self.position[1] += dt * 100
        if self.position[0] < -10 or self.position[1] < -10:
            self.kill()

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            self.position,
            self.radius,
            1
        )