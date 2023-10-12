from umqtt.robust import MQTTClient
    
'''Connect to MQTT Broker'''
def connectMQTTBroker(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_USER, MQTT_PASSWORD, KEEP_ALIVE_DURATION, MQTT_PORT):
  print("Connecting to MQTT server... ", end="")
  client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD, \
                        keepalive = KEEP_ALIVE_DURATION, port = MQTT_PORT)
  return client

'''After connecting to MQTT broker, subscribe to topic for receiving box-image center delta to find servo rotation angle'''
def subscribeMQTT(client, subscribe_topic):
  client.subscribe(subscribe_topic)