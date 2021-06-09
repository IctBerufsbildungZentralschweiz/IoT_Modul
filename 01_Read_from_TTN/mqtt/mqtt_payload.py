import paho.mqtt.client as mqtt
import json
import mysql.connector
import base64
import requests

topic = "rak811-sensor/devices/rak811-sensor1/up"
mqttuser = "rak811-sensor"
mqttpw = "ttn-account-v2.Neb3eabv_CRqI6rI2yh1R2XZeMtPTHpL9bkGrVQcM1Q"
ttnurl = "eu.thethings.network"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # The MQTT toppic we will follow
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))

    # Decode JSON
    data = json.loads(msg.payload.decode('utf-8'))
    meta = data["metadata"]   
    gways = meta["gateways"]
    mqtttopic = msg.topic
    #Parsing
    counter = (data["counter"])
    dev_id = (data["dev_id"])
    hardware_serial = (data["hardware_serial"])
    payload_raw = (data["payload_raw"])
    payload_raw = base64.b64decode(payload_raw.encode())
    port = (data["port"])
    app_id = (data["app_id"])
    airtime=(meta["airtime"])

    coding_rate = (meta["coding_rate"])
    data_rate = (meta["data_rate"])
    frequency = (meta["frequency"])
    modulation = (meta["modulation"])
    
    rf_chain = (gways[0]["rf_chain"])
    rssi = (gways[0]["rssi"])
    snr = (gways[0]["snr"])
    tme = (gways[0]["time"])
    tmstmp = (gways[0]["timestamp"])
    channel = (gways[0]["channel"])
    

    # Insert in to MYSQL-Table
    sql = "INSERT INTO tbl_messages (airtime, app_id, channel, coding_rate, counter, dev_id, frequency, hardware_serial, modulation, payload_raw, port, rf_chain, rssi, snr, time, tmstmp, data_rate, topic) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (airtime, app_id, channel, coding_rate, counter, dev_id, frequency, hardware_serial, modulation, payload_raw, port, rf_chain, rssi, snr, tme, tmstmp,data_rate, mqtttopic)
    mycursor.execute(sql, val)
    mydb.commit()

#MySQL Conncetion Data
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="rak811_db")
mycursor = mydb.cursor()



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# Login Credentials
client.username_pw_set(mqttuser, mqttpw)

client.connect(ttnurl, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()