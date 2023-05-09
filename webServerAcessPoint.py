import network
import machine
import socket
import _thread
import utime
from cycleTimer import CycleTimer
from picozero import pico_temp_sensor, pico_led

ssid = '<AccessPointTest>'
wifiPass = 'dingleberries'

# onboard LED for testing timers with
led = machine.Pin("LED",machine.Pin.OUT)

solenoidPin = 16
solenoidOnTime = 10
solenoidOffTime = 590
solenoidStartDelay = 0
solenoidIncrement = 0.1
solenoidLock = _thread.allocate_lock()
solenoidTimer = CycleTimer("Solenoid Timer", solenoidOnTime, solenoidOffTime, solenoidStartDelay, False, solenoidPin)

# aa = air atomizing
aaPumpPin = 15
aaPumpOnTime = 10
aaPumpOffTime = 590
aaPumpStartDelay = 0
aaPumpIncrement = 0.1
aaPumpLock = _thread.allocate_lock()
aaPumpTimer = CycleTimer("Air Atomizing Water Pump Timer", aaPumpOnTime, aaPumpOffTime, aaPumpStartDelay, True, aaPumpPin)

# lpa = low pressure aeroponic
lpaPumpPin = 17
lpaPumpOnTime = 200
lpaPumpOffTime = 5800
lpaPumpStartDelay = 0
lpaPumpIncrement = 1
lpaPumpLock = _thread.allocate_lock()
lpaPumpTimer = CycleTimer("Low Pressure Aeroponic Pump Timer", lpaPumpOnTime, lpaPumpOffTime, lpaPumpStartDelay, True, lpaPumpPin)

testSolenoidOnTime = 10
testSolenoidOffTime = 30
testSolenoidStartDelay = 0

testAaPumpOnTime = 10
testAaPumpOffTime = 30
testAaPumpStartDelay = 0

testLpaPumpOnTime = 200
testLpaPumpOffTime = 5800
testLpaPumpStartDelay = 0

testModeOn = False

def runTimers():
    index = 0
    while True:
        solenoidLock.acquire()
        solenoidTimer.tick()
        solenoidLock.release()
        
        aaPumpLock.acquire()
        aaPumpTimer.tick()
        aaPumpLock.release()
        
        lpaPumpLock.acquire()
        lpaPumpTimer.tick()
        lpaPumpLock.release()
        
        index += 1
        # sleep for a 100 milliseconds and go do it again
        utime.sleep_ms(100)
        # periodic logging so we know this thread is still running
        if index % 50 == 0:
            print(str(index / 10) + ' seconds')

