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
from mqtt_to_mysql_writer import startScript

db_host = os.getenv("DB_HOST", "localhost") # DB host (default: localhost)
db_user = os.getenv("DB_USER", "root") # MySQL user (default: root)
db_password = os.getenv("DB_PASSWORD", "") # MySQL password (default: empty)
sql_db = os.getenv("SQL_DB", "marsami_game") # MySQL database (default: marsami_game)
broker_host = os.getenv("BROKER_HOST", "broker.emqx.io")
broker_port = int(os.getenv("BROKER_PORT", 1883))
current_player = os.getenv("CURRENT_PLAYER", 1) # Currently active player (default: 1)
timeout = int(os.getenv("START_GAME_TIMEOUT", 60))

# guardar argumentos recebidos
if len(sys.argv) != 4:
    print("Usage: python start_game.py user name description")
    sys.exit(1)

gameUser = sys.argv[1]
gameName = sys.argv[2]
gameDescription = sys.argv[3]

threading.Thread(target=startScript, args=(gameUser,)).start()

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

    # Chamar stored procedure com parâmetros
    cursor.callproc("criar_jogo", [
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
    room = random.randint(1, 10)
    message = {"Type": "Score", "Player": current_player, "Room": room}
    print(str(message))
    client.publish("pisid_mazeact", str(message))

def single_door_act(type, client):
    origin = random.randint(1, 10)
    destiny = origin
    while destiny == origin:
        destiny = random.randint(1, 10)
    message = {"Type": type, "Player": current_player, "RoomOrigin": origin, "RoomDestiny": destiny}
    print(str(message))
    client.publish("pisid_mazeact", str(message))

def all_door_act(type, client):
    message = {"Type": type, "Player": current_player}
    print(str(message))
    client.publish("pisid_mazeact", str(message))

def play_game(client, evento_parar):
    while not evento_parar.is_set():
        action = random.randint(1, 5)
        match action:
            case GameActions.SCORE:
                score(client)
            case GameActions.OPEN_DOOR:
                single_door_act("OpenDoor", client)
            case GameActions.CLOSE_DOOR:
                single_door_act("CloseDoor", client)
            case GameActions.OPEN_ALL_DOOR:
                all_door_act("OpenAllDoor", client)
            case GameActions.CLOSE_ALL_DOOR:
                all_door_act("CloseAllDoor", client)
        timer = random.randint(1, 5)
        time.sleep(timer)


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
    client.subscribe("pisid_mazeact")
    threading.Thread(target=controlState, args=(client,)).start()

evento_parar = threading.Event()
def on_message(client, userdata, msg):
    global PC1_READY, PC2_READY, evento_parar
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
            createMysqlGame()
            script_dir = Path(__file__).parent.resolve()
            exe_path = script_dir.parent / "game" / "mazerun.exe"
            print(exe_path)
            subprocess.Popen(
                f'start "Mazerun" "{exe_path}" {current_player}',
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
        if status == "GAME_OVER":
            evento_parar.set()
            time.sleep(2)
            os._exit(0)
    if (msg.topic == "g1_control_pc1" and msg.payload.decode() == "START"):
        print('GAME IS READY TO PLAY...')
        threading.Thread(target=play_game, args=(client, evento_parar,)).start()
    if(msg.topic == "pisid_mazeact"):
        print("\033[92mPLAYING MAZEACT... ", str(msg.payload.decode()), "\033[00m")



mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect(broker_host, broker_port, 60)
mqttc.loop_forever()
