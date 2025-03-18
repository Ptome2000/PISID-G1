import json
import re
import paho.mqtt.client as mqtt
import pymongo
from pymongo import MongoClient
client = MongoClient("localhost", 27017)

db = client["labirinto_pisid"]


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("pisid_g1_movimento_1")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.connect("broker.mqtt-dashboard.com", 1883, 60)


def sendData(collectionName):
    collection = db[collectionName]
    query = {"$or": [{"isRead": False}, {"isRead": {"$exists": False}}]}
    data = collection.find(query)
    for row in data:
        mongo_id = row["_id"]  # Guarda o _id antes de remover, para usar mais tarde ao fazer o update
        del row["_id"]  # Remove o _id do objeto antes do JSON dump
        print(row)
        # Verificar o que é spam e o que não é

        # enviar para o MQTT este registo
        mqttc.publish("pisid_g1_movimento_1", json.dumps(row), 2)
        # atualizar na base de dados para isRead=True
        collection.update_one({"_id": mongo_id}, {"$set": {"isRead": True}})


sendData("movimento")

