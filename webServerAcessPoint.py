import network
import machine
import socket
import _thread
import utime
from cycleTimer import CycleTimer
from picozero import pico_led

# for demonstration purposes, use your own credentials
ssid = '<AccessPointTest2>'
wifiPass = 'dingleberries'

# timer resolution in milliseconds
# Lower for better resolution, raise for lower power consumption
tickSizeMs = 100

# onboard LED for testing timers with
led = machine.Pin("LED",machine.Pin.OUT)

# controls the solenoid for the air line leading to the nozzle
solenoidPin = 16
solenoidOnTimeMs = 1000
solenoidOffTimeMs = 59000
solenoidStartDelayMs = 0
solenoidIncrementMs = 100
solenoidLock = _thread.allocate_lock()
solenoidTimer = CycleTimer("Solenoid Timer", solenoidOnTimeMs, solenoidOffTimeMs, solenoidStartDelayMs, False, tickSizeMs, solenoidPin)

# circulation pump for the reservoir
circulationPumpPin = 17
circulationPumpOnTimeMs = 60000
circulationPumpOffTimeMs = 1800000
circulationPumpStartDelayMs = 0
circulationPumpIncrementMs = 1000
circulationPumpLock = _thread.allocate_lock()
circulationPumpTimer = CycleTimer("Circulation Pump Timer", circulationPumpOnTimeMs, circulationPumpOffTimeMs, circulationPumpStartDelayMs, True, tickSizeMs, circulationPumpPin)

testSolenoidOnTimeMs = 1000
testSolenoidOffTimeMs = 3000
testSolenoidStartDelayMs = 0

testCirculationPumpOnTimeMs = 10000
testCirculationPumpOffTimeMs = 10000
testCirculationPumpStartDelayMs = 0

testModeOn = False

def runTimers():
    index = 0
    while True:
        solenoidLock.acquire()
        solenoidTimer.tick()
        solenoidLock.release()
        
        circulationPumpLock.acquire()
        circulationPumpTimer.tick()
        circulationPumpLock.release()
        
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
    global circulationPumpOnTimeMs
    global testCirculationPumpOnTimeMs
    global circulationPumpOffTimeMs
    global testCirculationPumpOffTimeMs
    global circulationPumpStartDelayMs
    global testCirculationPumpStartDelayMs
    
    solenoidLock.acquire()
    
    solenoidOnTimeMs, testSolenoidOnTimeMs = testSolenoidOnTimeMs, solenoidOnTimeMs
    solenoidOffTimeMs, testSolenoidOffTimeMs = testSolenoidOffTimeMs, solenoidOffTimeMs
    solenoidStartDelayMs, testSolenoidStartDelayMs = testSolenoidStartDelayMs, solenoidStartDelayMs
    solenoidTimer.reinitialize(solenoidOnTimeMs, solenoidOffTimeMs, solenoidStartDelayMs)
    
    solenoidLock.release()
    
    circulationPumpLock.acquire()
    
    circulationPumpOnTimeMs, testCirculationPumpOnTimeMs = testCirculationPumpOnTimeMs, circulationPumpOnTimeMs
    circulationPumpOffTimeMs, testCirculationPumpOffTimeMs = testCirculationPumpOffTimeMs, circulationPumpOffTimeMs
    circulationPumpStartDelayMs, testCirculationPumpStartDelayMs = testCirculationPumpStartDelayMs, circulationPumpStartDelayMs
    
    circulationPumpLock.release()

accessPoint = network.WLAN(network.AP_IF)
accessPoint.config(essid=ssid, password=wifiPass)
accessPoint.active(True)

while accessPoint.active() == False:
  pass

print('Access point established')
print('ifconfig = ' + str(accessPoint.ifconfig()))

