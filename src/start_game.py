import subprocess
import threading
from pathlib import Path
import random

import mysql.connector
import sys
import os
import paho.mqtt.client as mqtt
import time
from utils.Enums import GameActions

db_host = os.getenv("DB_HOST", "localhost") # DB host (default: localhost)
db_user = os.getenv("DB_USER", "root") # MySQL user (default: root)
db_password = os.getenv("DB_PASSWORD", "") # MySQL password (default: empty)
sql_db = os.getenv("SQL_DB", "marsami_game") # MySQL database (default: marsami_game)
broker_host = os.getenv("BROKER_HOST", "broker.emqx.io")
broker_port = int(os.getenv("BROKER_PORT", 1883))
current_player = os.getenv("CURRENT_PLAYER", 1) # Currently active player (default: 1)
timeout = 60

# guardar argumentos recebidos
if len(sys.argv) != 4:
    print("Usage: python start_game.py user name description")
    sys.exit(1)

gameUser = sys.argv[1]
gameName = sys.argv[2]
gameDescription = sys.argv[3]


# Conectar ao MQTT e enviar SYN -> PC1 e SYN -> PC2 com timeout de 30s

# pegar dados do MYSQL Cloud
def connect_mysql_cloud():
    try:
        connection = mysql.connector.connect(
            host="194.210.86.10",
            user="aluno",
            password="aluno",
            database="maze"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

# Criar novo jogo na bd marsamis
def connect_mysql_pc2():
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=sql_db
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
def getSettings():
    conn = connect_mysql_cloud()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM setupmaze")
    settings = cursor.fetchone()
    return settings

def createMysqlGame():
    settings = getSettings()
    conn = connect_mysql_pc2()
    cursor = conn.cursor(dictionary=True)

    game_name = "Jogo Exemplo"
    game_description = "Descrição do jogo"

    # Chamar stored procedure com parâmetros
    cursor.callproc("createGame", [
        gameUser,
        gameName,
        gameDescription,
        settings["numbermarsamis"],
        settings["noisevartoleration"],
        settings["normalnoise"]
    ])

    print('SP called')
    conn.commit()  # <- obrigatório para gravar alterações na BD
    cursor.close()
    conn.close()


# correr o jogo
def score(client):
    # TODO: pegar room da base de dados
    room = random.randint(1, 10)
    message = {"Type": "Score", "Player": current_player, "Room": room}
    print(str(message))
    client.publish("pisid_mazeact", str(message))
def play_game(client):
    action = random.randint(1, 5)
    match action:
        case GameActions.SCORE:
            score(client)
            print("SCORE")
        case GameActions.OPEN_DOOR:
            print("OPEN_DOOR")
        case GameActions.CLOSE_DOOR:
            print("CLOSE_DOOR")
        case GameActions.OPEN_ALL_DOOR:
            print("OPEN_ALL_DOOR")
        case GameActions.CLOSE_ALL_DOOR:
            print("CLOSE_ALL_DOOR")


# controlar estados do jogo

PC1_READY = 0
PC2_READY = 0

def controlState(client):
    global PC1_READY, PC2_READY
    try:
        timeOutState = True
        for i in range(timeout):
            if PC1_READY < 2:
                client.publish("g1_control_pc1", "SYN")
                print('Send SYN PC1')
            elif PC2_READY < 1:
                client.publish("g1_control_pc2", "SYN")
                print('Send SYN PC2')
            else:
                timeOutState = False
                break
            time.sleep(1)
        if timeOutState:
            print('Thread ended with TIMEOUT')
            client.publish("g1_control_status", "TIMEOUT")  # 🔔 sinal de timeout
        else:
            print('Thread ended with OK')
            client.publish("g1_control_status", "OK")  # 🔔 sinal de successo
    except Exception as e:
        print("Erro na thread:", e)

# metodos MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("g1_control_pc1")
    client.subscribe("g1_control_pc2")
    client.subscribe("g1_control_status")
    threading.Thread(target=controlState, args=(client,)).start()


def on_message(client, userdata, msg):
    global PC1_READY, PC2_READY
    print(msg.topic + " " + str(msg.payload))
    if (msg.topic == "g1_control_pc1" and msg.payload.decode() == "ACK"):
        print('ACK received')
        PC1_READY += 1
    if (msg.topic == "g1_control_pc2" and msg.payload.decode() == "ACK"):
        print('ACK received')
        PC2_READY += 1
    if msg.topic == "g1_control_status":
        status = msg.payload.decode()
        print("Estado da thread de controlo:", msg.payload.decode())
        if status == "TIMEOUT":
            print('TIMEOUT: scripts ainda não foram iniciados')
            sys.exit()
        if status == "OK":
            # createMysqlGame()
            script_dir = Path(__file__).parent.resolve()
            exe_path = script_dir.parent / "game" / "mazerun.exe"
            subprocess.Popen(
                f'start "Mazerun" "{exe_path}" {current_player}',
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
    if (msg.topic == "g1_control_pc1" and msg.payload.decode() == "START"):
        print('GAME IS READY TO PLAY...')
        while True:
            play_game(client)
            time.sleep(2)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect(broker_host, broker_port, 60)
mqttc.loop_forever()
