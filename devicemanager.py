from device import *
from constants import (
    PLAYER_SHOT_FLASH_LENGTH,
    PLAYER_SHOT_FLASH_INTENSITY
)


updatables = [
    generator := Generator(constant(PLAYER_SHOT_FLASH_INTENSITY)),
    impulse := Impulse(PLAYER_SHOT_FLASH_LENGTH),
    channel := Channel(),
     # peak detection, strongest signal is transmitted
    mixer := Mixer()
]
mixer.set_bus('asteroid_player_shot_flash')
mixer.set_bus('player_player_shot_flash')
mixer.set_bus('background_player_shot_flash', 1/64)
mixer.set_bus('star_player_shot_flash', 1/64)
channel.signal_combiner = max
generator.connect_to(impulse)
impulse.connect_to(channel)
channel.connect_to(mixer)

def hello(dt):
    for updatable in updatables:
        updatable.update(dt)
    print(
        mixer.evaluate_bus('asteroid_player_shot_flash', 0),
        mixer.evaluate_bus('player_player_shot_flash', 0),
        mixer.evaluate_bus('background_player_shot_flash', 0),
        mixer.evaluate_bus('star_player_shot_flash', 0)
    )

def retrigger():
    impulse.reset()

def freeze():
    impulse.toggle_freeze()