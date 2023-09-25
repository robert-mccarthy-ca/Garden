import _thread
from targets import ControlTarget

class Control:
    def __init__(self, name: str, target: ControlTarget):
        self.lock = _thread.allocate_lock()
        self.logPrefix: str = name + ' - '
        self.name:str = name
        self.target: ControlTarget = target
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
    

















