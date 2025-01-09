class GhostImageEmission():
    def __init__(self, length, intensity, position, rotation, draw_function):
        self.length = length
        self.length_remaining = length
        self.intensity = intensity
        self.position = position
        self.rotation = rotation
        self.draw_function = draw_function

    def reduce_length(self, dt):
        self.length_remaining = max(0, self.length_remaining - dt)
