import pygame

def draw_circle(screen, color, position, rotation, radius):
    pygame.draw.circle(
        screen,
        color,
        position,
        radius,
        2
    )