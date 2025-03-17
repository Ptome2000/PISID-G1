import json
import re
import paho.mqtt.client as mqtt
import pymongo
from pymongo import MongoClient
client = MongoClient("localhost", 27017)

db = client["labirinto_pisid"]
collection = db["movimento"]

query = {"$or": [{"isRead": False}, {"isRead": {"$exists": False}}]}
movimentos = collection.find(query, {"_id": 0})

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("pisid_g1_movimento_1")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.connect("broker.mqtt-dashboard.com", 1883, 60)

for x in movimentos:
    print(x)
    # Verificar o que é spam e o que não é

    # enviar para o MQTT este registo
    mqttc.publish("pisid_g1_movimento_1", json.dumps(x), 2)
    # atualizar na base de dados para isRead=True



