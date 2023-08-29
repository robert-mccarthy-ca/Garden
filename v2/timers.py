from machine import Pin
import utime
import _thread

# Cycle Timer will turn on for onTime duration, then off for offTime duration, starting at the offset and repeating forever
# can be configured with an optional test circuit that can turn it on when set to high
class CycleTimer:
    # Args:
    #    name: str - display name for the timer
    #    onTime: int - on time in milliseconds
    #    offTime: int - off time in milliseconds
    #    offset: int - offset in milliseconds
    #    target: a TimerTarget object
    #    tickSize: int - tick size in milliseconds
    #    pinNumber: int - the Pico W's pin corresponding to your GPIO pin
    #    testPinNumber: int - an optional test pin which when set to high will turn on
    def __init__(self, name, onTime, offTime, offset, target, tickSize, pinNumber, testPinNumber=None):
        self.logPrefix = 'CycleTimer: ' + name
        self.onTime = onTime
        self.offTime = offTime
        self.offset = offset
        self.tickSize = tickSize
        self.target = target
        
        self.currentTime = 0
        self.on = False
        self.paused = False
        self.useLED = False
        self.lock = _thread.allocate_lock()
        
        self.led = Pin('LED', Pin.OUT)
        self.pin = Pin(pinNumber, Pin.OUT, Pin.PULL_DOWN)
        self.testPin = None
        if testPinNumber not None:
            testPin = Pin(testPinNumber, Pin.IN)
        
        if pinHigh == True:
            self.pin.on()
        else:
            self.pin.off()
        
        print("Created CycleTimer with name '", name, "'")
        print('onTime: ', onTime, 'ms, offTime: ', offTime, 'ms, offset: ', offset, 'ms')
        print('pinHigh: ', pinHigh, ', tickSize: ', tickSize, 'ms, on Pin ', pin)
    
    def turnOff(self):
        self.on = False
        if testPin is None or testPin.value() == 0:
            self.target.off()
        
    def turnOn(self):
        self.on = True
        self.target.on()
    
    def tick(self):
        if self.paused:
            return false
        
        
            





