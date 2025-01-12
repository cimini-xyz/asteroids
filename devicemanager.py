from device import *
from constants import (
    PLAYER_SHOT_FLASH_LENGTH,
    PLAYER_SHOT_FLASH_INTENSITY
)


updatables = [
    generator_player_shot_flash := Generator(constant(PLAYER_SHOT_FLASH_INTENSITY)),
    impulse_player_shot_flash := Impulse(PLAYER_SHOT_FLASH_LENGTH),
    channel_player_shot_flash := Channel(),
    mixer_player_shot_flash := Mixer()
]
mixer_player_shot_flash.set_bus('asteroid')
mixer_player_shot_flash.set_bus('player')
mixer_player_shot_flash.set_bus('background', 1/64)
mixer_player_shot_flash.set_bus('star', 1/64)
channel_player_shot_flash.signal_combiner = max
generator_player_shot_flash.connect_to(impulse_player_shot_flash)
impulse_player_shot_flash.connect_to(channel_player_shot_flash)
channel_player_shot_flash.connect_to(mixer_player_shot_flash)

def hello(dt):
    for updatable in updatables:
        updatable.update(dt)
    print(
        mixer_player_shot_flash.evaluate_bus('asteroid'),
        mixer_player_shot_flash.evaluate_bus('player'),
        mixer_player_shot_flash.evaluate_bus('background'),
        mixer_player_shot_flash.evaluate_bus('star')
    )

def retrigger():
    impulse_player_shot_flash.reset()

def freeze():
    impulse_player_shot_flash.toggle_freeze()