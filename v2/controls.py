import _thread
from targets import ControlTarget

class Control:
    def __init__(self, name: str, targets: list):
        self.lock = _thread.allocate_lock()
        self.logPrefix: str = name + ' - '
        self.name:str = name
        self.targets: list = targets
        self.on: bool = False
        self.paused: bool = False
    
    # pauses control
    def pause(self):
        with self.lock:
            if self.paused == False:
                self.paused = True
        print(self.name, ' pausing')
    
    # un-pauses control
    def resume(self):
        with self.lock:
            if self.paused == True:
                self.paused = False
        log(self.name, ' resuming')

    # Args:
    #   message: str - message to log, appended to the logPrefix with a timestamp
    def log(self, message: str):
        print(self.logPrefix, time.time(), ' - ', message)

    # Controller notifying us that time has elapsed and to update ourselves accordingly
    def tick(self):
        raise Exception('tick() method not implemented')
    
    # reset the control
    def reset(self):
        raise Exception('reset() method not implemented')
    
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
    #    targets: a list of ControlTarget objects
    def __init__(self, name: str, onTime: int, offTime: int, offset: int, targets: list):
        super().__init__(name, targets)
        
        self.onTime: int = onTime
        self.offTime: int = offTime
        self.offset: int = offset
        self.targets: list = targets
        
        self.currentTime: int = time.time_ms()
        self.nextOnTime: int = self.currentTime + offset
        self.nextOffTime: int = None
        
        print("Created CycleTimer with name '", name, "'")
        print('  onTime: ', onTime, 'ms, offTime: ', offTime, 'ms, offset: ', offset, 'ms')
        print('  controlTargets: ', targets)
    
    def __str__(self) -> str:
        p1: str = 'CycleTimer: (' + str(self.name) + ', '
        p2: str = 'onTime=' + str(self.onTime) + ', '
        p3: str = 'offTime=' + str(self.offTime) + ', '
        p4: str = 'offset=' + str(self.offset) + ', '
        p5: str = 'controlTargets: ' + str(self.targets) + ')'
        
        return p1 + p2 + p3 + p4 + p5
    
    # sets self.on to True and turns on the targets
    def turnOff(self):
        with self.lock:
            if self.on:
                self.on = False
                for target in self.targets:
                    target.off(self.name)
    
    # sets self.on to False and turns off the target
    def turnOn(self):
        with self.lock:
            if not self.on:
                self.on = True
                for target in self.targets:
                    target.on(self.name)
        
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
    
    # resets to starting settings, turning targets off and starting from offset just like a restart
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

















