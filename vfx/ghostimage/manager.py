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
    def __init__(self, sprite_group, emitter):
        self.emitter = emitter
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

        self.registered_sprites = []
        self.emission_sources = []

    def update(self, dt):
        self.unregister_dead_sprites()
        self.register_alive_sprites()
        self.increment_emission_timers(dt)
        self.spawn_emissions()

    def get_ready_emission_sources(self):
        return (
            source for source
            in self.emission_sources
            if source.last_emission_time >= source.frequency
        )

    def register_sprite(self, sprite):
        self.registered_sprites.append(sprite)
        self.emission_sources.append(
            GhostImageSource(
                sprite,
                self.config[type(sprite)]
            )
        )

    def register_alive_sprites(self):
        for sprite in self.sprite_group:
            if sprite not in self.registered_sprites:
                self.register_sprite(sprite)

    def unregister_sprite(self, source):
        self.registered_sprites.remove(source.sprite)
        self.emission_sources.remove(source)

    def unregister_dead_sprites(self):
        for source in self.emission_sources:
            if source.sprite not in self.sprite_group:
                self.unregister_sprite(source)

    def increment_emission_timers(self, dt):
        for source in self.emission_sources:
            source.increment_last_emission_time(dt)
            
    def spawn_emissions(self):
        for source in self.get_ready_emission_sources():
            self.emitter.register_emission(
                source.create_emission()
            )
            source.reset_last_emission_time()