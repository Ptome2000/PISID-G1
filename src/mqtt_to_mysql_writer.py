# ==============================
# Importações de bibliotecas
# ==============================

import os
import threading

from dotenv import load_dotenv
import paho.mqtt.client as mqtt              # Biblioteca MQTT para receber mensagens dos tópicos
import mysql.connector                       # Biblioteca para conectar ao MySQL
import json                                  # Para decodificar payloads JSON recebidos via MQTT
from datetime import datetime                # Para validações e formatação de
import sys


# guardar argumentos recebidos
# if len(sys.argv) != 2:
#     print("Usage: python mqtt_to_mysql_writer.py username")
#     sys.exit(1)

# USER_NAME = sys.argv[1]
USER_NAME = ""

from utils.Enums import AlertType

# ==============================
# Configurações do sistema
# ==============================

load_dotenv() 
current_player = os.getenv("CURRENT_PLAYER", 1) # Currently active player (default: 1)
broker_host = os.getenv("BROKER_HOST", "broker.emqx.io") # MQTT broker host (default: broker.emqx.io)
broker_port = int(os.getenv("BROKER_PORT", 1883)) # MQTT broker port (default: 1883)
db_host = os.getenv("DB_HOST", "localhost") # DB host (default: localhost)
db_user = os.getenv("DB_USER", "root") # MySQL user (default: root)
db_password = os.getenv("DB_PASSWORD", "") # MySQL password (default: empty)
sql_db = os.getenv("SQL_DB", "marsami_game") # MySQL database (default: marsami_game)

# ==============================
# Funções de callbacks do MQTT
# ==============================

def on_connect(client, userdata, flags, reason_code, properties):
    """
    Callback chamada ao conectar ao broker MQTT. Subcreve aos tópicos definidos.
    """
    print(f"Connected to MQTT broker with result code {reason_code}")
    client.subscribe(f"pisid_g1_movimento_{current_player}")
    client.subscribe(f"pisid_g1_ruido_{current_player}")
    client.subscribe("g1_control_pc2")
    client.subscribe("g1_control_status")


ACK_SENT = False
def on_message(client, userdata, msg):
    global ACK_SENT
    """
    Callback chamada ao receber uma mensagem de um dos tópicos MQTT.
    Encaminha a mensagem para a função de armazenamento no MySQL.
    """
    print(f"{msg.topic} {msg.payload}")
    # threading.Thread(target=store_to_mysql, args=(
    #     userdata['connection'],
    #     msg.topic,
    #     msg.payload.decode(),
    # )).start()
    store_to_mysql(userdata['connection'], msg.topic, msg.payload.decode())
    if msg.topic == "g1_control_pc2" and msg.payload.decode() == "SYN":
        if not ACK_SENT:
            client.publish("g1_control_pc2", "ACK")
            print('ACK SENT')
            ACK_SENT = True

# ==============================
# Conexão à base de dados
# ==============================

def connect_mysql():
    """
    Cria e retorna uma conexão com a base de dados MySQL.
    """
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

# ==============================
# Validação dos dados recebidos
# ==============================

