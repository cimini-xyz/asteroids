class Signal():
    def __init__(self, value):
        self.value = value

    def evaluate(self, t):
        raise NotImplementedError()
    
class ConstantSignal(Signal):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, t=None):
        return self.value

class LinearVariableSignal(Signal):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, t):
        return self.value * t
    
class ExponentVariableSignal(Signal):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, t):
        return self.value ** t
