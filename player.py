import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot
from globalhue import get_ghost_image_color

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
        self.shot_flash_length = 0
        self.ghost_image_length = []
        self.ghost_image_position = []
        self.ghost_image_rotation = []
        self.last_triggered_time = 0
        
    
    # in the player class
    def triangle(self, position, rotation):
        forward = pygame.Vector2(0, 1).rotate(rotation)
        right = pygame.Vector2(0, 1).rotate(rotation + 90) * PLAYER_VISIBLE_RADIUS / 1.5
        a = position + forward * PLAYER_VISIBLE_RADIUS
        b = position - forward * PLAYER_VISIBLE_RADIUS - right
        c = position - forward * PLAYER_VISIBLE_RADIUS + right
        return [a, b, c]
    
    def draw(self, screen):
        self.draw_ghost_images(screen)
        pygame.draw.polygon(
            screen,
            self.color,
            self.triangle(self.position, self.rotation),
            2
        )

    def draw_ghost_images(self, screen):
        for i in range(0, len(self.ghost_image_length)):
            if self.ghost_image_length[i] <= PLAYER_GHOST_IMAGE_LENGTH:
                ghost_image_color = get_ghost_image_color(self.ghost_image_length[i])
                pygame.draw.polygon(
                    screen,
                    ghost_image_color,
                    self.triangle(self.ghost_image_position[i], self.ghost_image_rotation[i]),
                    2
                )

    def add_ghost_image(self):
        self.ghost_image_length.append(PLAYER_GHOST_IMAGE_LENGTH)
        self.ghost_image_position.append(self.position.copy())
        self.ghost_image_rotation.append(self.rotation)

    def reduce_ghost_image_length(self, index, dt):
        self.ghost_image_length[index] = self.ghost_image_length[index] - dt

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

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
        if keys[pygame.K_SPACE]:
            self.shoot(dt)
        
        for i in range(len(self.ghost_image_length) - 1, -1, -1):
            self.reduce_ghost_image_length(i, dt)
            if self.ghost_image_length[i] <= 0:
                del self.ghost_image_length[i]
                del self.ghost_image_position[i]
                del self.ghost_image_rotation[i]
        
        self.last_triggered_time += dt
        if self.last_triggered_time >= PLAYER_GHOST_IMAGE_FREQUENCY:
            self.last_triggered_time -= PLAYER_GHOST_IMAGE_FREQUENCY
            self.add_ghost_image()
            

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    
    def shoot(self, dt):
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.shot_flash_length = PLAYER_SHOT_FLASH_LENGTH
        shot = Shot(self.position[0], self.position[1])
        vector = pygame.Vector2(0, 1)
        vector = vector.rotate(self.rotation)
        shot.velocity = vector * PLAYER_SHOOT_SPEED