def deal_alerts(data, game, connection):
    """
    Valida e gera alertas com base nos cenários descritos.

    :param data: Dicionário com os dados da mensagem de som.
    :param game: Dicionário com informações do jogo ativo.
    :param cursor: Cursor da conexão MySQL.
    """
    cursor = connection.cursor(dictionary=True)

    try:
        hour = data["Hour"]
        game_start_date = game['StartDate'] if 'StartDate' in game else datetime.now()
        current_sound = float(data["Sound"])
        normal_noise = float(game.get("BaseSound", 0))
        tolerance = float(game.get("SoundVarTolerance", 0))
        max_limit = float(normal_noise + tolerance)
        threshold_90 = float(normal_noise + tolerance * 0.9)
        print(threshold_90)
        threshold_10 = float(normal_noise + tolerance * 0.1)

        # Cenário 1: Alerta caso o limite máximo tenha sido ultrapassado
        if current_sound > max_limit:
            print("\033[93m[GAME OVER] Maximum sound limit exceeded! The maze doors are closed, and the game is lost.\033[00m")
            alert = AlertType.SOUND_EXCEEDS_MAX_LIMIT
            cursor.callproc("post_alert", (hour, None, game['IDJogo'], 1, current_sound, alert.code, alert.message))
            client.publish("g1_control_status", "GAME_OVER")

        # Cenário 2: Alertar 1x se o nível de som exceder 90% do limite máximo
        elif current_sound > threshold_90:
            print("\033[93m[ALERT] Sound level exceeded 90% of the maximum limit!\033[00m")
            alert = AlertType.SOUND_EXCEEDS_90_PERCENT
            cursor.callproc("post_alert", (hour, None, game['IDJogo'], 1, current_sound, alert.code, alert.message))

        # Cenário 3: Alertar 1x se o nível de som estiver abaixo de 10% do ruído normal
        elif current_sound <= threshold_10:
            print("\033[93m[ALERT] Sound level under 90% of the maximum limit! You're marsamis are safe.\033[00m")
            alert = AlertType.SOUND_BELOW_90_PERCENT
            cursor.callproc("post_alert", (hour, None, game['IDJogo'], 1, current_sound, alert.code, alert.message))

        # Cenário 4: Após 30s do início do jogo, alertar se o som estiver demasiado perto do ruído normal
        elif (datetime.now() - game_start_date).total_seconds() > 30 and current_sound <= threshold_10:
            print("\033[93m[ALERT] Sound level is too close to normal noise after 30 seconds!\033[00m")
            alert = AlertType.SOUND_TOO_CLOSE_TO_NORMAL
            cursor.callproc("post_alert", (hour, None, game['IDJogo'], 1, current_sound, alert.code, alert.message))


    except KeyError as e:
        print(f"[ERROR] Missing key in data: {e}")
    except ValueError as e:
        print(f"[ERROR] Invalid value in data: {e}")
    cursor.close()

def validate_data(data, tipo, game, previous_value=None):
    """
    Valida dados recebidos de mensagens MQTT antes de serem inseridos no MySQL.

    :param data: Dicionário com os dados da mensagem
    :param tipo: Tipo da mensagem: 'movement' ou 'sound'
    :param game: Dicionário com informações do jogo ativo
    :param previous_value: Valor anterior (apenas usado para verificar outliers de ruído)
    :return: (bool, str) -> (válido?, mensagem de erro)
    """
    try:
        # Validação do campo Player (comum)
        if "Player" not in data or int(data["Player"]) <= 0:
            return False, "Invalid or missing Player ID"

        # Validação de campos específicos para movimento
        if tipo == "movement":
            if "Marsami" not in data or int(data["Marsami"]) <= 0 or int(data["Marsami"]) > int(game["TotalMarsamis"]):
                return False, "Invalid or missing Marsami number"
            if "RoomOrigin" not in data or int(data["RoomOrigin"]) < 0:
                return False, "Invalid or missing RoomOrigin"
            if "RoomDestiny" not in data or int(data["RoomDestiny"]) < 0:
                return False, "Invalid or missing RoomDestiny"
            if "Status" not in data or int(data["Status"]) < 0 or int(data["Status"]) > 2:
                return False, "Invalid or missing Status field"

        # Validação de campos específicos para ruído
        elif tipo == "sound":
            if "Sound" not in data or float(data["Sound"]) < 0:
                return False, "Invalid or missing Sound value"
            if "Hour" not in data:
                return False, "Missing timestamp (Hour)"

            # Verifica se a data é válida e coerente
            game_start_date = game['StartDate'] if 'StartDate' in game else datetime.now()
            try:
                msg_time = datetime.fromisoformat(data["Hour"])
            except ValueError:
                return False, "Timestamp is not a valid ISO date"

            if msg_time > datetime.now():
                return False, "Timestamp is in the future"
            if msg_time < game_start_date:
                return False, "Timestamp is before the game start"

            # Verifica se o valor do som é um outlier
            normal_noise = float(game.get("BaseSound", 0))
            tolerance = float(game.get("SoundVarTolerance", 0))
            threshold = (normal_noise + tolerance) * 1.75
            current_sound = float(data["Sound"])

            if current_sound > threshold or current_sound < normal_noise:
                return False, "Sound value is outside acceptable limits"

            # Verifica se a variação para o valor anterior é excessiva
            if previous_value is not None:
                if abs(current_sound - previous_value) > previous_value * 0.75:
                    return False, "Sound variation is too abrupt (outlier detection)"

        return True, "Valid"
    except (KeyError, ValueError, TypeError) as e:
        return False, f"Validation error: {e}"

