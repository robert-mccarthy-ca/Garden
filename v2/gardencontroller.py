import json
import timers
import utime
import _thread
import targets

def getConfigDictionary() -> dict:
    config = None
    print('loading configuration dictionary')
    with open('config.json', 'r') as configFile:
        config = json.load(configFile, 'r')
    return config

def loadControls(config: dict) -> dict:
    controls = None
    print('configuring controls')
    for name in config:
        try:
            controlConfig = config[name]
            controlType = controlConfig['controlType']
            if 'CycleTimer' == controlType:
                onTime = controlConfig['onTime']
                offTime = controlConfig['offTime']
                offset = controlConfig['offset']
                target = controlConfig['target']
                targetType = target['targetType']
                targetPin = target['targetPin']
                
                controlTarget = getTarget(targetType, targetPin)
                control = timers.CycleTimer(name, onTime, offTime, offSet, controlTarget)
                controls[name]=[control]
            else:
                raise Exception('Invalid configuration data, discarding object: ' + str(controlType))
        except Exception as ex:
            print('Error occurred while loading ', name)
            print(ex)
    
    return controls

def getControlTarget(controlType:str, pinNumber: int):
    controlTarget: targets.ControlTarget = None
    if controlType == 'SolidStateRelay':
        controlTarget = targets.SolidStateRelay(pinNumber)
    elif controlType == 'Solenoid':
        controlTarget = targets.Solenoid(pinNumber)
    else:
        raise Exception('Unknown controlType: ' + str(controlType))
    return target

def getWifiConfig():
    config: dict = None
    print('loading configuration for wifi ...')
    with open('wifi.json', 'r') as configFile:
        config: dict = json.load(configFile, 'r')

    return config['ssid'], config['password']

def buildHtml():
    return None

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

def runTimers():
    global controlLock
    global config
    while True:
        with controlLock:
            for control in controls:
                with control.lock:
                    control.tick()

def getParameters(actionString):
    print('debug start')
    print(f'actionString: {actionString}')
    parameters = actionString.split('?')
    print(f'parameters: {parameters}')
    if len(parameters) < 2 or len(parameters[1]) == 0:
        return parameters[0], None
    splitParameters = parameters[1].split('&')
    print(f'splitParameters: {splitParameters}')
    keys = []
    values = []
    
    for index, parameter in enumerate(splitParameters):
        print(f'index: {index}, parameter: {parameter}')
        pair = parameter.split('=')
        if pair == None or len(pair) < 2:
            pass
        keys.append(pair[0])
        values.append(pair[1])
        
    result = dict(zip(keys, values))
    print(f'result: {result}')
    print('debug end')
    return parameters[0], result

def processRequest(request, client):
    requestParts = request.split()
    httpMethod = None
    action = None
    try:
        httpMethod = requestParts[0]
        action = requestParts[1]
        print('http method = ' + str(httpMethod) + ', action = ' + str(action))
    except IndexError:
        pass
    
    parameters = getParameters(action)
    target = parameters[0]
    print('target: ', target)
    dictionary = parameters[1]
    print('actionDictionary:', dictionary)
    
    if target == '/reset':
        for control in controls:
            control.reset()
    elif target[1:] in controls:
        with control.lock:
            control = controls[target[1:]]
            control.update(dictionary)
    
    if httpMethod == 'GET':
        if target == '/favicon.ico':
            response = 'HTTP/1.1 404 Not Found\nConnection: close\n\n'
        else:
            response = buildHtml()
        client.send(response)
        print('returning html response to ', clientAddress, ':\n', response)

def runWebServer():
    serverAddress = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    serverSocket = socket.socket()
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(serverAddress)
    serverSocket.listen(1)
    print('listening on', serverAddress)
    
    while True:
    try:
        client, clientAddress = serverSocket.accept()
        print('client connected from', clientAddress)
        request = client.recv(1024)
        requestString = request.decode('ASCII')
        print('Content = %s' % requestString)
        processRequest(requestString, client)
        client.close()
        
    except OSError as e:
        client.close()
        print('connection closed')
    except KeyboardInterrupt:
        machine.reset()

# for modifying controls across threads
controlLock = _thread.allocate_lock()

# load our configuration from file
config = getConfigDictionary()
ssid, password = getWifiConfig()
controls = loadControls(config)       # TODO

connectWifi(config.get('connectionType', 'station'), ssid, password)
_thread.start_new_thread(runTimers, ())
runWebServer()                                                       # TODO

        
     
















