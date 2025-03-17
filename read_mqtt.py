import json
import re
import paho.mqtt.client as mqtt
import pymongo
from pymongo import MongoClient
client = MongoClient("localhost", 27017)

# connect to database
def insertData(collectionName, message):
    db = client["labirinto_pisid"]
    collection = db[collectionName]

    try:
        # Step 1: Decode bytes to string
        decoded_message = message.decode("utf-8").strip("{}")  # Remove surrounding {}

        # Step 2: Iterate and construct a dictionary
        payload = {}
        for field in decoded_message.split(", "):  # Split key-value pairs
            key, value = field.split(":", 1)  # Split key and value
            key = key.strip()  # Remove spaces

            # Check if the value is a string (has quotes)
            value = value.strip()

            try:
                if value.startswith('"') and value.endswith('"'):
                    value = value.strip('"')  # Remove quotes
                # Check if the value is a number (int or float)
                elif "." in value:
                    value = float(value)  # Convert to float
                else:
                    value = int(value)  # Convert to int
            except ValueError as e:
                print(f"error while converting '{value}': {e}")
                continue

            payload[key] = value  # Add to dictionary

        payload["isRead"] = False

        try:
            res = collection.insert_one(payload)
            print("Inserted: " + str(res))
        except pymongo.errors.PyMongoError as e:
            print(f"error while inserting: {e}")

    except Exception as e:
        print(f"error while porocessing MQTT message: {e}")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("pisid_mazesound_1")
    client.subscribe("pisid_mazemov_1")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if (msg.topic == "pisid_mazemov_1"):
        insertData("movimento", msg.payload)
    if (msg.topic == "pisid_mazesound_1"):
        insertData("ruido", msg.payload)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("broker.mqtt-dashboard.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()

