import paho.mqtt.client as mqtt
import json
import mysql.connector
import base64
import requests



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # The MQTT toppic we will follow
    client.subscribe("rak811-sensor/devices/rak811-sensor1/up")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))

    # Decode JSON
    data = json.loads(msg.payload.decode('utf-8'))
    meta = (json.dumps(data["metadata"]))    
    gateways_dict = json.dumps(meta("gateways"))
    print(gateways_dict)

    #print(meta)
    #*** airtime ***
    airtime=(gateways_dict["airtime"])
    #***  
    #app_id=
    app_id = (data["app_id"])
    #channel=
    channel = (gateways_dict["channel"])
    #***
    #*** coding_rate ***
    coding_rate = (meta["coding_rate"])
    #***
    #*** counter ***
    counter = (data["counter"])
    #***
    #*** data_rate ***
    data_rate = (meta["data_rate"])
    #***
    #*** dev_id ***
    dev_id = (data["dev_id"])
    #***
    #*** freqeuny ***
    frequency = (meta["frequency"])
    #***
    #*** gateways ***
    #***
    #hardware_serial
    hardware_serial = (data["hardware_serial"])
    #***
    #*** modulation ***
    #modulation = (data["modulation"])
    #***
    #*** payload_raw ***
    payload_raw = (data["payload_raw"])
    payload_raw = base64.b64decode(payload_raw.encode())
    #***
    #*** port ***
    port = (data["port"])
    #***
    #rf_chain=#*** time ***
    rf_chain = (gateways_dict["rf_chain"])
    #***
    #*** rssi ***
    rssi = (gateways_dict["rssi"])
    #***
    #*** snr ***
    snr = (gateways_dict["snr"])
    #***
    #*** time ***
    time = (gateways_dict["time"])
    #***


    print(airtime)
    # Insert in to MYSQL-Table
    sql = "INSERT INTO ***** (airtime, app_id, channel, coding_rate, counter, dev_id, frequency, hardware_serial, modulation, payload_raw, port, rf_chain, rssi, snr, time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (airtime, app_id, channel, coding_rate, dev_id, frequency, hardware_serial, modulation, payload_raw, port, rf_chain, rssi, snr, time)
    mycursor.execute(sql, val)
    mydb.commit()

#MySQL Conncetion Data
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="*****")
mycursor = mydb.cursor()



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# Login Credentials
client.username_pw_set("****", "****")

client.connect("eu.thethings.network", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()