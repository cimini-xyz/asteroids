from constants import (
    SCREEN_SHAKE_MAX_OFFSET_X,
    SCREEN_SHAKE_MAX_OFFSET_Y,
    SCREEN_SHAKE_ASTEROID_SPLIT_LENGTH,
    SCREEN_SHAKE_ASTEROID_SPLIT_INTENSITY,
    SCREEN_SHAKE_ASTEROID_KILL_LENGTH,
    SCREEN_SHAKE_ASTEROID_KILL_INTENSITY
)
import random
import math

screen_shake_length_remaining = 0.0
screen_shake_intensity = 0.0
screen_shake_time = 0.0

def get_screen_shake(dt):
    global screen_shake_length_remaining, screen_shake_time

    if screen_shake_length_remaining <= 0:
        # Reset time for when a new shake begins
        screen_shake_time = 0.0
        return (0, 0)

    intensity = screen_shake_intensity * screen_shake_length_remaining

    # Increment elapsed time to control oscillation
    screen_shake_time += dt

    # Use smooth oscillation for offsets
    screen_offset_x = math.sin(screen_shake_time * 10) * intensity / 1.14
    screen_offset_y = math.cos(screen_shake_time * 10) * intensity / 1.2

    jitter_mod_x = random.uniform(max(-intensity, SCREEN_SHAKE_MAX_OFFSET_X), min(intensity, SCREEN_SHAKE_MAX_OFFSET_X)) // 7
    jitter_mod_y = random.uniform(max(-intensity, SCREEN_SHAKE_MAX_OFFSET_X), min(intensity, SCREEN_SHAKE_MAX_OFFSET_X)) // 12
    # Clamp the offsets
    screen_offset_x = max(-SCREEN_SHAKE_MAX_OFFSET_X, min(screen_offset_x, SCREEN_SHAKE_MAX_OFFSET_X)) + jitter_mod_x
    screen_offset_y = max(-SCREEN_SHAKE_MAX_OFFSET_Y, min(screen_offset_y, SCREEN_SHAKE_MAX_OFFSET_Y)) + jitter_mod_y

    return (screen_offset_x, screen_offset_y)


def reduce_screen_shake_remaining(dt):
    global screen_shake_length_remaining
    screen_shake_length_remaining = max(0, screen_shake_length_remaining - dt)

def reset_screen_shake_asteroid_split():
    global screen_shake_length_remaining
    global screen_shake_intensity
    screen_shake_length_remaining = SCREEN_SHAKE_ASTEROID_SPLIT_LENGTH
    screen_shake_intensity = SCREEN_SHAKE_ASTEROID_SPLIT_INTENSITY

def reset_screen_shake_asteroid_kill():
    global screen_shake_length_remaining
    global screen_shake_intensity
    if SCREEN_SHAKE_ASTEROID_KILL_LENGTH > screen_shake_length_remaining:
        screen_shake_length_remaining = SCREEN_SHAKE_ASTEROID_KILL_LENGTH
    if SCREEN_SHAKE_ASTEROID_KILL_INTENSITY > screen_shake_intensity:
        screen_shake_intensity = SCREEN_SHAKE_ASTEROID_KILL_INTENSITY