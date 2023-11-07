import machine

class ControlInput:
    def __init__(self, name: str, pinNumber: int):
        self.name: str = name
        self.pin: Pin = Pin(pinNumber, Pin.IN, Pin.PULL_DOWN)
        self.on: bool = False
    
    def isOn(self):
        return self.on
    
class Button(ControlInput):
    def __init__(self, name: str, pinNumber: int):
        super().__init__(name, pinNumber)

