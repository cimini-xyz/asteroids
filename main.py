import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from globalhue import update_global_hue, update_sprite_color, get_background_color, reduce_asteroid_split_flash_remaining, reduce_asteroid_kill_flash_remaining
from screenfx import reduce_screen_shake_remaining, get_screen_shake
import random

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    world = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    global_hue = 0.0
    screen_offset_x = 0
    screen_offset_y = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    while True:
        #logic  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        for sprite in updatable:
            sprite.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collide(shot):
                    asteroid.split(dt)
                    shot.kill()
            
            if asteroid.collide(player):
                print("Game over!")
                exit()
        
        
        reduce_asteroid_split_flash_remaining(dt)
        reduce_asteroid_kill_flash_remaining(dt)
        reduce_screen_shake_remaining(dt)
        update_global_hue(dt)

        for sprite in drawable:
            update_sprite_color(sprite, player)
        
        #graphic
        world.fill(get_background_color(player))
        screen.fill(get_background_color(player))
        for sprite in drawable:
            sprite.draw(world)

        screen_offset_x += random.randint(-5,5)
        screen_offset_y += random.randint(-5,5)
        screen.blit(world, get_screen_shake(dt))
        
        #refresh
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()