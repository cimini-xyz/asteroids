from circleshape import CircleShape
import pygame

class Star(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)
    
    def draw(self, surface):
        lines = [
            (
                (self.position[0]-self.radius, self.position[1]),
                (self.position[0]+self.radius, self.position[1])
            ),
            (
                (self.position[0], self.position[1]-self.radius),
                (self.position[0], self.position[1]+self.radius)
            ),
            (
                (self.position[0]-self.radius+1, self.position[1]+self.radius-1),
                (self.position[0]+self.radius-1, self.position[1]-self.radius+1)
            ),
            ( 
                (self.position[0]-self.radius+1, self.position[1]-self.radius+1),
                (self.position[0]+self.radius-1, self.position[1]+self.radius-1)
            )
        ]
        for line in lines:
            pygame.draw.line(
                surface,
                self.color,
                line[0],
                line[1],
                1
            )
        
    def update(self, dt):
        self.position[0] -= dt * 100
        self.position[1] += dt * 100
        if self.position[0] < -10 or self.position[1] < -10:
            self.kill()