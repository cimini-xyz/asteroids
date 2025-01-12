from enum import Enum, auto
from collections import deque

def clamp(value, min_value=0, max_value=1.0):
    return max(min_value, min(max_value, value))

def constant(value):
    return lambda t: value

class DeviceState(Enum):
    ALIVE = auto()
    FROZEN = auto()
    DISABLED = auto()
    DEAD = auto()

class Device:
    def __init__(self, signal_combiner=sum):
        self.state = DeviceState.ALIVE
        self.output_connections = []
        self.input_connections = []
        self.signal_combiner = signal_combiner

    def update(self, dt):
        if self.not_updateable():
            return
        return self._update(dt)

    def evaluate(self, t):
        if self.state in (DeviceState.DISABLED, DeviceState.DEAD):
            return 0
        if not isinstance(self, Generator) and not self.input_connections:
            return 0
        return self._evaluate(t)
    
    def not_updateable(self):
        return self.state in (DeviceState.FROZEN, DeviceState.DISABLED, DeviceState.DEAD)
    
    def _update(self, dt):
        raise NotImplementedError
    
    def _evaluate(self, t):
        raise NotImplementedError
    
    def remove(self):
        for output_device in self.output_connections.copy():
            output_device.input_connections.remove(self)
        for input_device in self.input_connections.copy():
            input_device.output_connections.remove(self)

    def connect_to(self, output_device):
        if output_device not in self.output_connections:
            self.output_connections.append(output_device)
        if self not in output_device.input_connections:
            output_device.input_connections.append(self)

    def disconnect_from(self, output_device):
        if output_device in self.output_connections:
            self.output_connections.remove(output_device)
        if self in output_device.input_connections:
            output_device.input_connections.remove(self)

    def get_signals(self, t):
        return (device.evaluate(t) for device in self.input_connections)
    
    def toggle_freeze(self):
        if self.state == DeviceState.FROZEN:
            self.state = DeviceState.ALIVE
            print("I am alive")
        else:
            self.state = DeviceState.FROZEN
            print("I am frozen")
        
class Generator(Device):
    def __init__(self, generator_func=constant):
        super().__init__()
        self.generator = generator_func

    def _update(self, dt):
        return

    def _evaluate(self, t):
        return self.generator(t)
    

class Impulse(Device):
    def __init__(self, length = 0.0, retrigger=False):
        super().__init__()
        self.length = length
        self._remaining = 0.0
        self.retrigger = retrigger

    def _evaluate(self, t):
        factor = self._remaining if self._remaining > 0 else 0
        return self.signal_combiner(self.get_signals(t)) * factor

    def _update(self, dt):
        if self.retrigger and self._remaining <= 0:
            self.reset()
        self._remaining = max(0, self._remaining - dt)

    def reset(self):
        if self.not_updateable():
            return
        self._remaining = self.length

class Channel(Device):
    def __init__(self):
        super().__init__()

    def _evaluate(self, t):
        return self.signal_combiner(self.get_signals(t))

    def _update(self, dt):
        pass  # If no update logic needed

class Mixer(Device):
    def __init__(self):
        super().__init__()
        self.bus = {}
    
    def set_bus(self, name, gain=1.0):
        if self.not_updateable():
            return
        self.bus[name] = gain

    def remove_bus(self, name):
        if self.not_updateable():
            return
        self.bus.pop(name, None)

    def evaluate_bus(self, name, t):
        factor = self.bus[name] if name in self.bus else 0.0
        return clamp(super().evaluate(t) * factor)

    def _evaluate(self, t):
        return self.signal_combiner(self.get_signals(t))

    def _update(self, dt):
        pass  # If no update logic needed
