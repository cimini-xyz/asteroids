from constants import (
    SCREEN_SHAKE_MAX_OFFSET_X,
    SCREEN_SHAKE_MAX_OFFSET_Y,
    SCREEN_SHAKE_UNIFORM_X_MOD,
    SCREEN_SHAKE_UNIFORM_Y_MOD,
    SCREEN_SHAKE_JITTER_X_MOD,
    SCREEN_SHAKE_JITTER_Y_MOD,
    SCREEN_SHAKE_ASTEROID_SPLIT_LENGTH,
    SCREEN_SHAKE_ASTEROID_SPLIT_INTENSITY,
    SCREEN_SHAKE_ASTEROID_KILL_LENGTH,
    SCREEN_SHAKE_ASTEROID_KILL_INTENSITY
)

from collections import defaultdict


class ScreenShakeConfigEntry():
    def __init__(self, length = 0, intensity = 0):
        self.length = length
        self.intensity = intensity

class ScreenShakeConfig():
    max_offset = {
        'x' : SCREEN_SHAKE_MAX_OFFSET_X,
        'y' : SCREEN_SHAKE_MAX_OFFSET_Y
    }

    offset_mods = {
        'uniform_x_mod' : 1 / SCREEN_SHAKE_UNIFORM_X_MOD,
        'uniform_y_mod' : 1 / SCREEN_SHAKE_UNIFORM_Y_MOD,
        'jitter_x_mod' : 1 / SCREEN_SHAKE_JITTER_X_MOD,
        'jitter_y_mod' : 1 / SCREEN_SHAKE_JITTER_Y_MOD
    }

    impulses = defaultdict(
        ScreenShakeConfigEntry,
        {
            'asteroid_split' : ScreenShakeConfigEntry(
                length = SCREEN_SHAKE_ASTEROID_SPLIT_LENGTH,
                intensity = SCREEN_SHAKE_ASTEROID_SPLIT_INTENSITY
            ),
            'asteroid_kill' : ScreenShakeConfigEntry(
                length = SCREEN_SHAKE_ASTEROID_KILL_LENGTH,
                intensity = SCREEN_SHAKE_ASTEROID_KILL_INTENSITY
            )
        }
    )