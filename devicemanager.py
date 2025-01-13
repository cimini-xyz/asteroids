from device import *
from constants import (
    PLAYER_SHOT_FLASH_LENGTH,
    PLAYER_SHOT_FLASH_INTENSITY,
    ASTEROID_KILL_FLASH_LENGTH,
    ASTEROID_KILL_FLASH_INTENSITY,
    ASTEROID_SPLIT_FLASH_LENGTH,
    ASTEROID_SPLIT_FLASH_INTENSITY
)

from star import Star
from asteroid import Asteroid

def flatten_dict(d):
    result = []
    for value in d.values():
        if isinstance(value, dict):
            result.extend(flatten_dict(value))
        else:
            result.append(value)
    return result

def create_impulse_device_chain(label='impulse', intensity=1.0, length=1.0):
    generator = Generator(constant(intensity))
    impulse = Impulse(length)
    sendreturn = SendReturn()
    sendreturn.cache_signal_per_frame = False
    sendreturn.routes['star_' + label] = ['default']
    sendreturn.routes['background_' + label] = ['default']
    generator \
        .connect_to(impulse) \
        .connect_to(sendreturn)
    return {
            'generator' : generator,
            'impulse' : impulse,
            'sendreturn' : sendreturn
        }

def create_dynamic_flash_device_chain():
    device_chain = {}
    device_chain['player_shot_flash'] = create_impulse_device_chain(
        'player_shot_flash',
        PLAYER_SHOT_FLASH_INTENSITY,
        PLAYER_SHOT_FLASH_LENGTH)
    device_chain['asteroid_split_flash'] = create_impulse_device_chain(
        'asteroid_split_flash',
        ASTEROID_SPLIT_FLASH_INTENSITY,
        ASTEROID_SPLIT_FLASH_LENGTH)
    device_chain['asteroid_kill_flash'] = create_impulse_device_chain(
        'asteroid_kill_flash',
        ASTEROID_KILL_FLASH_INTENSITY,
        ASTEROID_KILL_FLASH_LENGTH)
    
    mixer = Mixer()
    limiter = Limiter()
    channel_combiner_star = ChannelCombiner()
    channel_combiner_background = ChannelCombiner()
    channel_combiner_default = ChannelCombiner()

    device_chain['mixer'] = mixer
    
    device_chain['cc_star'] = channel_combiner_star
    device_chain['cc_background'] = channel_combiner_background
    device_chain['cc_default'] = channel_combiner_default

    player_shot_flash_sendreturn = device_chain \
        ['player_shot_flash'] \
        ['sendreturn']
        
    asteroid_split_flash_sendreturn = device_chain \
        ['asteroid_split_flash'] \
        ['sendreturn'] \
    
    asteroid_kill_flash_sendreturn = device_chain \
        ['asteroid_kill_flash'] \
        ['sendreturn'] \

    player_shot_flash_sendreturn.connect_to(mixer, 'star_player_shot_flash')
    asteroid_split_flash_sendreturn.connect_to(mixer, 'star_asteroid_split_flash')
    asteroid_kill_flash_sendreturn.connect_to(mixer, 'star_asteroid_kill_flash')
    player_shot_flash_sendreturn.connect_to(mixer, 'background_player_shot_flash')
    asteroid_split_flash_sendreturn.connect_to(mixer, 'background_asteroid_split_flash')
    asteroid_kill_flash_sendreturn.connect_to(mixer, 'background_asteroid_kill_flash')

    player_shot_flash_sendreturn.connect_to(channel_combiner_default)
    asteroid_split_flash_sendreturn.connect_to(channel_combiner_default)
    asteroid_kill_flash_sendreturn.connect_to(channel_combiner_default)

    mixer.set_bus('star_player_shot_flash', 6/64)
    mixer.set_bus('star_asteroid_split_flash', 6/32)
    mixer.set_bus('star_asteroid_kill_flash', 6/22)
    mixer.set_bus('background_player_shot_flash', 3/64)
    mixer.set_bus('background_asteroid_split_flash', 3/32)
    mixer.set_bus('background_asteroid_kill_flash', 3/22)

    mixer.connect_to(channel_combiner_background, 'background_player_shot_flash')
    mixer.connect_to(channel_combiner_background, 'background_asteroid_split_flash')
    mixer.connect_to(channel_combiner_background, 'background_asteroid_kill_flash')
    mixer.connect_to(channel_combiner_star, 'star_player_shot_flash')
    mixer.connect_to(channel_combiner_star, 'star_asteroid_split_flash')
    mixer.connect_to(channel_combiner_star, 'star_asteroid_kill_flash')

    channel_combiner_background.connect_to(limiter, "background")
    channel_combiner_star.connect_to(limiter, "star")

    channel_combiner_default.connect_to(limiter)

    device_chain['limiter'] = limiter

    return device_chain

dynamic_flash_device_chain = create_dynamic_flash_device_chain()

updatables = flatten_dict(dynamic_flash_device_chain)

def hello(dt):
    for updatable in updatables:
        updatable.update(dt)
    #print(channel_player_shot_flash.evaluate())
    #print(get_player_shot_flash('star'))

def retrigger():
        dynamic_flash_device_chain \
        ['player_shot_flash'] \
        ['impulse'] \
            .reset()


def freeze():
    dynamic_flash_device_chain \
        ['player_shot_flash'] \
        ['impulse'] \
            .toggle_freeze()

def bypass():
        dynamic_flash_device_chain \
        ['player_shot_flash'] \
        ['impulse'] \
            .bypass()

def get_player_shot_flash(bus_name='default'):
    return dynamic_flash_device_chain['limiter'].evaluate(bus_name)