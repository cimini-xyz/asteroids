from signal import ConstantSignal 

class Processor():
    def __init__(self, signal):
        self._signal = signal
        
    def update(self, dt):
        """Update processor state"""
        raise NotImplementedError
        
    def evaluate(self, t=None):
        """Get current value"""
        raise NotImplementedError

class ImpulseProcessor(Processor):
    def __init__(self, length=0.0, value=0.0):
        super().__init__(ConstantSignal(value))
        self.length = length
        self._length_remaining = length

    def update(self, dt):
        self._reduce_length_remaining(dt)

    def evaluate(self, t=None):
        return self._signal.evaluate() * self._length_remaining
    
    def _reduce_length_remaining(self, dt):
        self._length_remaining = max(0, self._length_remaining - dt)