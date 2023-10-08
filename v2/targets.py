import machine
from builtins import False

# multiple controls can be linked to the same target
# not thread safe
class ControlTarget:
    def __init__(self, name, pinNumber):
        self.pinNumber = pinNumber
        self.pin = Pin(pinNumber, Pin.OUT, Pin.PULL_DOWN)
        self.on = False
        self.disabled = False
        self.name = name
        self.controllerOnList = []
    
    # Args:
    #   controlName: str - name of the calling controller
    def on(self, controlName):
        if self.disabled:
            return
        
        self.controllerOnList[controlName] = True
        if not self.on:
            self.on = True
            self.pin.toggle()
    
    # Args:
    #   controlName: str - name of the calling controller
    def off(self, controlName):
        if self.disabled:
            return
        
        self.controllerOnList[controlName] = False
        if self.on and any(self.controllerOnList):
            self.on = False
            self.pin.toggle()
            
    # Args:
    #   message: str - message to log, appended to the logPrefix with a timestamp
    def log(self, message: str):
        print(self.logPrefix, time.time(), ' - ', message)
    
    def disable(self):
        if self.disabled == False:
            self.disabled = True
            if self.on():
                self.pin.toggle()
    
    def enable(self):
        if self.disabled:
            self.disabled = False
            if self.on():
                self.pin.toggle()

class SolidStateRelay(ControlTarget):
    def __init__(self, pinNumber, name):
        super().__init__(pinNumber, name)
        self.pin.off()
    
    def __str__(self):
        return 'Solid State Relay, pin ' + str(self.pinNumber)

class Solenoid(ControlTarget):
    def __init__(self, pinNumber, name):
        super().__init__(pinNumber, name)
        self.pin.on()
    
    def __str__(self):
        return 'Solenoid, pin ' + str(self.pinNumber)
















