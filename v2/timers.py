from machine import Pin
import time
import _thread

# Cycle Timer will turn on for onTime duration, then off for offTime duration, starting at the offset and repeating forever
# - the time taken for each cycle is the sum of processing time from each tick plus the on and off times
# - starts in the off state
# - externally timed, tick() gets called with the time since the last tick determined automatically
# - externally driven, tick() needs to be called by someone else, whether in a delay loop or busy loop, it needs to be called from outside
# - single threaded
# - thread safe
class CycleTimer:
    # Args:
    #    name: str - display name for the timer
    #    onTime: int - on time in milliseconds
    #    offTime: int - off time in milliseconds
    #    offset: int - offset in milliseconds
    #    target: a TimerTarget object
    #    pinNumber: int - the Pico W's pin corresponding to your GPIO pin
    def __init__(self, name, onTime, offTime, offset, target, pinNumber):
        self.logPrefix = 'CycleTimer: ' + name + ' - '
        self.onTime = onTime
        self.offTime = offTime
        self.offset = offset
        self.target = target
        
        self.currentTime = time.time_ms()
        self.nextOnTime = self.currentTime + offset
        self.nextOffTime = None
        self.on = False
        self.paused = False
        self.useLED = False
        self.lock = _thread.allocate_lock()
        
        self.led = Pin('LED', Pin.OUT)
        self.pin = Pin(pinNumber, Pin.OUT, Pin.PULL_DOWN)
        
        print("Created CycleTimer with name '", name, "'")
        print('  onTime: ', onTime, 'ms, offTime: ', offTime, 'ms, offset: ', offset, 'ms')
        print('  pinHigh: ', pinHigh, ', tickSize: ', tickSize, 'ms, on Pin ', pin)
    
    # Args:
    #   message: str - message to log, appended to the logPrefix with a timestamp
    def log(self, message):
        print(self.logPrefix, time.time(), ' - ', message)
    
    # sets self.on to True and turns on the target
    def turnOff():
        self.on = False
        self.target.off()
    
    # sets self.on to False and turns off the target
    def turnOn():
        self.on = True
        self.target.on()
        
    # Args:
    #   tickSize: int - how long since the tick() method was last called
    # Returns:
    #   result: bool - False if paused, True otherwise
    def tick(self):
        newTime = time.time_ms()
        
        if self.paused:
            self.lock.acquire()
            
            elapsedTime = newTime - self.currentTime
            self.nextOnTime += elapsedTime
            self.nextOffTime += elapsedTime
            self.currentTime = newTime
            
            self.lock.release()
            return false
        
        self.lock.acquire()
        
        self.currentTime = newTime
        if not self.on and self.currentTime >= self.nextOnTime:
            self.on = True
            self.target.on()
            log('turning on at time ' + str(self.currentTime))
            self.nextOffTime = self.currentTime + self.onTime
            if self.useLED == True:
                self.led.on()
                log('LED on')
        elif self.on and self.currentTime >= self.nextOffTime:
            turnOff()
            log('turning off at time ' + str(self.currentTime))
            self.nextOnTime = self.currentTime + self.offTime
            if self.useLED == True:
                self.led.off()
                log('LED off')
        
        self.lock.release()
        
        return True
    
    # Args:
    #   newTime: int - set onTime to newTime
    def setOnTime(self, newTime):
        self.lock.acquire()
        
        self.onTime = newTime
        log('onTime set to ' + str(newTime/1000) + ' seconds')
        
        self.lock.release()
    
    # Args:
    #   newTime: int - set offTime to newTime
    def setOffTime(self, newTime):
        self.lock.acquire()
        
        self.offTime = newTime
        log('offTime set to ' + str(newTime/1000) + ' seconds')
        
        self.lock.release()
    
    # Args:
    #   newTime: int - set offset to newTime
    def setOffset(self, newTime):
        self.lock.acquire()
        
        self.offset = newTime
        log('offset set to ' + str(newTime/1000) + ' seconds')
        
        self.lock.release()
    
    # pauses timer
    def pause(self):
        self.lock.acquire()
        
        if self.paused == False:
            self.paused = True
            log('pausing')
            
        self.lock.release()
    
    # un-pauses timer
    def resume(self):
        self.lock.acquire()
        
        if self.paused == True:
            self.paused = False
            log('resuming')
            
        self.lock.release()
    
    # resets to starting settings, turning target off and starting from offset just like a restart
    def reset(self):
        self.lock.acquire()
        
        turnOff()
        self.currentTime = time.time_ms()
        self.nextOnTime = self.currentTime + self.offset
        self.nextOffTime = None
        
        self.lock.release()
    
    # Assigns fresh values and resets
    # Args:
    #   onTime: int - new onTime
    #   offTime: int - new offTime
    #   offset: int - new offset
    def reinitialize(self, onTime, offTime, offset):
        self.lock.acquire()
        
        self.onTime = onTime
        self.offTime = offTime
        self.offset = offset
        
        self.lock.release()
        
        self.reset()
    
    # Args:
    #   value: bool - new value for self.useLED
    def setUseLED(self, value):
        self.lock.acquire()
        
        self.useLED = value
        log('UseLED set to ' + str(self.useLED))
        
        self.lock.release()
    
    # Returns:
    #   self.useLED: bool
    def isUsingLED(self):
        return self.useLED
