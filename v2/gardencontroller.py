import BaseHTTPServer
import json
import requests
import controllers
import time
import _thread
import targets
from controllers import CycleTimer

class GardenRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        # basic page no arguments
        page: str = buildHtml()
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)
        # pages with arguments
    
def buildHtml() -> str:
    result: str = '<!DOCTYPE html>\n'
    result += '<html lang="en">\n'
    result += '  <head>\n'
    result += '    <title>Hortus Deorum</title>\n'
    result += '    <meta name="viewport" content="width=device-width, initial-scale=1" /><meta charset="UTF-8" />\n'
    result += '    <style>\n'
    result += '      {\n'
    result += '        font-size: 50px;\n'
    result += '        box-sizing: border-box;\n'
    result += '      }\n'
    result += '    </style>\n'
    result += '  </head>\n'
    result += '  <body>\n'
    result += '    <h1>Hortus Deorum</h1>\n'
    result += '    <hr>\n'

    for control in controls:
        result += control.toHtmlElement()
    
    result += '    <hr>\n'
    result += '  </body>\n'
    result += '</html>\n'
    
    return result

def getConfigDictionary() -> dict:
    config = None
    print('loading configuration dictionary')
    with open('config.json', 'r') as configFile:
        config = json.load(configFile, 'r')
    return config

def loadControls() -> dict:
    config = getConfigDictionary()
    controls: dict = {}
    print('configuring controls')
    for name in config:
        try:
            controlConfig: dict = config[name]
            controlType: str = str(controlConfig['controlType'])
            controlTargets: list = getControlTargets(controlConfig['controlTargets'])
                
            if 'CycleTimer' == controlType:
                onTime: int = controlConfig['onTime']
                offTime: int = controlConfig['offTime']
                offset: int = controlConfig['offset']
                
                control: CycleTimer = CycleTimer(name, onTime, offTime, offSet, controlTargets)
                controls[name] = control
            else:
                raise Exception('Invalid configuration data, discarding object: ' + str(controlType))
            
        except Exception as ex:
            print('Error occurred while loading ', name)
            print(ex)
    
    return controls

def getControlTargets(targetDictionary: dict) -> list:
    controlTargets: list = []
    for controlTarget in targetDictionary:
        name: str = str(controlTarget['name'])
        pinNumber: int = int(controlTarget['pinNumber'])
        controlType:str = str(controlTarget['type'])
        
        if controlType == 'SolidStateRelay':
            newTarget: targets.SolidStateRelay = targets.SolidStateRelay(name, pinNumber)
            controlTargets.append(newTarget)
        elif controlType == 'Solenoid':
            newTarget: targets.Solenoid = targets.Solenoid(name, pinNumber)
            controlTargets.append(newTarget)
        else:
            log('Unknown control target type: ' + controlType)
    
    return controlTargets

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


        
     
















