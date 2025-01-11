import colorsys
from color.config import ColorConfig
from color.impulse import ColorImpulse
from color.channelgroup import ColorChannelGroup

def clamp(value, min_value=0, max_value=1.0):
    return max(min_value, min(max_value, value))


class ColorManager():
    def __init__(self, sprite_group):
        self.config = ColorConfig()
        self.hue = self.config.base_hue
        self.sat = self.config.base_sat
        self.val = self.config.base_val
        self.sprite_group = sprite_group
        self.hue_animation = (
            self.
            config.
            animations
            ['cycle']
        )
        self.impulses = []
        self.channels = ColorChannelGroup()

    def update(self, dt):
        self.update_hue(dt)
        self.channels.update(dt)
        self.update_sprites()

    def update_hue(self, dt):
        self.hue = self.hue_animation.function(self.hue, dt)

    def update_sprite_color(self, sprite):
        combined_hsv = self.get_combined_hsv()
        print(combined_hsv)
        sprite.color = self.get_rgb(combined_hsv[0], combined_hsv[1], combined_hsv[2])

    def update_sprites(self):
        for sprite in self.sprite_group:
            self.update_sprite_color(sprite)

    def get_base_hsv(self):
        return (self.hue, self.sat, self.val)
    
    def get_channel_hsv(self):
        self.channels.get_channel_values()

    def get_combined_hsv(self):
        base_hsv = self.get_base_hsv()
        channel_hsv = self.channels.get_channel_values()
        return (clamp(base_hsv[0] + channel_hsv[0]), clamp(base_hsv[1] + channel_hsv[1]), clamp(base_hsv[2] + channel_hsv[2]))

    def get_rgb(self, hue, sat, val):
        rgb = colorsys.hsv_to_rgb(
            hue,
            sat,
            val
        )
        return tuple(int(255 * c) for c in rgb)
    
    def send_impulse(self, impulse_key):
        self.channels.send_impulse(impulse_key)
    
