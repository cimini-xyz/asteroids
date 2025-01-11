class ColorChannel():
    def __init__(self, config, *, length = 0, intensity = 0, function = None):
        self.length = config.length if config and config.length else length
        self.length_remaining = config.length if config and config.length else length
        self.intensity = config.intensity if config and config.intensity else intensity
        self.function = config.function if config and config.function else self.empty_values

    def reduce_length_remaining(self, dt):
        if self.length_remaining:
            self.length_remaining = max(0, self.length_remaining - dt)
    
    def apply_impulse(self):
        self.length_remaining = self.length

    def empty_values():
        return (0, 0, 0)