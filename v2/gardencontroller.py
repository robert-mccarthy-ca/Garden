import BaseHTTPServer
import json
import requests
import controllers
import time
import _thread
import controlTargets
import urllib.parse
from controllers import CycleTimer

class GardenRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        # build our parameters dictionary from the path. 
        #   'name' contains the control name
        #   'type' contains the Controller type
        #   'operation' contains the operation type
        #   the rest are the parameters for the Controller
        parameters: dict = getParametersFromPath(self.path)
        if len(parameters) > 1:
            operation: str = parameters['operation']
            if operation == 'update':
                updateControl(parameters)
            elif operation == 'new':
                createControl(parameters)
            elif operation == 'delete':
                deleteControl(parameters)
            else:
                print('unknown operation:', operation)
                # send error response back
                self.send_response(400)
                return
          
        # build and return the webpage unless we errored out above
        # all valid GET requests to this server return this page
        htmlPage: str = buildHtml()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(htmlPage)))
        self.end_headers()
        self.wfile.write(page)
    
    # update an existing control
    def updateControl(self, params: dict):
        global controls
        global controlLock
        name: str = params['name']
        if name in controls:
            with controlLock:
                control = controls[name]
            type: str = params['type']
            if type == 'CycleTimer':
                onTime: int = int(params['onTime'])
                control.setOnTime(onTime)
                offTime: int = int(params['offTime'])
                control.setOffTime(offTime)
                startDelay: int = int(params['startDelay'])
                control.setStartDelay(startDelay)
                # allow updates to targetList
            else:
                print('unknown control type:', type)
        else:
            print('Invalid control name, not found:', name)
    
    def createControl(self, params: dict):
        type: str = params['type']
        if type == 'CycleTimer':
            onTime: int = int(params['onTime'])
            offTime: int = int(params['offTime'])
            startDelay: int = int(params['startDelay'])
            name: str = params['name']
            control: CycleTimer = CycleTimer(name, )
        return None
    
    def deleteControl(self, params: dict):
        return None
    
    def getParametersFromPath(self, path: str) -> dict:
        result: dict = {}
        pathParts: list = path.split('?')
        if len(pathParts) == 1:
            return result
        result['name'] = pathParts[0]
        for queryPair: str in pathParts[1].split('&'):
            queryParts = queryPair.split('=')
            result[queryParts[0]] = queryParts[1]
        return result
    
    def handle_error(self, msg: str):
        do_GET()
    
def buildHtml() -> str:
    result: str = ''
    
    return result

def loadControls() -> dict:
    mechanicalRelays: dict = {}
    mechanicalRelays[0] = MechanicalRelay('Air Solenoid Relay (All)', 0)
    
    mechanicalRelays[1] = MechanicalRelay('Sump Relay A', 1)
    mechanicalRelays[2] = MechanicalRelay('AAA Nutrient Pump Relay A', 2)
    mechanicalRelays[3] = MechanicalRelay('LPA Nutrient Pump Relay A', 3)
    
    mechanicalRelays[4] = MechanicalRelay('Sump Relay B', 4)
    mechanicalRelays[5] = MechanicalRelay('AAA Nutrient Pump Relay B', 5)
    mechanicalRelays[6] = MechanicalRelay('LPA Nutrient Pump Relay B', 6)
    
    mechanicalRelays[7] = MechanicalRelay('Sump Relay C', 7)
    mechanicalRelays[8] = MechanicalRelay('AAA Nutrient Pump Relay C', 8)
    mechanicalRelays[9] = MechanicalRelay('LPA Nutrient Pump Relay C', 9)
    
    inputSwitches: dict = {}
    inputSwitches[16] = Trigger('Sump A Float Switch', 16)
    inputSwitches[17] = Trigger('Sump B Float Switch', 17)
    inputSwitches[18] = Trigger('Sump C Float Switch', 18)
    
    controls: dict = {}
    controls['Air Solenoid (All)'] = CycleTimer(name='Air Solenoid (All)', onTime=1000, offTime=59000, offset=1000, targets=[mechanicalRelays[0]])
    
    controls['Sump Pump A'] = OnTrigger(name='Sump Pump A', duration=15000, trigger=inputSwitches[16], targets=[mechanicalRelays[1]])
    controls['AAA Nutrient Pump A'] = CycleTimer(name='AAA Nutrient Pump A', onTime=2000, offTime=58000, offset=0, targets=[mechanicalRelays[2]])
    controls['LPA Nutrient Pump A'] = CycleTimer(name='LPA Nutrient Pump A', onTime=30000, offTime=3570000, offset=0, targets=[mechanicalRelays[3]])
    
    controls['Sump Pump B'] = OnTrigger(name='Sump Pump B', duration=15000, trigger=inputSwitches[17], targets=[mechanicalRelays[4]])
    controls['AAA Nutrient Pump B'] = CycleTimer(name='AAA Nutrient Pump B', onTime=2000, offTime=58000, offset=0, targets=[mechanicalRelays[5]])
    controls['LPA Nutrient Pump B'] = CycleTimer(name='LPA Nutrient Pump B', onTime=30000, offTime=3570000, offset=0, targets=[mechanicalRelays[6]])
    
    controls['Sump Pump C'] = OnTrigger(name='Sump Pump C', duration=15000, trigger=inputSwitches[18], targets=[mechanicalRelays[7]])
    controls['AAA Nutrient Pump C'] = CycleTimer(name='AAA Nutrient Pump C', onTime=2000, offTime=58000, offset=0, targets=[mechanicalRelays[8]])
    controls['LPA Nutrient Pump C'] = CycleTimer(name='LPA Nutrient Pump C', onTime=30000, offTime=3570000, offset=0, targets=[mechanicalRelays[9]])
    
    return controls

def getWifiConfig() -> tuple:
    config: dict = None
    print('loading configuration for wifi ...')
    with open('wifi.json', 'r') as configFile:
        config: dict = json.load(configFile, 'r')

    return (config['ssid'], config['password'])

def connectWifi(connectionType:str, ssid: str, wifiPass: str):
    if connectionType == 'accessPoint':
        accessPoint = network.WLAN(network.AP_IF)
    elif connectionType == 'station':
        accessPoint = network.WLAN(network.AP_IF)
    else:
        raise Exception('Unknown connection type')
    
    print('Connecting to wifi as ', connectionType)
    accessPoint.config(essid=ssid, password=wifiPass)
    accessPoint.active(True)

    # wait until it's connected before proceeding
    while accessPoint.active() == False:
      pass

    print('Connection established')
    print('ifconfig = ' + str(accessPoint.ifconfig()))

# loops through our controls as fast as it can
def runControls():
    global controlLock
    global controls
    while True:
        with controlLock:
            for control in controls:
                with control.lock:
                    control.tick()

# for modifying controls across threads
controlLock = _thread.allocate_lock()

# load our configuration from file
ssid, password = getWifiConfig()
controls = loadControls()

connectWifi(config.get('connectionType', 'station'), ssid, password)
webServer = HTTPServer((hostName, serverPort), GardenRequestHandler)
print("Server started http://%s:%s" % ('localhost', 8080))  #Server starts

_thread.start_new_thread(runControls, ())
try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass
webServer.server_close()  #Executes when you hit a keyboard interrupt, closing the server
print("Server stopped.")


        
     
















