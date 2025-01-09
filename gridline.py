from constants import *
import pygame

gridline_surface_a = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
gridline_surface_b = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

gridline_x_offset = 0
gridline_y_offset = 0

def gridline_convert_alpha():
    global gridline_surface_a
    global gridline_surface_b
    gridline_surface_a = gridline_surface_a.convert_alpha()
    gridline_surface_b = gridline_surface_b.convert_alpha()

def get_gridline_surface(gridline_surface, grid_color, grid_spacing):
    pos_y = SCREEN_HEIGHT // 2
    gridline_surface.fill((0,0,0,0))
    pygame.draw.line(gridline_surface, grid_color, (0,pos_y),(SCREEN_WIDTH,pos_y))

    for x in range(0, SCREEN_WIDTH, grid_spacing):
        pygame.draw.line(gridline_surface, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)

    for y in range(0, SCREEN_HEIGHT, grid_spacing):
        pygame.draw.line(gridline_surface, grid_color, (0, y), (SCREEN_WIDTH, y), 1)
    return gridline_surface

def pan_gridline_x(dt, grid_spacing):
    global gridline_x_offset
    gridline_x_offset -= dt * 100
    gridline_x_offset %= grid_spacing
    

def pan_gridline_y(dt, grid_spacing):
    global gridline_y_offset
    gridline_y_offset -= dt * 50
    gridline_y_offset %= grid_spacing

def get_gridline_x_offset():
    global gridline_x_offset
    return gridline_x_offset

def get_gridline_y_offset():
    global gridline_y_offset
    return gridline_y_offset