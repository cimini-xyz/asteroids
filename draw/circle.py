import pygame

def draw_circle(screen, color, position, rotation, radius, points=None, width=2):
    pygame.draw.circle(
        screen,
        color,
        position,
        radius,
        width,
    )