class ColorImpulse():
    def __init__(self, config, *, length = 0, intensity = 0, function):
        self.length = config.length if config and config.length else length
        self.length_remaining = config.length if config and config.length else length
        self.intensity = config.intensity if config and config.intensity else intensity
        self.function = config.function if config and self.function else function

    def reduce_length_remaining(self, dt):
        self.length_remaining = max(0, self.length_remaining - dt)