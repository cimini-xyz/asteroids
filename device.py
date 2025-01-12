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
    default_device_bus_name = 'default'
    def __init__(self, signal_combiner=sum):
        self.state = DeviceState.ALIVE
        self.connect = ConnectionMapping()
        self.device_map = DeviceMapping()
        self.signal_combiner = signal_combiner
        
    def update(self, dt):
        if self.not_updateable():
            return
        return self._update(dt)

    def evaluate(self, bus_name='default'):
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
    
    def _evaluate(self, bus_name='default'):
        raise NotImplementedError
    
    def disconnect_all_devices_from_device_map(self, device_map):
        tasks = []
        for connected_device in device_map:
            for bus_name in device_map[connected_device]:
                tasks.append((connected_device, bus_name))
        for task_args in tasks:
            self.disconnect_from(task_args[0], task_args[1])

    def remove(self):
        self.disconnect_all_devices_from_device_map(self.device_map.input)
        self.disconnect_all_devices_from_device_map(self.device_map.output)


    def get_connection_arguments(self, output_device, bus_name='default'):
        return [
            # Adds or discards target device [1] from source device output bus [0]
            (self.connect.output[bus_name], output_device),
            # Adds or discards source device [1] from target device input bus [0]
            (output_device.connect.input[bus_name], self),
            # Adds or discards bus name [1] from tarbus_nameget device 'source device -> in bus' map [0]
            (output_device.device_map.input[self], bus_name),
            # Adds or discards bus name [1] from source device 'target device -> in bus' map [0]
            (self.device_map.output[output_device], bus_name)
        ]
    
    def connect_to(self, output_device, bus_name='default'):
        args = self.get_connection_arguments(output_device, bus_name)
        for arg in args:
            arg[0].add(arg[1])
        return output_device

    def clean_entry_name(self, group, name):
        if not group[name]:
            del group[name]

    def clean_device_name(self, map, device_name):
        if not map[device_name]:
            del map[device_name]

    def disconnect_from(self, output_device, bus_name='default'):
        args = self.get_connection_arguments(output_device, bus_name)
        for arg in args:
            arg[0].discard(arg[1])
        self.clean_entry_name(self.connect.output, bus_name)
        self.clean_entry_name(output_device.connect.input, bus_name)
        self.clean_entry_name(self.device_map.output, output_device)
        self.clean_entry_name(output_device.device_map.input, self)
        return output_device


    def get_signals(self, bus_name='default'):
        return (device.evaluate(bus_name) for device in self.connect.input[bus_name])
    
    def toggle_freeze(self):
        if self.state == DeviceState.FROZEN:
            self.state = DeviceState.ALIVE
            print("I am alive")
        else:
            self.state = DeviceState.FROZEN
            print("I am freezy")
        
        

    def toggle_bypass(self):
        if self.state == DeviceState.DISABLED:
            self.state = DeviceState.ALIVE
            print("I am alive")
        else:
            self.state = DeviceState.DISABLED
            print("I am disabled")
    

class Generator(Device):
    def __init__(self, generator_func=constant):
        super().__init__()
        self.generator = generator_func

    def _update(self, dt):
        return

    def _evaluate(self, bus_name='default'):
        return self.generator() if self.connect.output[bus_name] else 0.0
    

class Impulse(Device):
    def __init__(self, length = 0.0, retrigger=False):
        super().__init__()
        self.length = length
        self._remaining = 0.0
        self.retrigger = retrigger

    def _evaluate(self, bus_name='default'):
        factor = self._remaining if self._remaining > 0 else 0
        return self.signal_combiner(self.get_signals(bus_name)) * factor

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

    def _evaluate(self, bus_name='default'):
        return self.signal_combiner(self.get_signals(bus_name))

    def _update(self, dt):
        pass  # If no update logic needed

class ChannelCombiner(Device):
    def __init__(self):
        super().__init__()
    
    def _evaluate(self, bus_name='default'):
        return self.signal_combiner(chain.from_iterable(list(self.get_signals(bus)) for bus in self.connect.input))
    
    def _update(self, dt):
        pass

class Mixer(Device):
    def __init__(self):
        super().__init__()
        self.bus_fader_gain = defaultdict(lambda: 1.0)

    def set_bus(self, bus_name, gain=1.0):
        self.bus_fader_gain[bus_name] = gain
        return self

    def evaluate_bus(self, bus_name='default'):
        if bus_name not in self.bus_fader_gain:
            return 0.0
        return self.evaluate() * self.bus_fader_gain[bus_name]

    def _evaluate(self, bus_name='default'):
        return self.signal_combiner(self.get_signals(bus_name))

    def _update(self, dt):
        pass 
