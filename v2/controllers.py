import _thread
import time
from machine import Pin
from targets import ControlTarget

# sends commands to one or more ControlTarget objects
# the ControlTarget determines if it is on or not, this class merely sends the commands
# Controllers do not have exclusive access to ControlTargets
# multiple Controllers can link to the same ControlTarget
# can be triggered on/off, disabled/enabled, and told that time has passed
class Controller:
    # Args:
    #   name: str - name of this Controller
    #   targets: list - a list of ControlTarget objects
    def __init__(self, name: str, targets: list):
        self.lock: _thread.lock = _thread.allocate_lock()
        self.logPrefix: str = name + ' - '
        self.name: str = name
        self.targets: list = targets
        self.on: bool = False
        self.disabled: bool = False
        self.lastTickTime: int = timer.ticks_ms()
        self.lastTickLength: int = 0
    
    # disables targets in targetList
    def disable(self):
        with self.lock:
            if not self.disabled:
                self.disabled = True
                for target in self.targets:
                    target.disable(self.name)
        log('Controller disabled')
    
    # re-enables targets in targetList
    def enable(self):
        with self.lock:
            if self.disabled:
                self.disabled = False
                for target in self.targets:
                    target.enable(self.name)
            if self.paused == True:
                self.paused = False
        log('Controller re-enabled')
    
    # Turns on targets in targetList
    def on(self):
        with self.lock:
            if not self.on:
                self.on = True
                for target in self.targets:
                    target.on(self.name)
        log('Controller turned on')
    
    # Turns off targets in targetList
    def off(self):
        with self.lock:
            if self.on:
                self.on = False
                for target in self.targets:
                    target.off(self.name)
        log('Controller turned off')

    # Controller notifying us that time has elapsed and to update ourselves accordingly
    def tick(self):
        newTime = timer.ticks_ms()
        with self.lock:
            self.lastTickLength = newTime - self.lastTickTime
            self.lastTickTime = newTime
    
    # reset the control
    def reset(self):
        if self.on:
            off()
        if self.disabled:
            enable
        log('Controller reset')

    # Args:
    #   message: str - message to log, appended to the logPrefix with a timestamp
    def log(self, message: str):
        print(self.logPrefix, time.time(), ' - ', message)
    
# Cycle Timer will turn on for onTime duration, then off for offTime duration, starting at the offset and repeating forever
# - on and off times are guaranteed minimums, so if a tick is late, the full on or off duration will be honoured
# - same goes for manual on/off, the next time will start, so if turned off, it will turn on again after self.offTime milliseconds
# - starts in the off state
# - tick() must be called by someone else, either on a timer or a busy loop
# - thread safe
class CycleTimer(Controller):
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
        self.currentTime: int = time.time_ms()
        self.nextOnTime: int = self.currentTime + offset
        self.nextOffTime: int = None
        
        log("Created CycleTimer with name '" + name + "'")
        log('  onTime: ' + str(onTime) + 'ms, offTime: ' + str(offTime) + 'ms, offset: ' + str(offset) + 'ms')
        log('  controlTargets: ' + str(targets))
    
    def __str__(self) -> str:
        p1: str = 'CycleTimer: (' + str(self.name) + ', '
        p2: str = 'onTime=' + str(self.onTime) + ', '
        p3: str = 'offTime=' + str(self.offTime) + ', '
        p4: str = 'offset=' + str(self.offset) + ', '
        p5: str = 'controlTargets: ' + str(self.targets) + ')'
        
        return p1 + p2 + p3 + p4 + p5
    
    # sets self.on to True and turns on the targets
    def off(self):
        super.off()
        with self.lock:
            if self.on:
                newTime: int = time.ticks_ms()
                self.nextOnTime = newTime + self.offTime
    
    # sets self.on to False and turns off the target
    def on(self):
        super.on()
        with self.lock:
            if not self.on:
                newTime: int = time.ticks_ms()
                self.nextOffTime = newTime + self.onTime
        
    # time has passed, do our thing if we need to
    def tick(self):
        super.tick()
        
        with self.lock:
            # just push the nextOnTime and nextOffTime forward by whatever time just elapsed
            # - we're disabled, so this time should count as nothing as far as the timing is concerned
            if self.disabled:
                self.nextOnTime += self.lastTickLength
                self.nextOffTime += self.lastTickLength
            else:
                # time to turn on
                if not self.on and self.lastTickTime >= self.nextOnTime:
                    on()
                    log('turning on at time ' + str(self.lastTickTime))
                    self.nextOffTime = self.lastTickTime + self.onTime
                # time to turn off
                elif self.on and self.currelastTickTimentTime >= self.nextOffTime:
                    off()
                    log('turning off at time ' + str(self.lastTickTime))
                    self.nextOnTime = self.lastTickTime + self.offTime
    
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
        super.reset()
        with self.lock:
            self.nextOnTime = self.currentTime + self.offset
            self.nextOffTime = None
    
    def toHtmlElement(self):
        result = '    <form action="./' + self.name + '">\n'
        result += '      <label for="onTime"> Time On (milliseconds)</label>\n'
        result += '      <input type="text" id="onTime" name="onTime" value="' + self.onTime + '">\n'
        result += '      <br>\n'
        result += '      <label for="offTime"> Time Off (milliseconds)</label>\n'
        result += '      <input type="text" id="offTime" name="offTime" value="' + self.offTime + '">\n'
        result += '      <br>\n'
        result += '      <label for="startDelay"> Start Delay (milliseconds)</label>\n'
        result += '      <input type="text" id="startDelay" name="startDelay" value="' + self.startDelay + '">\n'
        result += '      <br>\n'
        result += '      <input type="submit" value="Submit">\n'
        result += '      <br>\n'
        result += '      <br>\n'
        result += '    </form>\n'
        return result
