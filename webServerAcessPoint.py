import network
import machine
import socket
import _thread
import utime
from cycleTimer import CycleTimer
from picozero import pico_led

# for demonstration purposes, use your own credentials
ssid = 'Demon Portal'
wifiPass = 'purplepolkadots'

# timer resolution in milliseconds
# Lower for better resolution, raise for lower power consumption
tickSizeMs = 100

# onboard LED for testing timers with
led = machine.Pin("LED",machine.Pin.OUT)

# water pump for the sprayer nozzle
aaPumpPin = 15
aaPumpOnTimeMs = 5000
aaPumpOffTimeMs = 35000
aaPumpStartDelayMs = 0
aaPumpIncrementMs = 100
aaPumpLock = _thread.allocate_lock()
aaPumpTimer = CycleTimer("Nozzle Pump Timer", aaPumpOnTimeMs, aaPumpOffTimeMs, aaPumpStartDelayMs, True, tickSizeMs, aaPumpPin)

# controls the solenoid for the air line leading to the nozzle
solenoidPin = 16
solenoidOnTimeMs = 1000
solenoidOffTimeMs = 39000
solenoidStartDelayMs = 2000
solenoidIncrementMs = 100
solenoidLock = _thread.allocate_lock()
solenoidTimer = CycleTimer("Solenoid Timer", solenoidOnTimeMs, solenoidOffTimeMs, solenoidStartDelayMs, False, tickSizeMs, solenoidPin)

# lpa pump for the reservoir
lpaPumpPin = 17
lpaPumpOnTimeMs = 60000
lpaPumpOffTimeMs = 1800000
lpaPumpStartDelayMs = 0
lpaPumpIncrementMs = 1000
lpaPumpLock = _thread.allocate_lock()
lpaPumpTimer = CycleTimer("LPA Pump Timer", lpaPumpOnTimeMs, lpaPumpOffTimeMs, lpaPumpStartDelayMs, True, tickSizeMs, lpaPumpPin)

testAaPumpOnTimeMs = 1000
testAaPumpOffTimeMs = 3000
testAaPumpStartDelayMs = 0

testSolenoidOnTimeMs = 1000
testSolenoidOffTimeMs = 3000
testSolenoidStartDelayMs = 0

testlpaPumpOnTimeMs = 10000
testlpaPumpOffTimeMs = 10000
testlpaPumpStartDelayMs = 0

testModeOn = False

def runTimers():
    index = 0
    while True:
        solenoidLock.acquire()
        solenoidTimer.tick()
        solenoidLock.release()
        
        lpaPumpLock.acquire()
        lpaPumpTimer.tick()
        lpaPumpLock.release()
        
        aaPumpLock.acquire()
        aaPumpTimer.tick()
        aaPumpLock.release()
        
        index += 1
        # sleep for however long our tick size is
        utime.sleep_ms(tickSizeMs)
        # periodic logging so we know this thread is still running
        if index % 50 == 0:
            print(str(index * tickSizeMs / 1000) + ' seconds')

def swapAndReset():
    global solenoidOnTimeMs
    global testSolenoidOnTimeMs
    global solenoidOffTimeMs
    global testSolenoidOffTimeMs
    global solenoidStartDelayMs
    global testSolenoidStartDelayMs
    global lpaPumpOnTimeMs
    global testlpaPumpOnTimeMs
    global lpaPumpOffTimeMs
    global testlpaPumpOffTimeMs
    global lpaPumpStartDelayMs
    global testlpaPumpStartDelayMs
    global aaPumpOnTimeMs
    global testAaPumpOnTimeMs
    global aaPumpOffTimeMs
    global testAaPumpOffTimeMs
    global aaPumpStartDelayMs
    global testAaPumpStartDelayMs
    
    solenoidLock.acquire()
    
    solenoidOnTimeMs, testSolenoidOnTimeMs = testSolenoidOnTimeMs, solenoidOnTimeMs
    solenoidOffTimeMs, testSolenoidOffTimeMs = testSolenoidOffTimeMs, solenoidOffTimeMs
    solenoidStartDelayMs, testSolenoidStartDelayMs = testSolenoidStartDelayMs, solenoidStartDelayMs
    solenoidTimer.reinitialize(solenoidOnTimeMs, solenoidOffTimeMs, solenoidStartDelayMs)
    
    solenoidLock.release()
    
    lpaPumpLock.acquire()
    
    lpaPumpOnTimeMs, testlpaPumpOnTimeMs = testlpaPumpOnTimeMs, lpaPumpOnTimeMs
    lpaPumpOffTimeMs, testlpaPumpOffTimeMs = testlpaPumpOffTimeMs, lpaPumpOffTimeMs
    lpaPumpStartDelayMs, testlpaPumpStartDelayMs = testlpaPumpStartDelayMs, lpaPumpStartDelayMs
    lpaPumpTimer.reinitialize(lpaPumpOnTimeMs, lpaPumpOffTimeMs, lpaPumpStartDelayMs)
    
    lpaPumpLock.release()
    
    aaPumpLock.acquire()
    
    aaPumpOnTimeMs, testAaPumpOnTimeMs = testAaPumpOnTimeMs, aaPumpOnTimeMs
    aaPumpOffTimeMs, testAaPumpOffTimeMs = testAaPumpOffTimeMs, aaPumpOffTimeMs
    aaPumpStartDelayMs, testAaPumpStartDelayMs = testAaPumpStartDelayMs, aaPumpStartDelayMs
    aaPumpTimer.reinitialize(aaPumpOnTimeMs, aaPumpOffTimeMs, aaPumpStartDelayMs)
    
    aaPumpLock.release()

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

