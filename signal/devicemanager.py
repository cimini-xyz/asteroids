from device import *
from constants import (
    PLAYER_SHOT_FLASH_LENGTH,
    PLAYER_SHOT_FLASH_INTENSITY
)


generator = Generator()
impulse = Impulse(PLAYER_SHOT_FLASH_LENGTH)
channel = Channel()
channel.signal_combiner = max # peak detection, strongest signal is transmitted
mixer = Mixer()
mixer.set_bus('asteroid_player_shot_flash')
mixer.set_bus('player_player_shot_flash')
mixer.set_bus('background_player_shot_flash', 1/64)
mixer.set_bus('star_player_shot_flash', 1/64)
generator.connect_to(impulse)
impulse.connect_to(channel)
channel.connect_to_(mixer)

def hello():
    print(
        mixer.evaluate_bus('asteroid_player_shot_flash', PLAYER_SHOT_FLASH_INTENSITY),
        mixer.evaluate_bus('player_player_shot_flash', PLAYER_SHOT_FLASH_INTENSITY),
        mixer.evaluate_bus('background_player_shot_flash', PLAYER_SHOT_FLASH_INTENSITY),
        mixer.evaluate_bus('star_player_shot_flash', PLAYER_SHOT_FLASH_INTENSITY)
    )