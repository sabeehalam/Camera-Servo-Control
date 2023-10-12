# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
import uos
import machine
import micropython
from servo import Servo
from machine import Pin
from micropython import const
from umqtt.robust import MQTTClient
from time import sleep, localtime, time, sleep_ms
import ntptime
import network
import ujson
import usocket as socket
import request_to_json
import wifi_ap
import mqtt
import settings_server
import webpage

#webrepl.start()
gc.collect()

try:
    parameters_changeable, parameters_unchangeable = request_to_json.loadParameters()
except:
    pass

'''Load GPIO pins and start positions of servo motor'''
TILT_PIN = const(5)
PAN_PIN = const(4)
START_X = const(45)
START_Y = const(45)    

'''WiFi Parameters'''
try:
    WIFI_NAME = parameters_changeable["Wifi-Name"]
    WIFI_PASSWORD = parameters_changeable["Wifi-Password"]
except (ValueError, NameError, KeyError):
    WIFI_NAME = "Extensity"
    WIFI_PASSWORD = "password1"

'''MQTT Server Parameters'''
try:
    MQTT_CLIENT_ID = parameters_changeable["MqttClientID"]
except (ValueError, NameError, KeyError):
    MQTT_CLIENT_ID = "Camera Monitor"

try:
    MQTT_BROKER = parameters_changeable["MqttBroker"]
except (ValueError, NameError, KeyError):
    MQTT_BROKER = "192.168.120.164"

try:
    MQTT_USER = parameters_changeable["MqttUSER"]
except (ValueError, NameError, KeyError):
    MQTT_USER = ""

try:
    MQTT_PASSWORD = parameters_changeable["MqttPassword"]
except (ValueError, NameError, KeyError):
    MQTT_PASSWORD = ""
    
try:    
    KEEP_ALIVE_DURATION = int(parameters_changeable["KeepAlive"])
except (ValueError, NameError, KeyError):
    KEEP_ALIVE_DURATION = 0
    
try:
    MQTT_PORT = int(parameters_changeable["MqttPort"])
except (ValueError, NameError, KeyError):
    MQTT_PORT = 1883
    
'''MQTT Publish/Subscribe Parameters'''
try:
    MQTT_PUBLISH_TOPIC = parameters_changeable["MqttPublishTopic"]
    MQTT_PUBLISH_TIME_GAP = int(parameters_changeable["MqttPublishTime"])
except (ValueError, NameError, KeyError):
    MQTT_PUBLISH_TOPIC = "vectracom/monitor/publish"
    MQTT_PUBLISH_TIME_GAP = 10
    
try:
    MQTT_SUBSCRIBE_TOPIC = parameters_changeable["MqttSubscribeTopic"]
except (ValueError, NameError, KeyError):
    MQTT_SUBSCRIBE_TOPIC = "vectracom/monitor/subscribe"
    
'''Access Point parameters'''
try:
    ACCESS_POINT_NAME = parameters_unchangeable["AP_Name"]
    ACCESS_POINT_PASSWORD = parameters_unchangeable["AP_Password"]
except (ValueError, NameError, KeyError):
    ACCESS_POINT_NAME = "Camera Monitor"
    ACCESS_POINT_PASSWORD = "password"
    
'''Web Server Parameters'''
try:
    WEB_SERVER = parameters_unchangeable["WebServer"]
    WEB_PORT = int(parameters_unchangeable["WebPort"])
except (ValueError, NameError, KeyError):
    WEB_SERVER = "192.168.4.1"
    WEB_PORT = 80