def getTestModeElement():
    global testModeOn
    
    firstPart = '<p>Test Mode:</p><p><form action="./testModeOn"><input type="submit" value="Test Mode On" /></form>'
    secondPart = '<form action="./testModeOff"><input type="submit" value="Test Mode Off" /></form></p>'
    
    result = firstPart + str(testModeOn) + secondPart
    return result

def getHtmlBody():
    global solenoidTimer
    global lpaPumpTimer
    
    htmlBodyStart = '<body><h1>Hortus Deorum</h1><hr>\n'
    solenoidElement = solenoidTimer.toHtmlElement('airForm', 'airLedOn', 'airLedOff')
    lpaPumpElement = lpaPumpTimer.toHtmlElement('lpaPumpForm', 'lpaLedOn', 'lpaLedOff')
    aaPumpElement = aaPumpTimer.toHtmlElement('aaPumpForm', 'aaLedOn', 'aaLedOff')
    testModeElement = getTestModeElement()
    htmlBodyEnd = '</body>\n'
    gap = '<hr>\n'
    
    result = htmlBodyStart + solenoidElement + gap + lpaPumpElement + gap + aaPumpElement + gap + testModeElement + htmlBodyEnd
    return result

def buildHtml():
    doctype = '<!DOCTYPE html>\n'
    htmlOpen = '<html lang="en">\n'
    htmlMeta = '<meta name="viewport" content="width=device-width, initial-scale=1" /><meta charset="UTF-8" />'
    style = '<style>{font-size:50px;box-sizing: border-box;}</style>'
    htmlHead = '<head><title>Hortus Deorum</title>' + htmlMeta + style + '</head>\n'
    htmlBody = getHtmlBody()
    htmlEnd = '</html>\n'
    
    result = doctype + htmlOpen + htmlHead + htmlBody + htmlEnd
    return result

accessPoint = network.WLAN(network.AP_IF)
accessPoint.config(essid=ssid, password=wifiPass)
accessPoint.active(True)

while accessPoint.active() == False:
  pass

print('Access point established')
print('ifconfig = ' + str(accessPoint.ifconfig()))

serverAddress = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
serverSocket = socket.socket()
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(serverAddress)
serverSocket.listen(1)

print('listening on', serverAddress)

led.off()

# timer handling thread on the other CPU, so we must lock when modifying them
_thread.start_new_thread(runTimers, ())

# Listen for connections
while True:
    try:
        client, clientAddress = serverSocket.accept()
        print('client connected from', clientAddress)
        request = client.recv(1024)
        requestString = request.decode('ASCII')
        print('Content = %s' % requestString)
        requestParts = requestString.split()
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
        
        if target == '/airForm':
            solenoidLock.acquire()
            solenoidTimer.reinitialize(int(dictionary['onTime']),
                                       int(dictionary['offTime']),
                                       int(dictionary['startDelay']))
            solenoidLock.release()
            print('airForm fired')
        elif target == '/lpaForm':
            lpaLock.acquire()
            lpaPumpTimer.reinitialize(int(dictionary['onTime']),
                                  int(dictionary['offTime']),
                                  int(dictionary['startDelay']))
            lpaLock.release()
            print('lpaForm fired')
        elif target == '/aaForm':
            aaLock.acquire()
            aaPumpTimer.reinitialize(int(dictionary['onTime']),
                                  int(dictionary['offTime']),
                                  int(dictionary['startDelay']))
            aaLock.release()
            print('aaForm fired')
        elif target == '/airLedOn':
            solenoidLock.acquire()
            solenoidTimer.setUseLED(True)
            lpaPumpLock.acquire()
            lpaPumpTimer.setUseLED(False)
            aaPumpLock.acquire()
            aaPumpTimer.setUseLED(False)
            aaPumpLock.release()
            lpaPumpLock.release()
            solenoidLock.release()
            print('airLedOn fired')
        elif target == '/airLedOff':
            solenoidLock.acquire()
            solenoidTimer.setUseLED(False)
            solenoidLock.release()
            print('airLedOff fired')
        elif target == '/lpaLedOn':
            lpaPumpLock.acquire()
            lpaPumpTimer.setUseLED(True)
            solenoidLock.acquire()
            solenoidTimer.setUseLED(False)
            aaPumpLock.acquire()
            aaPumpTimer.setUseLED(False)
            aaPumpLock.release()
            solenoidLock.release()
            lpaPumpLock.release()
            print('lpaLedOn fired')
        elif target == '/lpaLedOff':
            lpaPumpLock.acquire()
            lpaPumpTimer.setUseLED(False)
            lpaPumpLock.release()
            print('lpaLedOff fired')
        elif target == '/aaLedOn':
            aaPumpLock.acquire()
            aaPumpTimer.setUseLED(True)
            solenoidLock.acquire()
            solenoidTimer.setUseLED(False)
            lpaPumpLock.acquire()
            lpaPumpTimer.setUseLED(False)
            lpaPumpLock.release()
            solenoidLock.release()
            aaPumpLock.release()
            print('aaLedOn fired')
        elif target == '/aaLedOff':
            aaPumpLock.acquire()
            aaPumpTimer.setUseLED(False)
            aaPumpLock.release()
            print('aaLedOff fired')
        elif target == '/testModeOn':
            if testModeOn == False:
                swapAndReset()
                testModeOn = True
        elif target == '/testModeOff':
            if testModeOn == True:
                swapAndReset()
                testModeOn = False            
        
        if httpMethod == 'GET':
            if target == '/favicon.ico':
                response = 'HTTP/1.1 404 Not Found\nConnection: close\n\n'
            else:
                response = buildHtml()
            client.send(response)
            print('returning html response to ', clientAddress, ':\n', response)

        client.close()

    except OSError as e:
        client.close()
        print('connection closed')
    except KeyboardInterrupt:
        machine.reset()




