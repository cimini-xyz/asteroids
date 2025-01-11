from vfx.screenshake.config import ScreenShakeConfig
from vfx.screenshake.impulse import ScreenShakeImpulse
from vfx.screenshake.strategy import ScreenShakeGroupStrategy, ScreenShakeImpulseStrategy
import random
import math

class ScreenShakeManager():
    _instance = None
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.impulses = []
        self.elapsed_time = 0.0
        self.offset = (0, 0)

    def update(self, dt):
        self.elapsed_time += dt
        self.apply_impulses()
        self.reduce_impulses(dt)
        if not self.impulses:
            self.elapsed_time = 0.0
        


    def send_impulse(self, impulse_key):
        self.impulses.append(
            ScreenShakeImpulse(
                ScreenShakeConfig.impulses[impulse_key]
            )
        )
    
    def reduce_impulses(self, dt):
        for impulse in self.impulses:
            impulse.reduce_length_remaining(dt)
            if impulse.length_remaining <= 0:
                self.impulses.remove(impulse)

    def apply_impulses(self):
        intensity = (
            ScreenShakeGroupStrategy.
            current_strategy(
                self.impulses
            )
        )
        self.offset = (
            ScreenShakeImpulseStrategy.
            current_strategy(
                self.elapsed_time,
                intensity,
                ScreenShakeConfig.offset_mods,
                ScreenShakeConfig.max_offset
            )
        )