from machine import Pin
import utime
import _thread

# used to set a pin to on/off on a cycle, for example, 2 seconds on, 7 seconds off forever
# onTime = how many seconds the timer is on for
# offTime = how many seconds the timer is off for
# startOn = whether or not the pin should initially be set to the high state
# startDelay = offset so this can be set to overlap with another timer
# thread safe
class CycleTimer:
    def __init__(self, name, onTime, offTime, startDelay, startOn, pinNumber):
        self.name = name
        self.onTime = onTime
        self.offTime = offTime
        self.startDelay = startDelay
        self.index = 0
        self.totalDuration = onTime + offTime
        self.onIndex = startDelay
        self.offIndex = (startDelay + onTime) % self.totalDuration
        self.on = False
        newPin = Pin(pinNumber, Pin.OUT, Pin.PULL_DOWN)
        self.lock = _thread.allocate_lock()
        
        if startOn == True:
            newPin.on()
        else:
            newPin.off()
        self.pin = newPin
            
        print("CycleTimer - " + str(name) + " created on GPIO pin " + str(pinNumber))
        print("  " + str(onTime) + " seconds on, " + str(offTime) + " seconds off, with start delay of " + str(startDelay) + " seconds")
        
    # passage of 0.1 seconds
    # returns whether the timer is currently in the on state
    def tick(self):
        self.lock.acquire()
        if self.index == self.onIndex and self.on == False and self.onTime > 0:
            print(self.timerName + " turning on at index " + str(self.index))
            self.pin.toggle()
            self.on = True
        elif self.index == self.offIndex and self.on:
            print(self.timerName + " turning off at index " + str(self.index))
            self.pin.toggle()
            self.on = False
        
        self.index += 0.1
        # faster than using modulus operations every time
        if self.index == self.totalDuration:
            self.index = 0
        self.lock.release()
            
        return self.on
        
    # resets with new values for onTime, offTime and startDelay
    def reinitialize(self, onTime, offTime, startDelay):
        self.lock.acquire()
        if self.on:
            self.pin.toggle()
            self.on = False
        self.index = 0
        self.onTime = onTime
        self.offTime = offTime
        self.totalDuration = onTime + offTime
        self.startDelay = startDelay
        self.onIndex = startDelay
        self.offIndex = (startDelay + onTime) % self.totalDuration
        self.lock.release()
