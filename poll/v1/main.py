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
#     print(f"Received message on topic: {topic.decode()} - Message: {msg.decode()}")
    received_message = msg.decode()
    
'''Connect to MQTT Broker'''
def connectMQTTBroker():
  print("Connecting to MQTT server... ", end="")
  client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD, \
                        keepalive = KEEP_ALIVE_DURATION, port = MQTT_PORT)
  client.set_callback(mqttCallback)
  client.connect()
  print("Connected!")
  return client

'''After connectiong to MQTT broker, subscribe to topic for receiving box-image center delta to find servo rotation angle'''
def subscribeMQTT(client, subscribe_topic):
  client.subscribe(subscribe_topic)

'''Declare constants for program'''
WIFI_NAME = "Extensity"
WIFI_PASSWORD = "password1"
MQTT_CLIENT_ID = "Monitor Camera"
MQTT_BROKER = "192.168.120.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
KEEP_ALIVE_DURATION = 0
MQTT_PORT = 1883
MQTT_SUBSCRIBE_TOPIC = "vectracom/monitor/subscribe"
TILT_PIN = 4
PAN_PIN = 5
START_X = 45
START_Y = 45

'''Declare message receive string'''
received_message = {"offset_x":0, "offset_y":0}

def main():
    global received_message
    '''Start location coordinates of the camera according to servos'''
    location_x = START_X
    location_y = START_Y
    
    '''Declare Servo objects '''
    tilt_servo = Servo(TILT_PIN)
    pan_servo = Servo(PAN_PIN)

    '''Establish connections to WiFi and MQTT'''
    wifi_client = connectWiFi(WIFI_NAME, WIFI_PASSWORD)
    mqtt_client = connectMQTTBroker()
    mqtt_client.set_callback(mqttCallback)
    subscribeMQTT(mqtt_client, MQTT_SUBSCRIBE_TOPIC)
    
    tilt_servo.move(location_x)
    pan_servo.move(location_y)
    
    while True:
        mqtt_client.wait_msg()
#         print(received_message,type(received_message))
        received_message = ujson.loads(received_message)                         
        offset_x = int(received_message["offset_x"])
        offset_y = int(received_message["offset_y"])
        print(offset_x, offset_y)
        if(offset_x != 0 and offset_y != 0):
          tilt_servo.move(location_y + offset_y) # tourne le servo à 0°
          sleep(0.75)

          pan_servo.move(location_x + offset_x) # tourne le servo à 0°
          sleep(0.75)
            
          location_x += offset_x
          location_y += offset_y 
            
          received_message = {"offset_x":0, "offset_y":0}

if __name__ == "__main__":
    main()