import network
from time import time, sleep

'''Connect ESP8266 to WiFi'''
def connectWiFi(WIFI_NAME, WIFI_PASSWORD):
    time_now = time()
    print("Connecting to WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_NAME, WIFI_PASSWORD)
    while sta_if.isconnected()==0 and (time()-time_now <= 10):
#         print(time()-time_now > 10)
        sleep(0.1)
    if sta_if.isconnected():
        print("Connected to WiFi!")
    return sta_if

'''Make the ESP8266 an access point'''
def makeAccessPoint(ACCESS_POINT_NAME, ACCESS_POINT_PASSWORD):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ACCESS_POINT_NAME, password=ACCESS_POINT_PASSWORD)
    while ap.active() == False:
      pass
    print('Access Point enabled successfully')
    print(ap.ifconfig())
    return ap