from machine import Pin
import utime
import _thread

# used to set a pin to on/off on a cycle, for example, 2 seconds on, 7 seconds off forever
# name = name used in log statements
# onTimeMs = how many milleseconds the timer is on for
# offTimeMs = how many milliseconds the timer is off for
# startOnMs = whether or not the pin should initially be set to the high state
# startDelayMs = offset so this can be set to overlap with another timer in milliseconds
# tickSizeMs = how much timer passes between ticks in milliseconds
# pinNumber = the Pico W pin number to use for transmitting our signal
# thread safe
class CycleTimer:
    def __init__(self, name, onTimeMs, offTimeMs, startDelayMs, startOn, tickSizeMs, pinNumber):
        self.name = name
        self.onTime = onTime 
        self.offTime = offTime
        self.startDelay = startDelay
        self.tickSize = tickSizeMs
        self.index = 0
        self.onIndex = startDelay
        self.offIndex = startDelay + onTime
        self.on = False
        self.paused = False
        self.led = Pin("LED",machine.Pin.OUT)
        self.useLED = False
        newPin = Pin(pinNumber, Pin.OUT, Pin.PULL_DOWN)
        self.lock = _thread.allocate_lock()
        
        if startOn == True:
            newPin.on()
        else:
            newPin.off()
        self.pin = newPin
            
        print("CycleTimer - " + str(name) + " created on GPIO pin " + str(pinNumber))
        print("  " + str(onTime) + " seconds on, " + str(offTime) + " seconds off, with start delay of " + str(startDelay) + " seconds")
        
    # passage of 1 tick
    # returns whether the timer is currently in the on state
    def tick(self):
        self.lock.acquire()
        
        # do nothing if paused
        if self.paused:
            pass
        # delay before next shutoff set at the start of the on period, changes to that value take effect then
        elif self.on == False and self.index >= self.onIndex:
            self.pin.toggle()
            self.on = True
            self.offIndex = self.index + self.offTime
            self.index += tickSize
            print(self.name + " turning on at index " + str(self.index))
            if self.useLED == True:
                self.led.on()
        elif self.on == True and self.index >= self.offIndex:
            self.pin.toggle()
            self.on = False
            self.onIndex = self.index + self.onTime
            self.index += tickSize
            print(self.name + " turning off at index " + str(self.index))
            self.led.off()
        
        self.lock.release()
            
        return self.on
    
    def setOnTimeMs(self, newTime):
        self.lock.acquire()
        self.onTime = newTime
        self.lock.release()
        
    def setOffTimeMs(self, newTime):
        self.lock.acquire()
        self.offTime = newTime
        self.lock.release()
        
    def setStartDelay(self, newTime):
        self.lock.acquire()
        self.startDelay = newTime
        self.lock.release()
        
    def setTickSize(self, newTime):
        self.lock.acquire()
        self.tickSize = newTime
        self.lock.release()
        
    def pause(self):
        self.lock.acquire()
        self.paused = True
        self.lock.release()
        
    def resume(self):
        self.lock.acquire()
        self.paused = False
        self.lock.release()
        
    def reset(self):
        self.lock.acquire()
        if self.on:
            self.pin.toggle()
            self.on = False
        self.index = 0
        self.onIndex = self.startDelay
        self.offIndex = self.onIndex + self.offTime
        self.lock.release()
        
    # resets with new values for onTime, offTime and startDelay
    def reinitialize(self, onTime, offTime, startDelay):
        self.lock.acquire()
        self.onTime = onTime
        self.offTime = offTime
        self.startDelay = startDelay
        self.lock.release()
        
        self.reset()
        
    def setUseLED(self, value):
        self.lock.acquire()
        self.useLED = value
        self.lock.release()
        
    def isUsingLED(self):
        return self.useLED
