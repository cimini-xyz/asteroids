from collections import defaultdict

from draw.none import draw_none
from draw.triangle import draw_triangle
from draw.circle import draw_circle

from player import Player
from shot import Shot
from constants import (
    PLAYER_GHOST_IMAGE_FREQUENCY,
    PLAYER_GHOST_IMAGE_LENGTH,
    PLAYER_GHOST_IMAGE_INTENSITY,
    SHOT_GHOST_IMAGE_FREQUENCY,
    SHOT_GHOST_IMAGE_LENGTH,
    SHOT_GHOST_IMAGE_INTENSITY
)

class GhostImageConfigEntry():
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

class GhostImageConfig():
    entries = defaultdict(
        GhostImageConfigEntry,
        {
            Player : GhostImageConfigEntry(
                draw_triangle,
                PLAYER_GHOST_IMAGE_FREQUENCY,
                PLAYER_GHOST_IMAGE_LENGTH,
                PLAYER_GHOST_IMAGE_INTENSITY
            ),
            Shot : GhostImageConfigEntry(
                draw_circle,
                SHOT_GHOST_IMAGE_FREQUENCY,
                SHOT_GHOST_IMAGE_LENGTH,
                SHOT_GHOST_IMAGE_INTENSITY
            )
        }
    )
    