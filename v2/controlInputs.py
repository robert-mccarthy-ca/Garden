import machine

# input to control
class ControlInput:
    def __init__(self, name: str, pinNumber: int):
        self.name: str = name
        self.pin: Pin = Pin(pinNumber, Pin.IN, Pin.PULL_DOWN)
    
    def isOn(self):
        return self.pin.value() == 1

# just a basic control, is on when pressed, only exists to provide a user friendly name
class Button(ControlInput):
    def __init__(self, name: str, pinNumber: int):
        super().__init__(name, pinNumber)

# just a basic control, is on when pressed, only exists to provide a user friendly name
class Trigger(ControlInput):
    def __init__(self, name: str, pinNumber: int):
        super().__init__(name, pinNumber)