# ==============================
# Armazenamento no MySQL
# ==============================

def get_active_game(cursor):
    """
    Obtém o jogo ativo para um jogador específico.
    """

    cursor.callproc("get_active_game", (str(USER_NAME),))
    # result = cursor.fetchone()
    # print(result)
    result = None
    for r in cursor.stored_results():
        result = r.fetchone()
        print(result)

    if not result:
        print(f"[ERROR] No active game found for Player {USER_NAME}")
        return

    print(f"[DEBUG] Active game found for Player {USER_NAME}: {result['IDJogo']}")
    return result

def store_to_mysql(connection, topic, payload):
    """
    Encaminha a mensagem para a função de armazenamento correta com base no tópico.
    """

    # TODO: Vai ser ser também validado os alertas neste script

    try:
        if topic == f"pisid_g1_movimento_{current_player}":
            store_movement(connection, payload)
        elif topic == f"pisid_g1_ruido_{current_player}":
            store_sound(connection, payload)
        else:
            print(f"[WARNING] Unknown topic: {topic}")
    except mysql.connector.Error as err:
        print(f"Error while storing data to MySQL: {err}")

def store_movement(connection, payload):
    """
    Processa e armazena dados de movimento no MySQL após validação.
    """
    try:
        payload = payload.replace("'", '"')
        data = json.loads(payload)

        cursor = connection.cursor(dictionary=True)
        game = get_active_game(cursor)
        if not game:
            return

        valid, msg = validate_data(data, "movement", game)
        if not valid:
            print(f"[INVALID MOVEMENT] {msg}")
            return

        # Insert into the movement table
        cursor.execute("""
            INSERT INTO Movement (OriginRoom, DestinationRoom, Status, MarsamiNum, IDGame)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["RoomOrigin"],
            data["RoomDestiny"],
            int(data["Status"]),
            data["Marsami"],
            game["IDJogo"]
        ))
        connection.commit()

        print(f"[MOVEMENT] Data stored successfully for Player {USER_NAME}")

    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON payload: {e}")
    except mysql.connector.Error as err:
        print(f"[ERROR] MySQL movement insert failed: {err}")
    finally:
        if cursor:
            cursor.close()

def store_sound(connection, payload):
    """
    Processa e armazena dados de som no MySQL após validação.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        data = json.loads(payload)
        game = get_active_game(cursor)
        if not game:
            return

        valid, msg = validate_data(data, "sound", game)
        if not valid:
            print(f"[INVALID SOUND] {msg}")
            return

        deal_alerts(data, game, connection)

        # Inserção na tabela sound
        cursor.execute("""
            INSERT INTO Sound (Sound, Hour, IDGame)
            VALUES (%s, %s, %s)
        """, (
            data["Sound"],
            data["Hour"],
            game["IDJogo"]
        ))
        connection.commit()

        print(f"[SOUND] Data stored successfully for Player {USER_NAME}")

    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON payload: {e}")
    except mysql.connector.Error as err:
        print(f"[ERROR] MySQL sound insert failed: {err}")
    finally:
        if cursor:
            cursor.close()

# ==============================
# Inicialização do cliente MQTT
# ==============================

# Criação do cliente MQTT com API v2
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Associação das funções de callback
client.on_connect = on_connect
client.on_message = on_message

# Cria conexão MySQL e passa como user_data para o cliente MQTT
connection = connect_mysql()
client.user_data_set({'connection': connection})

def startScript(username):
    global client, USER_NAME
    # Conecta ao broker e inicia o loop para escutar mensagens
    USER_NAME = username
    client.connect(broker_host, broker_port, 60)
    client.loop_forever()

# startScript("ptome")