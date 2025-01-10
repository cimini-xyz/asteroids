from vfx.ghostimage.emitter import GhostImageEmitter
from vfx.ghostimage.config import GhostImageConfig
from vfx.ghostimage.source import GhostImageSource

from collections import defaultdict

from player import Player
from shot import Shot


from draw.triangle import draw_triangle
from draw.circle import draw_circle

from constants import (
    PLAYER_GHOST_IMAGE_FREQUENCY,
    PLAYER_GHOST_IMAGE_LENGTH,
    PLAYER_GHOST_IMAGE_INTENSITY,
    SHOT_GHOST_IMAGE_FREQUENCY,
    SHOT_GHOST_IMAGE_LENGTH,
    SHOT_GHOST_IMAGE_INTENSITY
)

class GhostImageManager():
    def __init__(self, sprite_group):
        self.emitter = GhostImageEmitter()
        self.sprite_group = sprite_group

        self.config = defaultdict(GhostImageConfig)
        self.config[Player] = GhostImageConfig(
            draw_triangle,
            PLAYER_GHOST_IMAGE_FREQUENCY,
            PLAYER_GHOST_IMAGE_LENGTH,
            PLAYER_GHOST_IMAGE_INTENSITY
            )
        self.config[Shot] = GhostImageConfig(
            draw_circle, 
            SHOT_GHOST_IMAGE_FREQUENCY,
            SHOT_GHOST_IMAGE_LENGTH,
            SHOT_GHOST_IMAGE_INTENSITY
            )

        self.seen = []
        self.sources = []

    def register_source(self, sprite):
        self.seen.append(sprite)
        self.sources.append(
            GhostImageSource(sprite, self.config[type(sprite)])
        )

    def unregister_source(self, source):
        self.seen.remove(source.sprite)
        self.sources.remove(source)

    def unregister_dead_sprites(self):
        for source in self.sources:
            if source.sprite not in self.sprite_group:
                self.unregister_source(source)

    def register_alive_sprites(self):
        for sprite in self.sprite_group:
            if sprite not in self.seen:
                self.register_source(sprite)

    def get_ready_sources(self):
        return (
            source for source
            in self.sources
            if source.last_emission_time >= source.frequency    
        )

    def spawn_emissions(self):
        for source in self.get_ready_sources():
            self.emitter.register_emission(source.create_emission())
            source.reset_last_emission_time()

    def increment_sources(self, dt):
        for source in self.sources:
            source.increment_last_emission_time(dt)

    def update(self, dt):
        self.unregister_dead_sprites()
        self.increment_sources(dt)
        self.register_alive_sprites()
        self.spawn_emissions()
        self.emitter.update(dt)
        

    def draw(self, screen):
        self.emitter.draw(screen)