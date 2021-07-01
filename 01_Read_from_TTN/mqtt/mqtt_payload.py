import paho.mqtt.client as mqtt
import json
import mysql.connector
import base64
import requests

topic = "your_toppic"
mqttuser = "your_user"
mqttpw = "your_pw"
ttnurl = "eu1.cloud.thethings.network"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # The MQTT toppic we will follow
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    # Decode JSON
    data = json.loads(msg.payload.decode('utf-8'))
    dev_id = ((data["end_device_ids"])["device_id"])
    mqtttopic = msg.topic
    #Parsing
    hardware_serial = ((data["end_device_ids"])["dev_eui"])
    
    port = ((data["uplink_message"])["f_port"])
    app_id = (((data["end_device_ids"])["application_ids"])["application_id"])
    airtime=((data["uplink_message"])["consumed_airtime"])
    counter=((data["uplink_message"])["f_cnt"])
    coding_rate = (((data["uplink_message"])["settings"])["coding_rate"])
    data_rate = (((data["uplink_message"])["settings"])["data_rate_index"])
    frequency = (((data["uplink_message"])["settings"])["frequency"])
    
    gtw_id = (((((data["uplink_message"])["rx_metadata"])[0])["gateway_ids"])["gateway_id"])
    rssi = ((((data["uplink_message"])["rx_metadata"])[0])["rssi"])
    snr = ((((data["uplink_message"])["rx_metadata"])[0])["snr"])
    tme = ((((data["uplink_message"])["rx_metadata"])[0])["time"])
    tmstmp = ((((data["uplink_message"])["rx_metadata"])[0])["timestamp"])
    channel = ((((data["uplink_message"])["rx_metadata"])[0])["channel_index"])
    payload_raw = ((data["uplink_message"])["frm_payload"])
    payload_raw = base64.b64decode(payload_raw.encode())
    
    print(payload_raw)
    tmp=payload_raw[0:5]
    hum=payload_raw[10:15]

    print(tmp, hum)
    # Insert in to MYSQL-Table
    sql = "INSERT INTO tbl_messages (counter, airtime, app_id, channel, coding_rate, dev_id, frequency, hardware_serial, payload_raw, port, rssi, snr, time, tmstmp, data_rate, topic,hum, tmp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (counter, airtime, app_id, channel, coding_rate,  dev_id, frequency, hardware_serial, payload_raw, port, rssi, snr, tme, tmstmp,data_rate, mqtttopic, hum, tmp)
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