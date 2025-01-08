import pygame

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.color = (255, 255, 255)

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def collide(self, other_circleshape):
        distance = self.position.distance_to(other_circleshape.position)
        return distance <= self.radius + other_circleshape.radius
