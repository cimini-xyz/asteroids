from draw.none import draw_none


class GhostImageConfig():
    def __init__(
            self,
            draw_function=draw_none,
            frequency=60,
            length=1,
            intensity=50
    ):
        self.draw_function = draw_function
        self.frequency = frequency
        self.length = length
        self.intensity = intensity