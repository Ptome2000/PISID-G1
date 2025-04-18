import json
import os
from datetime import datetime
import paho.mqtt.client as mqtt
import pymongo
from pymongo import MongoClient

# === [1] MongoDB connection ===
client = MongoClient("localhost", 27017)

# === [2] Logging setup ===
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = f"{log_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
with open(log_filename, "w") as log_file:
    log_file.write(f"Log file created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def log_error(error_message, payload=None):
    """Logs an error with timestamp and optional payload to the log file"""
    with open(log_filename, "a") as log_file:
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_entry = f"{timestamp} {error_message}"
        if payload is not None:
            log_entry += f" | Payload: {json.dumps(payload, indent=2)}"
        log_file.write(log_entry + "\n")

# === [3] MongoDB data insertion ===
def insertData(collectionName, message):
    """Parses MQTT message and inserts data into the corresponding MongoDB collection"""
    db = client["labirinto_pisid"]
    collection = db[collectionName]

    try:
        # Convert bytes to string and clean outer braces
        decoded_message = message.decode("utf-8").strip("{}")
        payload = {}

        for field in decoded_message.split(", "):
            key, value = field.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Type conversion
            try:
                if value.startswith('"') and value.endswith('"'):
                    value = value.strip('"')
                elif "." in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError as e:
                error_msg = f"Error converting '{value}': {e}"
                print(error_msg)
                log_error(error_msg, payload)
                continue

            payload[key] = value

        # Insert into MongoDB
        try:
            res = collection.insert_one(payload)
            print("Inserted:", res)
        except pymongo.errors.PyMongoError as e:
            error_msg = f"Error inserting into MongoDB: {e}"
            print(error_msg)
            log_error(error_msg, payload)

    except Exception as e:
        error_msg = f"Error processing MQTT message: {e}"
        print(error_msg)
        log_error(error_msg)

# === [4] MQTT callback: on connect ===
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("pisid_mazesound_1")
    client.subscribe("pisid_mazemov_1")

# === [5] MQTT callback: on message ===
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == "pisid_mazemov_1":
        insertData("movimento", msg.payload)
    elif msg.topic == "pisid_mazesound_1":
        insertData("ruido", msg.payload)

# === [6] MQTT client setup and loop ===
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("broker.emqx.io", 1883, 60)
mqttc.loop_forever()