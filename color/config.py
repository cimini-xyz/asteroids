from constants import (
    BASE_GLOBAL_HUE,
    BASE_GLOBAL_SAT,
    BASE_GLOBAL_BRIGHTNESS,
    PLAYER_SHOT_FLASH_LENGTH,
    PLAYER_SHOT_FLASH_INTENSITY
)

from collections import defaultdict

def fill_value(value, dt):
    return 1.0

def cycle_value(value, dt):
    return (value + 1.0 * dt / 8) % 1.0

def fill_values(length, intensity):
    return (1.0, 1.0, 1.0)

#def player_shot_flash(length, intensity):
#    intensity *= length
#    return (0.0, intensity, intensity)


class ColorImpulseConfigEntry():
    def __init__(self, length=0, intensity=0, function=fill_values):
        self.length = length
        self.length_remaining = length
        self.intensity = intensity
        self.function = function

class ColorAnimationConfigEntry():
    def __init__(self, function=fill_value):
        self.function = function

class ColorConfig():
    base_hue = BASE_GLOBAL_HUE
    base_sat = BASE_GLOBAL_SAT
    base_val = BASE_GLOBAL_BRIGHTNESS

    impulses = defaultdict(
            ColorImpulseConfigEntry,
            {
                'player_shot_flash' : ColorImpulseConfigEntry(
                    length=PLAYER_SHOT_FLASH_LENGTH,
                    intensity=PLAYER_SHOT_FLASH_INTENSITY,
                    function=lambda t, x : (0.0, 0.0, 0.0) #player_shot_flash
                )
            }
        )
    animations = defaultdict(
            ColorAnimationConfigEntry,
            {
                'cycle' : ColorAnimationConfigEntry(
                    cycle_value
                )
            }
        )
