import colorsys
from constants import PLAYER_SHOT_FLASH_INTENSITY

global_hue = 0.0
global_sat = 0.8
global_brightness = 0.8

def update_global_hue(dt):
    global global_hue 
    global_hue = (global_hue + 1.0 * dt / 8) % 1.0

def get_rgb_from_hue(hue_mod = 0.0, sat_mod = 0.0, bri_mod = 0.0):
    global global_hue
    global global_sat
    global global_brightness
    rgb = colorsys.hsv_to_rgb(
        max(0, min(1.0, (global_hue + hue_mod))),
        max(0,min(1.0, (global_sat + sat_mod))),
        max(0,min(1.0, (global_brightness + bri_mod)))
    )
    return tuple(int(255 * c) for c in rgb)

def update_sprite_color(sprite, player):
    flash_bright = get_shot_flash_brightness(player)
    color = get_rgb_from_hue(0.0, flash_bright, flash_bright)
    sprite.color = color

def get_background_color(player):
    flash_bright = get_shot_flash_brightness(player) / 64
    color = get_rgb_from_hue(0.0, flash_bright - 0.725, flash_bright - 0.725)
    return color

def get_shot_flash_brightness(player):
    return player.shot_flash_length * PLAYER_SHOT_FLASH_INTENSITY
    