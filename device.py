from enum import Enum, auto
from collections import deque, defaultdict
from itertools import chain

def clamp(value, min_value=0, max_value=1.0):
    return max(min_value, min(max_value, value))

def constant(value):
    def func():
        return value
    return func

class DeviceState(Enum):
    ALIVE = auto()
    FROZEN = auto()
    DISABLED = auto()
    DEAD = auto()

class ConnectionMapping():
    def __init__(self):
        self.input = defaultdict(set)
        self.output = defaultdict(set)

class DeviceMapping():
    def __init__(self):
        self.input = defaultdict(set)
        self.output = defaultdict(set)

class Device:
    def __init__(self, signal_combiner=sum):
        self.state = DeviceState.ALIVE
        self.connect = ConnectionMapping()
        self.device_map = DeviceMapping()
        self.signal_combiner = signal_combiner
        
    def update(self, dt):
        if self.not_updateable():
            return
        return self._update(dt)

    def evaluate(self, bus_name=None):
        if self.state is DeviceState.DEAD:
            return 0
        if not isinstance(self, Generator) and not self.connect.input:
            return 0
        if self.state is DeviceState.DISABLED:
            return sum(self.get_signals(bus_name))
        return self._evaluate(bus_name)
    
    def not_updateable(self):
        return self.state in (DeviceState.FROZEN, DeviceState.DISABLED, DeviceState.DEAD)
    
    def _update(self, dt):
        raise NotImplementedError
    
    def _evaluate(self, bus_name=None):
        raise NotImplementedError
    
    def disconect_all_devices_from_device_map(self, device_map):
        for connected_device, bus_names in list(device_map.items()):
            for bus_name in bus_names:
                connected_device.disconnect_from(self, bus_name)

    def remove(self):
        self.disconnect_all_devices_from_device_map(self.device_map.input)
        self.disconnect_all_devices_from_device_map(self.device_map.output)


    def get_connection_arguments(self, output_device, bus_name=None):
        return [
            # Adds or discards target device [1] from source device output bus [0]
            (self.connect.output[bus_name], output_device),
            # Adds or discards source device [1] from target device input bus [0]
            (output_device.connect.input[bus_name], self),
            # Adds or discards bus name [1] from target device 'source device -> in bus' map [0]
            (output_device.device_map.input[self], bus_name),
            # Adds or discards bus name [1] from source device 'target device -> in bus' map [0]
            (self.device_map.output[output_device], bus_name)
        ]
    
    def connect_to(self, output_device, bus_name=None):
        args = self.get_connection_arguments(output_device, bus_name)
        for arg in args:
            arg[0].add(arg[1])

    def disconnect_from(self, output_device, bus_name=None):
        args = self.get_connection_arguments(output_device, bus_name)
        for arg in args:
            arg[0].discard(arg[1])

    def get_signals(self, bus_name=None):
        return (device.evaluate(bus_name) for device in self.connect.input[bus_name])
    
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

    def _evaluate(self, bus_name=None):
        return self.generator() if self.connect.output[bus_name] else 0.0
    

class Impulse(Device):
    def __init__(self, length = 0.0, retrigger=False):
        super().__init__()
        self.length = length
        self._remaining = 0.0
        self.retrigger = retrigger

    def _evaluate(self, bus_name=None):
        factor = self._remaining if self._remaining > 0 else 0
        return self.signal_combiner(self.get_signals()) * factor

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

    def _evaluate(self, bus_name=None):
        return self.signal_combiner(self.get_signals(bus_name))

    def _update(self, dt):
        pass  # If no update logic needed

class Mixer(Device):
    def __init__(self):
        super().__init__()
        self.fader = {}
        self.bus = {}

    def set_bus(self, bus_name, gain=1.0):
        self.bus[bus_name] = gain

    def evaluate_bus(self, bus_name):
        if bus_name not in self.bus:
            return 0.0
        return self.evaluate() * self.bus[bus_name]

    def _evaluate(self, bus_name = None):
        return self.signal_combiner(self.get_signals())

    def _update(self, dt):
        pass  # If no update logic needed
