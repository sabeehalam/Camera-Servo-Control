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

def mqttCallback(topic, msg):
    global received_message
    print(f"Received message on topic: {topic.decode()} - Message: {msg.decode()}")
    received_message = msg.decode()
    
'''Connect to MQTT Broker'''
def connectMQTTBroker():
  print("Connecting to MQTT server... ", end="")
  client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD, \
                        keepalive = KEEP_ALIVE_DURATION, port = MQTT_PORT)
  client.set_callback(mqtt_callback)
  client.connect()
  print("Connected!")
  return client

'''After connectiong to MQTT broker, subscribe to topic for receiving box-image center delta to find servo rotation angle'''
def subscribeMQTT(client, subscribe_topic):
  client.subscribe(subscribe_topic)

'''D3eclare constants for program'''
WIFI_NAME = "Embedded"
WIFI_PASSWORD = "password1"
MQTT_CLIENT_ID = "Monitor Camera"
MQTT_BROKER = "192.168.120.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
KEEP_ALIVE_DURATION = 0
MQTT_PORT = 1883
MQTT_TOPIC = "vectracom/monitor/publish"
MQTT_PUBLISH_TIME_GAP = 10
MQTT_SUBSCRIBE_TOPIC = "vectracom/monitor/subscribe"
MQTT_SUBSCRIBE_TIME_GAP = 10
TILT_PIN = 4
PAN_PIN = 5

'''Declare message receive string'''
received_message = {}
def main():
    '''Declare Servo objects '''
    tilt = Servo(TILT_PIN)
    pan = Servo(PAN_PIN)

    '''Establish connections to WiFi and MQTT'''
    connectWiFi(WIFI_NAME, WIFI_PASSWORD)
    mqtt_client = connectMQTTBroker()
    mqtt_client.set_callback(mqttCallback)
    subscribeMQTT(mqtt_client, MQTT_SUBSCRIBE_TOPIC)
    
    tilt.move(0)
    pan.move(0)
    while True:
        mqtt_client.wait_msg()
        offset_x = received_message['offset_x']
        offset_y = received_message['offset_y']
        while(offset_x! = 0 and offset_y != 0):
            tilt.move(offset_y) # tourne le servo à 0°
            time.sleep(0.5)

            pan.move(offset_x) # tourne le servo à 0°
            time.sleep(0.5)
            
            offset_x = 0
            offset_y = 0
