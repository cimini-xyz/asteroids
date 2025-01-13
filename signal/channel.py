class Channel():
    pass

class PeakDetectionChannel():
    def __init__(self):
        self.signals = []

    def update(self, dt):
        pass

    def evaluate(self, t=None):
        return max((signal.evalute() for signal in self.signals))