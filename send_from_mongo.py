import json
import time
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import threading
client = MongoClient("localhost", 27017)

db = client["labirinto_pisid"]


def start_game(player):
    print("Esta é uma thread")
    while True:
        sendData("movimento", player)
        sendData("ruido", player)
        time.sleep(0.5)  # Espera 0.5 segundos antes da próxima execução

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("pisid_g1_player")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    data = json.loads(msg.payload)
    if msg.topic == "pisid_g1_player":
        thread = threading.Thread(target=start_game, args=(data["player"],))
        thread.start()


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("broker.mqtt-dashboard.com", 1883, 60)


def sendData(collectionName, player):
    print("player", player, collectionName)
    collection = db[collectionName]
    query = {
        "$and": [
            {"Player": player},
            {"$or": [{"isRead": False}, {"isRead": {"$exists": False}}]}
        ]
    }
    data = collection.find(query)

    topic = f"pisid_g1_{collectionName}_{player}"
    for row in data:
        mongo_id = row["_id"]  # Guarda o _id antes de remover, para usar mais tarde ao fazer o update
        del row["_id"]  # Remove o _id do objeto antes do JSON dump
        print(row)
        # Verificar o que é spam e o que não é

        # enviar para o MQTT este registo
        mqttc.publish(topic, json.dumps(row), 2)
        # atualizar na base de dados para isRead=True
        collection.update_one({"_id": mongo_id}, {"$set": {"isRead": True}})


mqttc.loop_forever()

