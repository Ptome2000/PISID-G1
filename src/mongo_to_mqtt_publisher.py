import json
import time
import os
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from dotenv import load_dotenv

# ==============================
# System Settings
# ==============================

load_dotenv() 
broker_host = os.getenv("BROKER_HOST", "broker.emqx.io") # MQTT broker host (default: broker.emqx.io)
broker_port = int(os.getenv("BROKER_PORT", 1883)) # MQTT broker port (default: 1883)
replicas = os.getenv("REPLICA_SET") # Replicas
current_player = os.getenv("CURRENT_PLAYER" ,1) # current player

# ==============================
# MongoDB Connection
# ==============================

client = MongoClient(replicas)
db = client["labirinto_pisid"]

# ==============================
# Mongo Messages Settings
# ==============================

# Variables to track last messages for spam filtering
last_movimento = None
last_ruido = None
ruido_repeats = 0

# ==============================
# Helper Functions
# ==============================

def is_spam(collection_name, current_doc):
    """Check whether the document is considered spam based on recent history."""
    global last_movimento, last_ruido, ruido_repeats

    if collection_name == "movimento":
        if last_movimento == current_doc:
            return True  # Block repeated movement
        last_movimento = current_doc
        return False

    elif collection_name == "ruido":
        # TODO: alterar para comparar apenas o som, em vez do documento todo.
        if last_ruido == current_doc["Sound"]:
            ruido_repeats += 1
            if ruido_repeats > 1:
                return True  # Allow up to 1 repeated noise events
        else:
            last_ruido = current_doc["Sound"]
            ruido_repeats = 1
        return False

    return False

def send_data(collection_name, player):
    """Send unread documents from MongoDB to MQTT, applying spam filtering."""
    collection = db[collection_name]
    query = {
        "$and": [
            {"Player": int(player)},
            {"$or": [{"isRead": False}, {"isRead": {"$exists": False}}]}
        ]
    }

    documents = collection.find(query)
    topic = f"pisid_g1_{collection_name}_{player}"

    for doc in documents:
        mongo_id = doc["_id"]
        del doc["_id"]  # Remove _id for JSON serialization

        if is_spam(collection_name, doc):
            print(f"[SPAM] from '{collection_name}': {doc}")
        else:
            print(f"Sending to {topic}: {doc}")
            mqttc.publish(topic, json.dumps(doc).encode("utf-8"), qos=2)

        # Mark the document as read in MongoDB
        collection.update_one({"_id": mongo_id}, {"$set": {"isRead": True}})

# ==============================
# MQTT Callbacks
# ==============================

## This methods are called for testing purposes with a mocked topic
import threading

def start_sending_loop():
    while True:
        send_data("movimento", current_player)
        send_data("ruido", current_player)
        time.sleep(0.5)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    threading.Thread(target=start_sending_loop).start()
    # client.subscribe("pisid_g1_player")

# ==============================
# MQTT Setup
# ==============================

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.connect(broker_host, broker_port, 60)
mqttc.loop_forever()