def swapAndReset():
    solenoidLock.acquire()
    
    solenoidOnTime, testSolenoidOnTime = testSolenoidOnTime, solenoidOnTime
    solenoidOffTime, testSolenoidOffTime = testSolenoidOffTime, solenoidOffTime
    solenoidStartDelay, testSolenoidStartDelay = testSolenoidStartDelay, solenoidStartDelay
    solenoidTimer.reinitialize(solenoidOnTime, solenoidOffTime, solenoidStartDelay)
    
    solenoidLock.release()
    
    aaPumpLock.acquire()
    
    aaPumpOnTime, testAaPumpOnTime = testAaPumpOnTime, aaPumpOnTime
    aaPumpOffTime, testAaPumpOffTime = testAaPumpOffTime, aaPumpOffTime
    aaPumpStartDelay, testAaPumpStartDelay = testAaPumpStartDelay, aaPumpStartDelay
    
    aaPumpLock.release()
    
    lpaPumpLock.acquire()
    
    lpaPumpOnTime, testLpaPumpOnTime = testLpaPumpOnTime, lpaPumpOnTime
    lpaPumpOffTime, testLpaPumpOffTime = testLpaPumpOffTime, lpaPumpOffTime
    lpaPumpStartDelay, testLpaPumpStartDelay = testLpaPumpStartDelay, lpaPumpStartDelay
    
    lpaPumpLock.release()

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
                solenoidOnTime += solenoidIncrement
                print('solenoidOnTimeUp')
            elif action == '/solenoidOffTimeUp?':
                solenoidOffTime += solenoidIncrement
                print('solenoidOffTimeUp')
            elif action == '/solenoidStartDelayUp?':
                solenoidStartDelay += solenoidIncrement
                print('solenoidStartDelayUp')
            elif action == '/solenoidOnTimeDown?' and solenoidOnTime >= solenoidIncrement:
                solenoidOnTime -= solenoidIncrement
                print('solenoidOnTimeDown')
            elif action == '/solenoidOffTimeDown?' and solenoidOffTime >= solenoidIncrement:
                solenoidOffTime -= solenoidIncrement
                print('solenoidOffTimeDown')
            elif action == '/solenoidStartDelayDown?' and solenoidStartDelay >= solenoidIncrement:
                solenoidStartDelay -= solenoidIncrement
                print('solenoidStartDelayDown')
            else:
                changed = False
                print('unknown action for solenoid, skipping')               
            
            if changed:
                solenoidTimer.reinitialize(solenoidOnTime, solenoidOffTime, solenoidStartDelay)
                print('reinitializing solenoid timer')
                
            solenoidLock.release()
        elif action.startswith('/aaPump'):
            aaPumpLock.acquire()
            
            changed = True
            
            if action == '/aaPumpOnTimeUp?':
                aaPumpOnTime += aaPumpIncrement
                print('aaPumpOnTimeUp')
            elif action == '/aaPumpOffTimeUp?':
                aaPumpOffTime += aaPumpIncrement
                print('aaPumpOffTimeUp')
            elif action == '/aaPumpStartDelayUp?':
                aaPumpStartDelay += aaPumpIncrement
                print('aaPumpStartDelayUp')
            elif action == '/aaPumpOnTimeDown?' and aaPumpOnTime >= aaPumpIncrement:
                aaPumpOnTime -= aaPumpIncrement
                print('aaPumpOnTimeDown')
            elif action == '/aaPumpOffTimeDown?' and aaPumpOffTime >= aaPumpIncrement:
                aaPumpOffTime -= aaPumpIncrement
                print('aaPumpOffTimeDown')
            elif action == '/aaPumpStartDelayDown?' and aaPumpStartDelay >= aaPumpIncrement:
                aaPumpStartDelay -= aaPumpIncrement
                print('aaPumpStartDelayDown')
            else:
                changed = False
                print('unknown action for aaPump, skipping')              
            
            if changed:
                aaPumpTimer.reinitialize(aaPumpOnTime, aaPumpOffTime, aaPumpStartDelay)
                print('reinitializing AA timer')
                
            aaPump.release()
        elif action.startswith('/lpaPump'):
            lpaPumpLock.acquire()
            
            changed = True
            
            if action == '/lpaPumpOnTimeUp?':
                lpaPumpOnTime += lpaPumpIncrement
                print('lpaPumpOnTimeUp')
            elif action == '/lpaPumpOffTimeUp?':
                lpaPumpOffTime += lpaPumpIncrement
                print('lpaPumpOffTimeUp')
            elif action == '/lpaPumpStartDelayUp?':
                lpaPumpStartDelay += lpaPumpIncrement
                print('lpaPumpStartDelayUp')
            elif action == '/lpaPumpOnTimeDown?' and lpaPumpOnTime >= lpaPumpIncrement:
                lpaPumpOnTime -= lpaPumpIncrement
                print('lpaPumpOnTimeDown')
            elif action == '/lpaPumpOffTimeDown?' and lpaPumpOffTime >= lpaPumpIncrement:
                lpaPumpOffTime -= lpaPumpIncrement
                print('lpaPumpOffTimeDown')
            elif action == '/lpaPumpStartDelayDown?' and lpaPumpStartDelay >= lpaPumpIncrement:
                lpaPumpStartDelay -= lpaPumpIncrement
                print('lpaPumpStartDelayDown')
            else:
                changed = False
                print('unknown action for lpaPump, skipping')
            
            if changed == True:
                lpaPumpTimer.reinitialize(lpaPumpOnTime, lpaPumpOffTime, lpaPumpStartDelay)
                print('reinitializing LPA timer')
                
            lpaPumpLock.release()
        elif action == '/testModeOn?':
            if testModeOn == False:
                solenoidLock.acquire()
    
                solenoidOnTime, testSolenoidOnTime = testSolenoidOnTime, solenoidOnTime
                solenoidOffTime, testSolenoidOffTime = testSolenoidOffTime, solenoidOffTime
                solenoidStartDelay, testSolenoidStartDelay = testSolenoidStartDelay, solenoidStartDelay
                solenoidTimer.reinitialize(solenoidOnTime, solenoidOffTime, solenoidStartDelay)
                
                solenoidLock.release()
                
                aaPumpLock.acquire()
                
                aaPumpOnTime, testAaPumpOnTime = testAaPumpOnTime, aaPumpOnTime
                aaPumpOffTime, testAaPumpOffTime = testAaPumpOffTime, aaPumpOffTime
                aaPumpStartDelay, testAaPumpStartDelay = testAaPumpStartDelay, aaPumpStartDelay
                
                aaPumpLock.release()
                
                lpaPumpLock.acquire()
                
                lpaPumpOnTime, testLpaPumpOnTime = testLpaPumpOnTime, lpaPumpOnTime
                lpaPumpOffTime, testLpaPumpOffTime = testLpaPumpOffTime, lpaPumpOffTime
                lpaPumpStartDelay, testLpaPumpStartDelay = testLpaPumpStartDelay, lpaPumpStartDelay
                
                lpaPumpLock.release()
                testModeOn = True
        elif action == '/testModeOff?':
            if testModeOn == True:
                solenoidLock.acquire()
    
                solenoidOnTime, testSolenoidOnTime = testSolenoidOnTime, solenoidOnTime
                solenoidOffTime, testSolenoidOffTime = testSolenoidOffTime, solenoidOffTime
                solenoidStartDelay, testSolenoidStartDelay = testSolenoidStartDelay, solenoidStartDelay
                solenoidTimer.reinitialize(solenoidOnTime, solenoidOffTime, solenoidStartDelay)
                
                solenoidLock.release()
                
                aaPumpLock.acquire()
                
                aaPumpOnTime, testAaPumpOnTime = testAaPumpOnTime, aaPumpOnTime
                aaPumpOffTime, testAaPumpOffTime = testAaPumpOffTime, aaPumpOffTime
                aaPumpStartDelay, testAaPumpStartDelay = testAaPumpStartDelay, aaPumpStartDelay
                
                aaPumpLock.release()
                
                lpaPumpLock.acquire()
                
                lpaPumpOnTime, testLpaPumpOnTime = testLpaPumpOnTime, lpaPumpOnTime
                lpaPumpOffTime, testLpaPumpOffTime = testLpaPumpOffTime, lpaPumpOffTime
                lpaPumpStartDelay, testLpaPumpStartDelay = testLpaPumpStartDelay, lpaPumpStartDelay
                
                lpaPumpLock.release()
                testModeOn = False
        
        if httpMethod == 'GET':
            response = html.format(solenoidOnTime, solenoidOffTime, solenoidStartDelay, aaPumpOnTime, aaPumpOffTime, aaPumpStartDelay, lpaPumpOnTime, lpaPumpOffTime, lpaPumpStartDelay, testModeOn, 'font-size:50px;')
            client.send(response)
            print('returning html response to ', clientAddress)

        client.close()

    except OSError as e:
        client.close()
        print('connection closed')
    except KeyboardInterrupt:
        machine.reset()




