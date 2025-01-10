class GhostImageSource():
    def __init__(self, frequency, sprite, draw_function, length, intensity):
        self.frequency = frequency
        self.last_emission_time = 0
        self.draw_function = draw_function
        self.sprite = sprite
        self.length = length
        self.intensity = intensity

    def increment_last_emission_time(self, dt):
        self.last_emission_time += dt

    def reset_last_emission_time(self):
        self.last_emission_time -= self.frequency
