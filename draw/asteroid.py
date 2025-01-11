import math
import random
import pygame

def asteroid(radius, num_vertices):
    points = []
    for i in range(num_vertices):
        angle = (i / num_vertices) * 2 * math.pi
        # Add some random variance to radius
        variance = random.uniform(0.8, 1.2)
        x = math.cos(angle) * radius * variance
        y = math.sin(angle) * radius * variance
        points.append((x, y))
    return points

def draw_asteroid(surface, color, position, rotation, radius, points, width=2):
    # Transform points to world space
    world_points = [(pygame.Vector2(p) + position) for p in points]
    # True makes it close the shape
    pygame.draw.lines(surface, color, True, world_points, width)