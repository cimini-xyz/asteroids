from circleshape import CircleShape
import pygame

class Planet(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)
    
        
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