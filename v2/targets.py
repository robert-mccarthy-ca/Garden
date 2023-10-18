import machine

# The ControlTarget is considered on if 1 or more controllers have requested it to be on and none have requested it to be disabled
# - multiple controls can be linked to the same target
# - this allows for both multiple on sources such as a timer/thermostat fan controller as well as disable sources like a pause button for maintenance
# - not thread safe
class ControlTarget:
    # Args:
    #   name: str - name of this control
    #   pinNumber: int - the pin number on the Pico W
    def __init__(self, name: str, pinNumber: int):
        self.pinNumber: int = pinNumber
        self.pin: Pin = Pin(pinNumber, Pin.OUT, Pin.PULL_DOWN)
        self.on: bool = False
        self.name: str = name
        self.controllerOnList: list = []
        self.controllerDisabledList: list = []
    
    # Args:
    #   controlName: str - name of the calling Controller
    def on(self, controlName: str):
        if isDisabled():
            return
        
        self.controllerOnList[controlName] = True
        if not self.on:
            wasOff: bool = any(self.controllerOnList)
            self.on = True
            if wasOff:
                self.pin.toggle()
    
    # Args:
    #   controlName: str - name of the calling controller
    def off(self, controlName: str):
        if isDisabled():
            return
        
        self.controllerOnList[controlName] = False
        if self.on and any(self.controllerOnList):
            self.on = False
            self.pin.toggle()
            
    # Args:
    #   message: str - message to log, appended to the logPrefix with a timestamp
    def log(self, message: str):
        print(self.logPrefix, time.time(), ' - ', message)
    
    def isDisabled(self):
        return any(self.controllerDisabledList)
    
    def disable(self, controlName: str):
        wasDisabled: bool = isDisabled()
        self.controllerDisabledList[controlName] = True
        if not wasDisabled and self.on():
            self.pin.toggle()
    
    def enable(self, controlName: str):
        wasDisabled: bool = isDisabled()
        self.controllerDisabledList[controlName] = False
        disabledNow: bool = isDisabled()
        if wasDisabled and not disabledNow and self.on:
            self.pin.toggle()

class SolidStateRelay(ControlTarget):
    def __init__(self, pinNumber, name):
        super().__init__(pinNumber, name)
        self.pin.off()
    
    def __str__(self):
        return 'Solid State Relay, operating on pin ' + str(self.pinNumber)

class Solenoid(ControlTarget):
    def __init__(self, pinNumber: int, name: str):
        super().__init__(pinNumber, name)
        self.pin.on()
    
    def __str__(self):
        return 'Solenoid, operating on pin ' + str(self.pinNumber)
















