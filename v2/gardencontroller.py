import timers
import utime
import _thread

def getConfigDictionary():
    return None

def loadControls():
    return None

def getWifiConfig():
    return None

def buildHtml():
    return None

def connectWifi(connectionType, ssid, wifiPass):
    if connectionType == 'accessPoint':
        accessPoint = network.WLAN(network.AP_IF)
    elif connectionType == 'station':
        accessPoint = network.WLAN(network.AP_IF)
    else:
        raise Exception('Unknown connection type')
    accessPoint.config(essid=ssid, password=wifiPass)
    accessPoint.active(True)

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

controlLock = _thread.allocate_lock()
config = getConfigDictionary()
ssid, password = getWifiConfig()
controls = loadControls(config)

connectWifi(config.get('connectionType', 'station'), ssid, password)
_thread.start_new_thread(runTimers, ())
runWebServer()

        
     















