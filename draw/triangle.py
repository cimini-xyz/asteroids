import pygame

def triangle(position, rotation, radius):
    forward = pygame.Vector2(0, 1).rotate(rotation)
    right = pygame.Vector2(0, 1).rotate(rotation + 90) * radius / 1.5
    a = position + forward * radius
    b = position - forward * radius - right
    c = position - forward * radius + right
    return [a, b, c]

def draw_triangle(screen, color, position, rotation, radius, points):
    pygame.draw.polygon(
        screen,
        color,
        triangle(position, rotation, radius),
        2
    )
