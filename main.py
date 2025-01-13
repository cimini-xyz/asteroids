import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
#from globalhue import update_global_hue, update_sprite_color, get_background_color, reduce_asteroid_split_flash_remaining, reduce_asteroid_kill_flash_remaining, get_gridline_a_color, get_gridline_b_color, update_star_color
import random
from star import Star
from starfield import StarField
from planet import Planet
from vfx.ghostimage.manager import GhostImageManager
from vfx.ghostimage.emitter import GhostImageEmitter
from vfx.screenshake.manager import ScreenShakeManager
from color.manager import ColorManager
from devicemanager import hello, freeze, bypass

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

    sprite_updatables = pygame.sprite.Group()
    sprite_drawables = pygame.sprite.Group()
    sprite_colorables = pygame.sprite.Group()
    ghost_image = pygame.sprite.Group()

    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    

    Player.containers = (sprite_updatables, sprite_drawables, sprite_colorables, ghost_image)
    Asteroid.containers = (sprite_updatables, sprite_drawables, sprite_colorables, asteroids)
    AsteroidField.containers = (sprite_updatables)
    StarField.containers = (sprite_updatables)
    Shot.containers = (sprite_updatables, sprite_drawables, sprite_colorables, shots, ghost_image)
    Star.containers = (sprite_updatables, sprite_colorables, stars)
    Planet.containers = (sprite_updatables, sprite_colorables, stars)
    

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    starfield = StarField()

    color_manager = ColorManager(sprite_colorables)
    player.color_manager = color_manager
    ghost_image_emitter = GhostImageEmitter()
    ghost_image_manager = GhostImageManager(ghost_image, ghost_image_emitter)
    updatables = [
        color_manager,
        ghost_image_manager,
        ghost_image_emitter,
        ScreenShakeManager().get_instance(),
    ]
    drawables = [
        ghost_image_emitter
    ]
    
    #counter = 0
    #t = 0
    while True:
        hello(dt)
        #print(dt)
        #logic
        #t += dt
        #hello(dt)
        #if t > 1:
            #if counter == 3:
            #    bypass()
            #if counter == 2:
            #    bypass()
            #if counter == 1:
            #    freeze()
            #if counter == 0:
            #    freeze()
            #counter = (counter + 1) % 4
            
            #t = 0
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    

        
        for sprite in sprite_updatables:
            sprite.update(dt)
        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collide(shot):
                    asteroid.split(dt)
                    shot.kill()
            
            if asteroid.collide(player):
                print("Game over!")
                exit()
        
        for updatable in updatables:
            updatable.update(dt)

        #reduce_asteroid_split_flash_remaining(dt)
        #reduce_asteroid_kill_flash_remaining(dt)
        #update_global_hue(dt)

        for sprite in sprite_drawables:
            pass
            #update_sprite_color(sprite, player)

        starscreen.fill((0, 0, 0, 0))
        world.fill((0, 0, 0, 0))
        for star in stars:
            pass
            #update_star_color(star, player)
            star.draw(world)

        
        #graphic
        
        
        screen.fill(color_manager.background_color)#get_background_color(player))
        for drawable in drawables:
            drawable.draw(world)
        for sprite in sprite_drawables:
            sprite.draw(world)

        screen_shake = ScreenShakeManager.get_instance().offset
        screen.blit(starscreen, screen_shake)
        screen.blit(world, screen_shake)
        
        
        
        #refresh
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()