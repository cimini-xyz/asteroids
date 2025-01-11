import pygame

def draw_circle(screen, color, position, rotation, radius, points=None):
    pygame.draw.circle(
        screen,
        color,
        position,
        radius,
        2,
    )