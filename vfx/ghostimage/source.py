class GhostImageSource():
    def __init__(self, frequency, sprite):
        self.frequency = frequency
        self.last_emission_time = 0
        self.sprite = sprite

    def get_position(self):
        return self.sprite.position
    
    def get_rotation(self):
        return self.sprite.rotation
