import json
import time
import paho.mqtt.client as mqtt
from pymongo import MongoClient

# ==============================
# MongoDB Connection
# ==============================

client = MongoClient("localhost", 27017)
db = client["labirinto_pisid"]

# ==============================
# Game State
# ==============================

current_player = 1  # Currently active player (default: 1)

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
        if last_ruido == current_doc:
            ruido_repeats += 1
            if ruido_repeats > 3:
                return True  # Allow up to 3 repeated noise events
        else:
            last_ruido = current_doc
            ruido_repeats = 1
        return False

    return False

def send_data(collection_name, player):
    """Send unread documents from MongoDB to MQTT, applying spam filtering."""
    collection = db[collection_name]

    query = {
        "$and": [
            {"Player": player},
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
            mqttc.publish(topic, json.dumps(doc), qos=2)

        # Mark the document as read in MongoDB
        collection.update_one({"_id": mongo_id}, {"$set": {"isRead": True}})

# ==============================
# MQTT Callbacks
# ==============================

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("pisid_g1_player")

def on_message(client, userdata, msg):
    global current_player
    print(f"{msg.topic} {msg.payload}")

    if msg.topic == "pisid_g1_player":
        data = json.loads(msg.payload)
        current_player = data["player"]
        print(f"Player set: {current_player}")

# ==============================
# MQTT Setup
# ==============================

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("broker.emqx.io", 1883, 60)
mqttc.loop_start()

# ==============================
# Main Loop
# ==============================

while True:
    if current_player:
        send_data("movimento", current_player)
        send_data("ruido", current_player)
    time.sleep(0.5)