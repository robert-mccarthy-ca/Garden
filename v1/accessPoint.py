import network
import machine
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led

ssid = '<your ssid here>'
wifiPass = '<your password here>'

led = machine.Pin("LED",machine.Pin.OUT)

accessPoint = network.WLAN(network.AP_IF)
accessPoint.config(essid=ssid, password=wifiPass)
accessPoint.active(True)

while accessPoint.active() == False:
  pass

print('Connection successful')
print('ifconfig = ' + str(accessPoint.ifconfig()))

html = """<!DOCTYPE html>
<html>
    <head> <title>Basic Operational Access Point</title> </head>
    <body> <h1>Acess Point</h1>
        <p>access point webpage</p>
    </body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)
led.off()

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        led.on()
        print(request)

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()
        led.off()

    except OSError as e:
        cl.close()
        print('connection closed')



