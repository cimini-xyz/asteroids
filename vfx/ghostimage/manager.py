from vfx.ghostimage.config import GhostImageConfig
from vfx.ghostimage.source import GhostImageSource


class GhostImageManager():
    def __init__(self, sprite_group, emitter):
        self.emitter = emitter
        self.sprite_group = sprite_group
        self.registered_sprites = []
        self.emission_sources = []
    
    # Main loop function
    def update(self, dt):
        self.unregister_dead_sprites()
        self.register_alive_sprites()
        self.increment_emission_timers(dt)
        self.spawn_emissions()

    # Getter
    def get_ready_emission_sources(self):
        """Returns all emission sources that are ready to generate an emission
        
        Returns:
            Generator of GhostImageSource objects whose timer has exceeded their frequency
        """
        return (
            source for source
            in self.emission_sources
            if source.last_emission_time >= source.frequency
        )

    # Registration methods
    # Base sprite registration
    def register_sprite(self, sprite):
        """Primary method for registering a single sprite and generating its emission source"""
        self.registered_sprites.append(sprite)
        self.emission_sources.append(
            GhostImageSource(
                sprite,
                GhostImageConfig.entries[type(sprite)]
            )
        )

    # Register all unregistered sprites
    def register_alive_sprites(self):
        """Registers all unregistered sprites that exist in sprite_group alongside their respective emission sources"""
        for sprite in self.sprite_group:
            if sprite not in self.registered_sprites:
                self.register_sprite(sprite)

    # Base sprite removal from registry
    def unregister_sprite(self, source):
        """Primary method to remove sprite and its emission source from registry"""
        self.registered_sprites.remove(source.sprite)
        self.emission_sources.remove(source)

    # Unregister all sprites that no longer exist
    def unregister_dead_sprites(self):
        """Unregisters sprites and its emission sources that no longer exist in their sprite group"""
        for source in self.emission_sources:
            if source.sprite not in self.sprite_group:
                self.unregister_sprite(source)

    # Emission creation and modification
    def increment_emission_timers(self, dt):
        """Increases all emission timers by delta time"""
        for source in self.emission_sources:
            source.increment_last_emission_time(dt)

    def spawn_emissions(self):
        """If emission timers pass their frequency threshold, generate an emission and reset timer"""
        for source in self.get_ready_emission_sources():
            self.emitter.register_emission(
                source.create_emission()
            )
            source.reset_last_emission_time()
