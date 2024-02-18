import machine

# input to control
class ControlInput:
    def __init__(self, name: str, pinNumber: int):
        self.name: str = name
        self.pin: Pin = Pin(pinNumber, Pin.IN, Pin.PULL_DOWN)
    
    def isOn(self):
        return self.pin.value() == 1

# on or off
class Button(ControlInput):
    def __init__(self, name: str, pinNumber: int):
        super().__init__(name, pinNumber)

# on or off
class Switch(ControlInput):
    def __init__(self, name: str, pinNumber: int):
        super().__init__(name, pinNumber)
