def mqttCallback(topic, msg):
    global received_message
#     print(f"Received message on topic: {topic.decode()} - Message: {msg.decode()}")
    received_message = msg.decode()
#     print(received_message)

def main():
    global received_message
    '''Declare local access point variables for access'''
    ap_after_con = 0
    AP = 1
#     print(parameters_changeable)
#     print(WIFI_NAME, WIFI_PASSWORD, MQTT_CLIENT_ID, MQTT_BROKER, MQTT_USER, MQTT_PASSWORD, KEEP_ALIVE_DURATION, MQTT_PORT, MQTT_PUBLISH_TOPIC, MQTT_SUBSCRIBE_TOPIC)
    
    '''Start location coordinates of the camera according to servos'''
    location_x = START_X
    location_y = START_Y
    
    '''Declare Servo objects '''
    tilt_servo = Servo(TILT_PIN)
    pan_servo = Servo(PAN_PIN)

    '''Establish connections to WiFi and MQTT and create instance of '''
    wifi_client = wifi_ap.connectWiFi(WIFI_NAME, WIFI_PASSWORD)
    ap_client = wifi_ap.makeAccessPoint(ACCESS_POINT_NAME, ACCESS_POINT_PASSWORD)
    web_socket = settings_server.createSocket(WEB_SERVER, WEB_PORT)  #Create a socket for web server
    mqtt_client = mqtt.connectMQTTBroker(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_USER, MQTT_PASSWORD, KEEP_ALIVE_DURATION, MQTT_PORT)
    mqtt_client.set_callback(mqttCallback)
    mqtt_client.connect()
    print("Connected!")
    mqtt.subscribeMQTT(mqtt_client, MQTT_SUBSCRIBE_TOPIC)
     
    '''Move the servo to initial location''' 
    tilt_servo.move(location_x)
    pan_servo.move(location_y)
    
    '''Define a variable for loading webpage'''
    html_webpage = webpage.getWebPage()
    
    while True:
      '''Check whether a client is connected to access point to transfer control to access point to host web server'''  
      while ap_client.isconnected() and AP == 0 and ap_after_con == 0:
        if not ap_client.isconnected():
          AP = 1
        try:
          client, address = web_socket.accept() #Accept the connection from client to web server
          print('Got a connection from %s' % str(address))
          settings_server.respondWebServer(client, html_webpage) #Send the webpage to the web server
          request = settings_server.receiveWebServer(client).decode("utf-8") #Await a response from the web server
          
          if request is not None: #If something is received
            data = str(request)
            referer = request_to_json.extractReferer(data) #Remove initial part of URL
          else:
            referer = None
          
          if referer is not None: #If any parameter is left after the referer from received URL
            params = request_to_json.extractRefererParams(referer)
          else:
            params = None
          
          if params == {}: #If params field is an empty dictionary
            params = None
          
          if params is not None: #If parameters are found from received URL
            print(params)
            ap_after_con = request_to_json.saveVariables(params)
            AP = 1
            print(ap_after_con, AP)
            break
        except (OSError, NameError) as e:
          pass
    
      while AP == 1:
        '''If client is connected to AP and never connected before change AP to 0 to transfer control to AP code'''
        if ap_client.isconnected() and ap_after_con == 0:
          print("ap_client.isconnected() and ap_after_con == 0")
          AP = 0
        
        '''Íf client has connected and chenged settings, then reset microcontroller'''
        if ap_client.isconnected() and ap_after_con == None:
          print("if ap_client.isconnected() and ap_after_con == None:")
          ap_client.active(False)
          sleep(10)
          machine.reset()
        
        check_msg_return = mqtt_client.check_msg()
        if check_msg_return is not None:
#           print(received_message)
          received_message = ujson.loads(received_message)                         
          offset_x = float(received_message["offset_x"])
          offset_y = float(received_message["offset_y"])
#           print(offset_x, offset_y)
        
          if(offset_x != 0 and offset_y != 0):
            '''Calculate temporary x, y coordinates for checking range of both axes'''
            location_x_temp = location_x + offset_x
            location_y_temp = location_y + offset_y
#             print(location_x_temp, location_y_temp)
            if(location_y_temp < 180 and location_y_temp > 0):
              tilt_servo.move(location_y_temp) # tourne le servo à 0°
              location_y += offset_y
            if(location_x_temp < 180 and location_x_temp > 0):
              pan_servo.move(location_x_temp) # tourne le servo à 0°
              location_x += offset_x  
            received_message = {"offset_x":0, "offset_y":0}

if __name__ == "__main__":
    main()