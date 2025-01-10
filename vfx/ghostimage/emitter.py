from globalhue import get_ghost_image_color 
from vfx.ghostimage.emission import GhostImageEmission

class GhostImageEmitter():
    def __init__(self):
        self.emissions = []

    def register_emission(self, source):
        self.emissions.append(
            GhostImageEmission(
                source.length,
                source.intensity,
                source.sprite.position.copy(),
                source.sprite.rotation,
                source.draw_function,
                source.sprite.visible_radius
            )
        )

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