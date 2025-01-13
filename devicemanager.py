from device import *
from constants import (
    PLAYER_SHOT_FLASH_LENGTH,
    PLAYER_SHOT_FLASH_INTENSITY,
    ASTEROID_KILL_FLASH_LENGTH,
    ASTEROID_KILL_FLASH_INTENSITY,
    ASTEROID_SPLIT_FLASH_LENGTH,
    ASTEROID_SPLIT_FLASH_INTENSITY,
    SCREEN_BACKGROUND_MODIFIER
)

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
    #sendreturn.cache_signal_per_frame = False
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
    device_chain['player_shot'] = create_impulse_device_chain(
        'player_shot_flash',
        PLAYER_SHOT_FLASH_INTENSITY,
        PLAYER_SHOT_FLASH_LENGTH)
    device_chain['asteroid_split'] = create_impulse_device_chain(
        'asteroid_split_flash',
        ASTEROID_SPLIT_FLASH_INTENSITY,
        ASTEROID_SPLIT_FLASH_LENGTH)
    device_chain['asteroid_kill'] = create_impulse_device_chain(
        'asteroid_kill',
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
        ['player_shot'] \
        ['sendreturn']
        
    asteroid_split_flash_sendreturn = device_chain \
        ['asteroid_split'] \
        ['sendreturn'] \
    
    asteroid_kill_flash_sendreturn = device_chain \
        ['asteroid_kill'] \
        ['sendreturn'] \

    player_shot_flash_sendreturn.connect_to(mixer, 'star_player_shot_flash')
    asteroid_split_flash_sendreturn.connect_to(mixer, 'star_asteroid_split_flash')
    asteroid_kill_flash_sendreturn.connect_to(mixer, 'star_asteroid_kill_flash')
    player_shot_flash_sendreturn.connect_to(mixer, 'background_player_shot_flash')
    asteroid_split_flash_sendreturn.connect_to(mixer, 'background_asteroid_split_flash')
    asteroid_kill_flash_sendreturn.connect_to(mixer, 'background_asteroid_kill_flash')

    mixer.set_bus('star_player_shot_flash', 6/64) # 6
    mixer.set_bus('star_asteroid_split_flash', 6/32) # 6
    mixer.set_bus('star_asteroid_kill_flash', 6/22) # 6
    mixer.set_bus('background_player_shot_flash', 2/64) # 3
    mixer.set_bus('background_asteroid_split_flash', 2/32) # 3
    mixer.set_bus('background_asteroid_kill_flash', 2/22) # 3

    mixer.connect_to(channel_combiner_background, 'background_player_shot_flash')
    mixer.connect_to(channel_combiner_background, 'background_asteroid_split_flash')
    mixer.connect_to(channel_combiner_background, 'background_asteroid_kill_flash')
    mixer.connect_to(channel_combiner_star, 'star_player_shot_flash')
    mixer.connect_to(channel_combiner_star, 'star_asteroid_split_flash')
    mixer.connect_to(channel_combiner_star, 'star_asteroid_kill_flash')

    player_shot_flash_sendreturn.connect_to(channel_combiner_default)
    asteroid_split_flash_sendreturn.connect_to(channel_combiner_default)
    asteroid_kill_flash_sendreturn.connect_to(channel_combiner_default)

    
    

    sendreturn = SendReturn()
    sub_mixer = SubtractiveMixer()

    device_chain['sendreturn'] = sendreturn
    device_chain['sub_mixer'] = sub_mixer

    #sendreturn.cache_signal_per_frame = False# cache_sample_per_update

    channel_combiner_background.connect_to(sendreturn, "background")
    channel_combiner_star.connect_to(sendreturn, "star")
    channel_combiner_default.connect_to(sendreturn)

    sendreturn.routes['background_sat'] = ['background']
    sendreturn.routes['background_val'] = ['background']
    sendreturn.routes['star_sat'] = ['star']
    sendreturn.routes['star_val'] = ['star']

    

    sendreturn.connect_to(sub_mixer, "background_sat")
    sendreturn.connect_to(sub_mixer, "background_val")
    sendreturn.connect_to(sub_mixer, "star_sat")
    sendreturn.connect_to(sub_mixer, "star_val")
    sendreturn.connect_to(sub_mixer)

    
    sub_mixer.set_bus('background_sat', SCREEN_BACKGROUND_MODIFIER)
    sub_mixer.set_bus('background_val', SCREEN_BACKGROUND_MODIFIER)
    sub_mixer.set_bus('star_sat', - 0.1)
    sub_mixer.set_bus('star_val', SCREEN_BACKGROUND_MODIFIER + 0.162) 
 
    sub_mixer.connect_to(limiter, 'background_sat')
    sub_mixer.connect_to(limiter, 'background_val')
    sub_mixer.connect_to(limiter, 'star_sat')
    sub_mixer.connect_to(limiter, 'star_val')

    device_chain['limiter'] = limiter

    return device_chain

dynamic_flash_device_chain = create_dynamic_flash_device_chain()

updatables = flatten_dict(dynamic_flash_device_chain)

def hello(dt):
    for updatable in updatables:
        updatable.update(dt)
    #print(channel_player_shot_flash.evaluate())
    #print(get_player_shot_flash('star'))

def retrigger_player_shot():
        dynamic_flash_device_chain \
        ['player_shot'] \
        ['impulse'] \
            .reset()

def retrigger_asteroid_split():
    dynamic_flash_device_chain \
        ['asteroid_split'] \
        ['impulse'] \
            .reset()

def retrigger_asteroid_kill():
    dynamic_flash_device_chain \
        ['asteroid_kill'] \
        ['impulse'] \
            .reset()

def freeze():
    dynamic_flash_device_chain \
        ['player_shot'] \
        ['impulse'] \
            .toggle_freeze()

def bypass():
        dynamic_flash_device_chain \
        ['player_shot'] \
        ['impulse'] \
            .bypass()

def get_dynamic_flash(bus_name='default'):
    return dynamic_flash_device_chain['limiter'].evaluate(bus_name)
