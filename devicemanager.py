from device import *
from constants import (
    PLAYER_SHOT_FLASH_LENGTH,
    PLAYER_SHOT_FLASH_INTENSITY
)


updatables = [
    generator2 := Generator(constant(PLAYER_SHOT_FLASH_INTENSITY*3)),
    generator_player_shot_flash := Generator(constant(PLAYER_SHOT_FLASH_INTENSITY)),
    impulse_player_shot_flash := Impulse(PLAYER_SHOT_FLASH_LENGTH),
    channel_player_shot_flash := Channel(),
    mixer_player_shot_flash := Mixer()
]

for device in updatables:
    print("This device is: ", device)
    for device_in in device.device_map.output:
        print("This output device is: ", device_in)
        print("These are the busses: ", device.device_map.output[device_in])
    print(":)")

mixer_player_shot_flash \
    .set_bus('asteroid') \
    .set_bus('player') \
    .set_bus('background', 1/64) \
    .set_bus('star', 1/64) \
    .signal_combiner = max

generator_player_shot_flash \
    .connect_to(impulse_player_shot_flash) \
    .connect_to(channel_player_shot_flash) \
    .connect_to(mixer_player_shot_flash)


generator2 \
    .connect_to(impulse_player_shot_flash, bus_name='asdf') \
    .connect_to(channel_player_shot_flash, bus_name='asdf') \
    .connect_to(mixer_player_shot_flash, bus_name='asdf')



print("Newly connected")
for device in updatables:
    print("This device is: ", device)
    for device_in in device.device_map.output:
        print("This output device is: ", device_in)
        print("These are the busses: ", device.device_map.output[device_in])
    print(":)")

#print("Everything should be removed")
#generator2.remove()
#generator_player_shot_flash.remove()
#impulse_player_shot_flash.remove()
#channel_player_shot_flash.remove()
#mixer_player_shot_flash.remove()

generator_player_shot_flash.disconnect_from(impulse_player_shot_flash)
impulse_player_shot_flash.disconnect_from(channel_player_shot_flash)
channel_player_shot_flash.disconnect_from(mixer_player_shot_flash)

for device in updatables:
    print("This device is: ", device)
    for device_in in device.device_map.output:
        print("This output device is: ", device_in)
        print("These are the busses: ", device.device_map.output[device_in])
    print(":)")

updatables = [
    generator2 := Generator(constant(PLAYER_SHOT_FLASH_INTENSITY*3)),
    generator_player_shot_flash := Generator(constant(PLAYER_SHOT_FLASH_INTENSITY)),
    impulse_player_shot_flash := Impulse(PLAYER_SHOT_FLASH_LENGTH),
    channel_player_shot_flash := Channel(),
    mixer_player_shot_flash := Mixer(),
    channel_combiner := ChannelCombiner(),
    generator_3 := Generator(constant(PLAYER_SHOT_FLASH_INTENSITY/2))
]
mixer_player_shot_flash \
    .set_bus('asteroid') \
    .set_bus('player') \
    .set_bus('background', 1/64) \
    .set_bus('star', 1/64) \
    .signal_combiner = max

generator_player_shot_flash \
    .connect_to(impulse_player_shot_flash) \
    .connect_to(channel_player_shot_flash) \
    .connect_to(mixer_player_shot_flash)

generator2 \
    .connect_to(impulse_player_shot_flash, bus_name='asdf') \
    .connect_to(channel_player_shot_flash, bus_name='asdf') \
    .connect_to(mixer_player_shot_flash, bus_name='asdf')


#generator_3.connect_to(channel_player_shot_flash, "asdf")
channel_player_shot_flash.connect_to(channel_combiner)
channel_player_shot_flash.connect_to(channel_combiner, bus_name="asdf")
channel_combiner.signal_combiner=sum

channel_combiner.connect_to(mixer_player_shot_flash, "combined_channels")

def hello(dt):
    for updatable in updatables:
        updatable.update(dt)
    print(
        mixer_player_shot_flash.evaluate_bus('asteroid'),
        mixer_player_shot_flash.evaluate_bus('player'),
        mixer_player_shot_flash.evaluate_bus('background'),
        mixer_player_shot_flash.evaluate_bus('star')
    )
    print(
        mixer_player_shot_flash.evaluate('asdf')
    )
    print(
        mixer_player_shot_flash.evaluate('combined_channels')
    )

def retrigger():
    impulse_player_shot_flash.reset()

def freeze():
    impulse_player_shot_flash.toggle_freeze()

def bypass():
    impulse_player_shot_flash.toggle_bypass()