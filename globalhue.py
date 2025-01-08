import colorsys

global_hue = 0.0

def update_global_hue(dt):
    global global_hue 
    global_hue = (global_hue + 1.0 * dt / 8) % 1.0

def get_rgb_from_hue():
    global global_hue
    rgb = colorsys.hsv_to_rgb(global_hue, 1.0, 1.0)
    return tuple(int(255 * c) for c in rgb)

def update_sprite_color(sprite):
    color = get_rgb_from_hue()
    sprite.color = color