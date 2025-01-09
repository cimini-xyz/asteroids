import colorsys
from constants import (
    BASE_GLOBAL_HUE,
    BASE_GLOBAL_BRIGHTNESS,
    BASE_GLOBAL_SAT,
    SCREEN_BACKGROUND_MODIFIER,
    GRIDLINE_A_MODIFIER,
    GRIDLINE_B_MODIFIER,
    PLAYER_SHOT_FLASH_INTENSITY, 
    PLAYER_GHOST_IMAGE_INTENSITY,
    ASTEROID_SPLIT_FLASH_INTENSITY, 
    ASTEROID_SPLIT_FLASH_LENGTH, 
    ASTEROID_KILL_FLASH_LENGTH, 
    ASTEROID_KILL_FLASH_INTENSITY
)



global_hue = BASE_GLOBAL_HUE
global_sat = BASE_GLOBAL_SAT
global_brightness = BASE_GLOBAL_BRIGHTNESS

asteroid_split_flash_remaining = 0.0
asteroid_kill_flash_remaining = 0.0

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
        max(0,min(1.0, (global_brightness + bri_mod))),
    )
    return tuple(int(255 * c) for c in rgb)

def update_sprite_color(sprite, player):
    flash_bright = (
        get_shot_flash_brightness(player) +
        get_asteroid_split_flash_brightness() +
        get_asteroid_kill_flash_brightness()
    )
    color = get_rgb_from_hue(0.0, flash_bright, flash_bright)
    sprite.color = color

def get_background_flash_bright(player, shot_mod = 64, split_mod = 32, kill_mod = 22):
    return (
        get_shot_flash_brightness(player) / shot_mod + 
        get_asteroid_split_flash_brightness() / split_mod + 
        get_asteroid_kill_flash_brightness() / kill_mod
    )

def get_background_color(player):
    background_modifier = SCREEN_BACKGROUND_MODIFIER
    flash_bright = get_background_flash_bright(player)
    color = get_rgb_from_hue(
        0.0,
        flash_bright + SCREEN_BACKGROUND_MODIFIER,
        flash_bright + SCREEN_BACKGROUND_MODIFIER 
    )
    return color

def get_gridline_a_color(player):
    flash_bright = get_background_flash_bright(player, 54, 28, 20)
    color = get_rgb_from_hue(
        0.0,
        flash_bright + GRIDLINE_A_MODIFIER - 3,
        flash_bright + GRIDLINE_A_MODIFIER
    )
    return color + (255,)

def get_gridline_b_color(player):
    flash_bright = get_background_flash_bright(player, 50, 30, 16)
    color = get_rgb_from_hue(
        0.0,
        flash_bright + GRIDLINE_B_MODIFIER - 2,
        flash_bright + GRIDLINE_B_MODIFIER + 1
    )
    return color + (255,)

def get_shot_flash_brightness(player):
    return player.shot_flash_length * PLAYER_SHOT_FLASH_INTENSITY

def reset_asteroid_split_flash_remaining():
    global asteroid_split_flash_remaining
    asteroid_split_flash_remaining = ASTEROID_SPLIT_FLASH_LENGTH

def reduce_asteroid_split_flash_remaining(dt):
    global asteroid_split_flash_remaining
    asteroid_split_flash_remaining = max(0, asteroid_split_flash_remaining - dt)

def get_asteroid_split_flash_brightness():
    return asteroid_split_flash_remaining * ASTEROID_SPLIT_FLASH_INTENSITY

def reset_asteroid_kill_flash_remaining():
    global asteroid_kill_flash_remaining
    asteroid_kill_flash_remaining = ASTEROID_KILL_FLASH_LENGTH

def reduce_asteroid_kill_flash_remaining(dt):
    global asteroid_kill_flash_remaining
    asteroid_kill_flash_remaining = max(0, asteroid_kill_flash_remaining - dt)

def get_asteroid_kill_flash_brightness():
    return asteroid_kill_flash_remaining * ASTEROID_KILL_FLASH_INTENSITY

def get_ghost_image_color(remaining_length):
    intensity = min(255, remaining_length * PLAYER_GHOST_IMAGE_INTENSITY)
    color = get_rgb_from_hue()
    return color + (intensity,)