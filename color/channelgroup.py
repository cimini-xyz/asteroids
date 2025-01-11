from color.config import ColorConfig
from color.channel import ColorChannel
from collections import defaultdict

class ColorChannelGroup():
    def __init__(self):
        self.channels = defaultdict(ColorChannel)
        for key in ColorConfig.impulses.keys():
            self.channels[key] = ColorChannel(ColorConfig.impulses[key])
    
    def update(self, dt):
        for channel in self.get_channels():
            channel.reduce_length_remaining(dt)

    def get_channels(self):
        return (self.channels[key] for key in self.channels.keys())
    
    def get_channel_values(self):
        hue = 0.0
        sat = 0.0
        val = 0.0
        for channel in self.get_channels():
            hsv = channel.function(channel.length_remaining, channel.intensity)
            hue += hsv[0]
            sat += hsv[1]
            val += hsv[2]
        return (hue, sat, val)
            

    def send_impulse(self, impulse_key):
        self.channels[impulse_key].apply_impulse()

    