import pygame
from circleshape import CircleShape
from constants import *
from globalhue import get_ghost_image_color

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.__init_ghost_image()

    def draw_base(self, screen, color, position, radius, width):
        pygame.draw.circle(
            screen,
            color,
            position,
            radius,
            width
        )

    def draw(self, screen):
        self.draw_ghost_images(screen)
        self.draw_base(
            screen,
            'white',
            self.position,
            self.radius,
            2
        )

    def update(self, dt):
        self.position += self.velocity * dt
        self.handle_ghost_image(dt)

    def __init_ghost_image(self):
        self.ghost_image_length = []
        self.ghost_image_position = []
        self.last_triggered_time = 0

    def add_ghost_image(self):
        self.ghost_image_length.append(SHOT_GHOST_IMAGE_LENGTH)
        self.ghost_image_position.append(self.position.copy())

    def reduce_ghost_image_length(self, index, dt):
        self.ghost_image_length[index] = self.ghost_image_length[index] - dt

    def handle_ghost_image_spawn(self, dt):
        self.last_triggered_time += dt
        if self.last_triggered_time >= SHOT_GHOST_IMAGE_FREQUENCY:
            self.last_triggered_time -= SHOT_GHOST_IMAGE_FREQUENCY
            self.add_ghost_image()

    def handle_ghost_image_reduction(self, dt):
        for i in range(len(self.ghost_image_length) - 1, -1, -1):
            self.reduce_ghost_image_length(i, dt)
            if self.ghost_image_length[i] <= 0:
                del self.ghost_image_length[i]
                del self.ghost_image_position[i]

    def handle_ghost_image(self, dt):
        self.handle_ghost_image_spawn(dt)
        self.handle_ghost_image_reduction(dt)

    def draw_ghost_images(self, screen):
        for i in range(0, len(self.ghost_image_length)):
            if self.ghost_image_length[i] <= SHOT_GHOST_IMAGE_LENGTH:
                ghost_image_color = get_ghost_image_color(self.ghost_image_length[i], SHOT_GHOST_IMAGE_INTENSITY)
                self.draw_base(
                    screen,
                    ghost_image_color,
                    self.ghost_image_position[i],
                    self.radius,
                    2
                )