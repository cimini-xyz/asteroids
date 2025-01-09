import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from globalhue import update_global_hue, update_sprite_color, get_background_color, reduce_asteroid_split_flash_remaining, reduce_asteroid_kill_flash_remaining, get_gridline_a_color, get_gridline_b_color, update_star_color
from screenfx import reduce_screen_shake_remaining, get_screen_shake
import random
from gridline import *
from star import Star
from starfield import StarField
from planet import Planet

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    starscreen= pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    world = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    clock = pygame.time.Clock()
    dt = 0
    global_hue = 0.0
    screen_offset_x = 0
    screen_offset_y = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    ghost_image = pygame.sprite.Group()

    Player.containers = (updatable, drawable, ghost_image)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    StarField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots, ghost_image)
    Star.containers = (updatable, stars)
    Planet.containers = (updatable, stars)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    starfield = StarField()
    star = Star(300, 300, 3)

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

        starscreen.fill((0, 0, 0, 0))
        for star in stars:
            update_star_color(star, player)
            star.draw(starscreen)

        
        #graphic
        world.fill((0, 0, 0, 0))
        
        screen.fill(get_background_color(player))
        for sprite in drawable:
            sprite.draw(world)

        screen_shake = get_screen_shake(dt)
        screen.blit(starscreen, screen_shake)
        screen.blit(world, screen_shake)
        
        
        
        #refresh
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()