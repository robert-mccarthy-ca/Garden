from machine import Pin
import utime
import _thread

# used to set a pin to on/off on a cycle, for example, 2 seconds on, 7 seconds off forever
# does not use interrupts, stays on the thread that calls it
# thread safe
#
# name = name used in log statements
# onTimeMs = how many milleseconds the timer is on for
# offTimeMs = how many milliseconds the timer is off for
# startPinHigh = whether or not the pin should initially be set to the high state
# startDelayMs = offset so this can be set to overlap with another timer in milliseconds
# tickSizeMs = how much timer passes between ticks in milliseconds
# pinNumber = the Pico W pin number to use for transmitting our signal

class CycleTimer:
    def __init__(self, name, onTimeMs, offTimeMs, startDelayMs, startPinHigh, tickSizeMs, pinNumber):
        self.prefix = name + ' - '
        self.onDuration = onTimeMs
        self.offDuration = offTimeMs 
        self.nextOnTime = startDelayMs 
        self.nextOffTime = startDelayMs + onTimeMs
        self.startDelay = startDelayMs
        self.tickSize = tickSizeMs
        self.currentTime = 0
        self.on = False
        self.paused = False
        self.led = Pin("LED", Pin.OUT)
        self.useLED = False
        self.pin = Pin(pinNumber, Pin.OUT, Pin.PULL_DOWN)
        self.lock = _thread.allocate_lock()
        
        if startPinHigh == True:
            self.pin.on()
        else:
            self.pin.off()
            
        print("CycleTimer - " + str(name) + " created on Pico W pin # " + str(pinNumber))
        print("  " + str(onTimeMs/1000) + " seconds on, " + str(offTimeMs/1000) + " seconds off, with start delay of " + str(startDelayMs/1000) +
              " seconds at a resolution of " + str(tickSizeMs) + " milliseconds")
        
    # passage of 1 tick
    # returns whether the timer is currently in the on state
    def tick(self):
        # do nothing if paused
        if self.paused:
            return
        
        self.lock.acquire()
        #print('on = ' + str(self.on) + ', currentTime = ' + str(self.currentTime) + ', nextOnTime = ' + str(self.nextOnTime) + ', nextOffTime = ' + str(self.nextOffTime))
        # delay before next shutoff set at the start of the on period, changes to that value take effect then
        if self.on == False and self.currentTime >= self.nextOnTime:
            self.pin.toggle()
            self.on = True
            self.nextOffTime = self.currentTime + self.onDuration
            print(self.prefix + "turning on at time " + str(self.currentTime))
            if self.useLED == True:
                self.led.on()
                print(self.prefix + 'LED on')
        elif self.on == True and self.currentTime >= self.nextOffTime:
            self.pin.toggle()
            self.on = False
            self.nextOnTime = self.currentTime + self.offDuration
            print(self.prefix + "turning off at time " + str(self.currentTime))
            if self.useLED == True:
                self.led.off()
                print(self.prefix + 'LED off')

        self.currentTime += self.tickSize
        #print(self.prefix + str(self.currentTime/1000) + ' seconds')
        
        self.lock.release()
            
        return self.on
    
    def setOnDuration(self, newTime):
        self.lock.acquire()
        self.onDuration = newTime
        print(self.prefix + 'onDuration set to ' + str(newTime/1000) + ' seconds')
        self.lock.release()
        
    def setOffDuration(self, newTime):
        self.lock.acquire()
        self.offDuration = newTime
        print(self.prefix + 'offDuration set to ' + str(newTime/1000) + ' seconds')
        self.lock.release()
        
    def setStartDelay(self, newTime):
        self.lock.acquire()
        self.startDelay = newTime
        print(self.prefix + 'startDelay set to ' + str(newTime/1000) + ' seconds')
        self.lock.release()
        
    def setTickSize(self, newTime):
        self.lock.acquire()
        self.tickSize = newTime
        print(self.prefix + 'tick size set to ' + str(newTime/1000) + ' seconds')
        self.lock.release()
        
    def pause(self):
        self.lock.acquire()
        if self.paused == False:
            self.paused = True
            print(self.prefix + 'pausing')
        self.lock.release()
        
    def resume(self):
        self.lock.acquire()
        if self.paused == True:
            self.paused = False
            print(self.prefix + 'resuming')
        self.lock.release()
        
    def reset(self):
        self.lock.acquire()
        if self.on:
            self.pin.toggle()
            self.on = False
        self.currentTime = 0
        self.nextOnTime = self.startDelay
        self.nextOffTime = self.startDelay + self.offDuration
        self.lock.release()
        
    # resets with new values for onDuration, offDuration and startDelay
    def reinitialize(self, onDuration, offDuration, startDelay):
        self.lock.acquire()
        self.onDuration = onDuration
        self.offDuration = offDuration
        self.startDelay = startDelay
        self.lock.release()
        
        self.reset()
        
    def setUseLED(self, value):
        self.lock.acquire()
        self.useLED = value
        print(self.prefix + 'UseLED set to ' + str(self.useLED))
        self.lock.release()
        
    def isUsingLED(self):
        return self.useLED
