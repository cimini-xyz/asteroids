from globalhue import get_ghost_image_color 

class GhostImageEmitter():
    def __init__(self):
        self.emissions = []

    def register_emission(self, emission):
        self.emissions.append(emission)

    def unregister_emission(self, emission):
        self.emissions.remove(emission)

    def unregister_spent_emissions(self):
        for emission in self.get_spent_emissions():
            self.unregister_emission(emission)

    def get_spent_emissions(self):
        return (
            emission for emission
            in self.emissions
            if not emission.length_remaining
        )

    def reduce_emissions(self, dt):
        for emission in self.emissions:
            if emission.length_remaining:
                emission.reduce_length(dt)

    def update(self, dt):
        self.unregister_spent_emissions()
        self.reduce_emissions(dt)

    def draw(self, screen):
        for emission in self.emissions:
            if emission.length_remaining:
                emission.draw_function(
                    screen,
                    get_ghost_image_color(
                        emission.length_remaining,
                        emission.intensity,
                    ),
                    emission.position,
                    emission.rotation,
                    emission.radius
                )