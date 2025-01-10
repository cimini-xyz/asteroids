import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot
from globalhue import get_ghost_image_color
from draw.triangle import draw_triangle

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
        self.shot_flash_length = 0
        self.visible_radius = PLAYER_VISIBLE_RADIUS
    
    def draw(self, screen):
        draw_triangle(
            screen,
            self.color,
            self.position,
            self.rotation,
            self.visible_radius
        )

    def update(self, dt):
        self.shoot_cooldown = max(0, self.shoot_cooldown - dt)
        self.shot_flash_length = max(0, self.shot_flash_length - dt)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_q]:
            self.strafe_left(dt)
        if keys[pygame.K_e]:
            self.strafe_right(dt)
        if keys[pygame.K_SPACE]:
            self.shoot(dt)
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def strafe_left(self, dt):
        vector = 1
        if (self.rotation - 90) % 360 > 180:
            vector = -1
        left = pygame.Vector2(vector, 0).rotate(self.rotation)
        self.position += left * PLAYER_SPEED * dt

    def strafe_right(self, dt):
        vector = -1
        if (self.rotation - 90) % 360 > 180:
            vector = 1
        right = pygame.Vector2(vector, 0).rotate(self.rotation)
        self.position += right * PLAYER_SPEED * dt


    def shoot(self, dt):
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.shot_flash_length = PLAYER_SHOT_FLASH_LENGTH
        shot = Shot(self.position[0], self.position[1])
        vector = pygame.Vector2(0, 1)
        vector = vector.rotate(self.rotation)
        shot.velocity = vector * PLAYER_SHOOT_SPEED