import machine

# multiple controls can be linked to the same target
# not thread safe
class ControlTarget:
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.pin = Pin(pinNumber, Pin.OUT, Pin.PULL_DOWN)
        self.on = False
        self.controllerOnList = []
    
    # Args:
    #   controlName: str - name of the calling controller
    def on(self, controlName):
        self.controllerOnList[controlName] = True
        if not self.on:
            self.on = True
            self.pin.toggle()
    
    # Args:
    #   controlName: str - name of the calling controller
    def off(self, controlName):
        self.controllerOnList[controlName] = False
        if self.on and any(self.controllerOnList):
            self.on = False
            self.pin.toggle()
            
    # Args:
    #   message: str - message to log, appended to the logPrefix with a timestamp
    def log(self, message: str):
        print(self.logPrefix, time.time(), ' - ', message)

class SolidStateRelay(ControlTarget):
    def __init__(self, pinNumber):
        super().__init__(pinNumber)
        self.pin.off()
    
    def __str__(self):
        return 'Solid State Relay, pin ' + str(self.pinNumber)

class Solenoid(ControlTarget):
    def __init__(self, pinNumber):
        super().__init__(pinNumber)
        self.pin.on()
    
    def __str__(self):
        return 'Solenoid, pin ' + str(self.pinNumber)
















