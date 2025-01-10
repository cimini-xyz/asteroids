from draw.none import draw_none

class GhostImageSource():
    def __init__(self, sprite, config, *, draw_function=draw_none, frequency=60, length=1, intensity=50):
        self.sprite = sprite
        self.last_emission_time = 0

        self.draw_function = config.draw_function if config and config.draw_function else draw_function
        self.frequency = config.frequency if config and config.frequency else frequency
        self.length = config.length if config and config.length else length
        self.intensity = config.intensity if config and config.intensity else intensity
        
    def increment_last_emission_time(self, dt):
        self.last_emission_time += dt

    def reset_last_emission_time(self):
        self.last_emission_time %= self.frequency
