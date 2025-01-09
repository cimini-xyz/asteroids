import pygame
import random
from star import Star
from planet import Planet
from constants import *


class StarField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(SCREEN_WIDTH + 3, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -3),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        roll = random.uniform(0.0, 1.0)
        if roll > 0.825:
            planet = Planet(position.x, position.y, radius)
        else:
            star = Star(position.x, position.y, radius)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > STAR_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge_weights = [9, 16]
            edge = random.choices(self.edges, weights=edge_weights, k=1)[0]
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(random.uniform(3,8) // 1, position, velocity)