htmlFile = open('index.html', 'r')
html = htmlFile.read()
htmlFile.close()

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
        
        if action.startswith('/solenoid'):
            solenoidLock.acquire()
            
            changed = True
            
            if action == '/solenoidOnTimeUp?':
                solenoidOnTimeMs += solenoidIncrementMs
                print('solenoidOnTimeUp')
            elif action == '/solenoidOffTimeUp?':
                solenoidOffTimeMs += solenoidIncrementMs
                print('solenoidOffTimeUp')
            elif action == '/solenoidStartDelayUp?':
                solenoidStartDelayMs += solenoidIncrementMs
                print('solenoidStartDelayUp')
            elif action == '/solenoidOnTimeDown?' and solenoidOnTimeMs >= 0:
                solenoidOnTimeMs -= solenoidIncrementMs
                print('solenoidOnTimeDown')
            elif action == '/solenoidOffTimeDown?' and solenoidOffTimeMs >= 0:
                solenoidOffTimeMs -= solenoidIncrementMs
                print('solenoidOffTimeDown')
            elif action == '/solenoidStartDelayDown?' and solenoidStartDelayMs >= 0:
                solenoidStartDelayMs -= solenoidIncrementMs
                print('solenoidStartDelayDown')
            elif action == '/solenoidSetUseLED?':
                solenoidTimer.setUseLED(True)
                
                circulationPumpLock.acquire()
                circulationPumpTimer.setUseLED(False)
                circulationPumpLock.release()
                
                print('solenoidSetUseLed')
            else:
                changed = False
                print('unknown action for solenoid, skipping')               
            
            if changed:
                solenoidTimer.reinitialize(solenoidOnTimeMs, solenoidOffTimeMs, solenoidStartDelayMs)
                print('reinitializing solenoid timer')
                
            solenoidLock.release()
        elif action.startswith('/circulationPump'):
            circulationPumpLock.acquire()
            
            changed = True
            
            if action == '/circulationPumpOnTimeUp?':
                circulationPumpOnTimeMs += circulationPumpIncrementMs
                print('circulationPumpOnTimeUp')
            elif action == '/circulationPumpOffTimeUp?':
                circulationPumpOffTimeMs += circulationPumpIncrementMs
                print('circulationPumpOffTimeUp')
            elif action == '/circulationPumpStartDelayUp?':
                circulationPumpStartDelayMs += circulationPumpIncrementMs
                print('circulationPumpStartDelayUp')
            elif action == '/circulationPumpOnTimeDown?' and circulationPumpOnTimeMs >= 0:
                circulationPumpOnTimeMs -= circulationPumpIncrementMs
                print('circulationPumpOnTimeDown')
            elif action == '/circulationPumpOffTimeDown?' and circulationPumpOffTimeMs >= 0:
                circulationPumpOffTimeMs -= circulationPumpIncrementMs
                print('circulationPumpOffTimeDown')
            elif action == '/circulationPumpStartDelayDown?' and circulationPumpStartDelayMs >= 0:
                circulationPumpStartDelayMs -= circulationPumpIncrementMs
                print('circulationPumpStartDelayDown')
            elif action == '/circulationPumpUseLED?':
                circulationPumpTimer.setUseLED(True)
                
                solenoidLock.release()
                solenoidTimer.setUseLED(False)
                solenoidLock.release()
                
                print('circulationPumpUseLED')
            else:
                changed = False
                print('unknown action for circulationPump, skipping')              
            
            if changed:
                circulationPumpTimer.reinitialize(circulationPumpOnTimeMs, circulationPumpOffTimeMs, circulationPumpStartDelayMs)
                print('reinitializing circulation pump timer')
                
            circulationPumpLock.release()
        elif action == '/testModeOn?':
            if testModeOn == False:
                swapAndReset()
                testModeOn = True
        elif action == '/testModeOff?':
            if testModeOn == True:
                swapAndReset()
                testModeOn = False
        
        if httpMethod == 'GET':
            response = html.format('{font-size:50px;}', solenoidOnTimeMs, solenoidOffTimeMs, solenoidStartDelayMs, solenoidTimer.isUsingLED(), circulationPumpOnTimeMs, circulationPumpOffTimeMs, circulationPumpStartDelayMs, solenoidTimer.isUsingLED(), testModeOn)
            client.send(response)
            print('returning html response to ', clientAddress)

        client.close()

    except OSError as e:
        client.close()
        print('connection closed')
    except KeyboardInterrupt:
        machine.reset()




