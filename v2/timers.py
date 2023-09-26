from machine import Pin
import time
import _thread
from targets import ControlTarget

# Cycle Timer will turn on for onTime duration, then off for offTime duration, starting at the offset and repeating forever
# - on and off times are guaranteed minimums, so if a tick is late, the full on or off duration will be honoured
# - starts in the off state
# - tick() must be called by someone else, either on a timer or a busy loop
# - thread safe
class CycleTimer(Control):
    # Args:
    #    name: str - display name for the timer
    #    onTime: int - on time in milliseconds
    #    offTime: int - off time in milliseconds
    #    offset: int - offset in milliseconds
    #    target: a ControlTarget object
    def __init__(self, name: str, onTime: int, offTime: int, offset: int, target: ControlTarget):
        super().__init__(name, target)
        
        self.onTime: int = onTime
        self.offTime: int = offTime
        self.offset: int = offset
        self.target: ControlTarget = target
        
        self.currentTime: int = time.time_ms()
        self.nextOnTime: int = self.currentTime + offset
        self.nextOffTime: int = None
        
        print("Created CycleTimer with name '", name, "'")
        print('  onTime: ', onTime, 'ms, offTime: ', offTime, 'ms, offset: ', offset, 'ms')
        print('  controlTarget: ', target)
    
    def __str__(self) -> str:
        p1: str = 'CycleTimer: (' + str(self.name) + ', '
        p2: str = 'onTime=' + str(self.onTime) + ', '
        p3: str = 'offTime=' + str(self.offTime) + ', '
        p4: str = 'offset=' + str(self.offset) + ', '
        p5: str = 'controlTarget: ' + str(self.target) + ')'
        
        return p1 + p2 + p3 + p4 + p5
    
    # sets self.on to True and turns on the target
    def turnOff(self):
        with self.lock:
            if self.on:
                self.on = False
                self.target.off(self.name)
    
    # sets self.on to False and turns off the target
    def turnOn(self):
        with self.lock:
            if not self.on:
                self.on = True
                self.target.on(self.name)
        
    # Returns:
    #   result: bool - False if paused, True otherwise
    def tick(self):
        newTime = time.ticks_ms()
        
        with self.lock:
            if self.paused:
                elapsedTime = newTime - self.currentTime
                self.nextOnTime += elapsedTime
                self.nextOffTime += elapsedTime
                self.currentTime = newTime
                return False
            else:
                self.currentTime = newTime
                if not self.on and self.currentTime >= self.nextOnTime:
                    turnOn()
                    log('turning on at time ' + str(self.currentTime))
                    self.nextOffTime = self.currentTime + self.onTime
                elif self.on and self.currentTime >= self.nextOffTime:
                    turnOff()
                    log('turning off at time ' + str(self.currentTime))
                    self.nextOnTime = self.currentTime + self.offTime
                return True
    
    # Args:
    #   newTime: int - set onTime to newTime
    def setOnTime(self, newTime: int):
        with self.lock:
            self.onTime = newTime
        log('onTime set to ' + str(newTime/1000) + ' seconds')
    
    # Args:
    #   newTime: int - set offTime to newTime
    def setOffTime(self, newTime: int):
        with self.lock:
            self.offTime = newTime
        log('offTime set to ' + str(newTime/1000) + ' seconds')
    
    # Args:
    #   newTime: int - set offset to newTime
    def setOffset(self, newTime: int):
        with self.lock:
            self.offset = newTime
        log('offset set to ' + str(newTime/1000) + ' seconds')
    
    # resets to starting settings, turning target off and starting from offset just like a restart
    def reset(self):
        with self.lock:
            turnOff()
            self.currentTime = time.ticks_ms()
            self.nextOnTime = self.currentTime + self.offset
            self.nextOffTime = None
        log('resetting')
    
    # Assigns fresh values and resets
    # Args:
    #   onTime: int - new onTime
    #   offTime: int - new offTime
    #   offset: int - new offset
    def reinitialize(self, onTime: int, offTime: int, offset: int):
        with self.lock:
            self.onTime = onTime
            self.offTime = offTime
            self.offset = offset
        log('reinitializing with new values:')
        log('  onTime = ', + str(onTime))
        log('  offTime = ', + str(offTime))
        log('  offset = ', + str(onTime))
        self.reset()
