# ==============================
# Importações de bibliotecas
# ==============================

import paho.mqtt.client as mqtt              # Biblioteca MQTT para receber mensagens dos tópicos
import mysql.connector                       # Biblioteca para conectar ao MySQL
import json                                  # Para decodificar payloads JSON recebidos via MQTT
from datetime import datetime                # Para validações e formatação de datas

# ==============================
# Configurações do sistema
# ==============================

# Configurações do broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPICS = [("pisid_g1_movimento_1", 0), ("pisid_g1_ruido_1", 0)]  # Subscrição aos tópicos

# Configurações da base de dados MySQL
MYSQL_HOST = "localhost"
MYSQL_DATABASE = "marsami_game"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""

# ==============================
# Funções de callbacks do MQTT
# ==============================

def on_connect(client, userdata, flags, reason_code, properties):
    """
    Callback chamada ao conectar ao broker MQTT. Subcreve aos tópicos definidos.
    """
    print(f"Connected to MQTT broker with result code {reason_code}")
    client.subscribe(MQTT_TOPICS)

def on_message(client, userdata, msg):
    """
    Callback chamada ao receber uma mensagem de um dos tópicos MQTT.
    Encaminha a mensagem para a função de armazenamento no MySQL.
    """
    print(f"MQTT message received: {msg.topic} -> {msg.payload.decode()}")
    store_to_mysql(userdata['connection'], msg.topic, msg.payload.decode())

# ==============================
# Conexão à base de dados
# ==============================

def connect_mysql():
    """
    Cria e retorna uma conexão com a base de dados MySQL.
    """
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

# ==============================
# Validação dos dados recebidos
# ==============================

def validate_data(data, tipo, game_start_date, previous_value=None):
    """
    Valida dados recebidos de mensagens MQTT antes de serem inseridos no MySQL.

    :param data: Dicionário com os dados da mensagem
    :param tipo: Tipo da mensagem: 'movement' ou 'sound'
    :param game_start_date: Data de início do jogo
    :param previous_value: Valor anterior (apenas usado para verificar outliers de ruído)
    :return: (bool, str) -> (válido?, mensagem de erro)
    """
    try:
        # Validação do campo Player (comum)
        if "Player" not in data or int(data["Player"]) <= 0:
            return False, "Invalid or missing Player ID"

        # Validação de campos específicos para movimento
        if tipo == "movement":
            if "Marsami" not in data or int(data["Marsami"]) <= 0:
                return False, "Invalid or missing Marsami number"
            if "RoomOrigin" not in data or int(data["RoomOrigin"]) < 0:
                return False, "Invalid or missing RoomOrigin"
            if "RoomDestiny" not in data or int(data["RoomDestiny"]) < 0:
                return False, "Invalid or missing RoomDestiny"
            if "Status" not in data:
                return False, "Missing Status field"

        # Validação de campos específicos para ruído
        elif tipo == "sound":
            if "Sound" not in data or float(data["Sound"]) < 0:
                return False, "Invalid or missing Sound value"
            if "Hour" not in data:
                return False, "Missing timestamp (Hour)"

            # Verifica se a data é válida e coerente
            try:
                msg_time = datetime.fromisoformat(data["Hour"])
            except ValueError:
                return False, "Timestamp is not a valid ISO date"

            if msg_time > datetime.now():
                return False, "Timestamp is in the future"
            if msg_time < game_start_date:
                return False, "Timestamp is before the game start"

            # Verifica se o valor do som é um outlier
            normal_noise = float(data.get("NormalNoise", 0))
            tolerance = float(data.get("Tolerance", 0))
            threshold = (normal_noise + tolerance) * 1.75
            current_sound = float(data["Sound"])

            if current_sound > threshold or current_sound <= normal_noise:
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

def store_to_mysql(connection, topic, payload):
    """
    Encaminha a mensagem para a função de armazenamento correta com base no tópico.
    """
    try:
        if topic == "pisid_g1_movimento_1":
            store_movement(connection, payload)
        elif topic == "pisid_g1_ruido_1":
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
        data = json.loads(payload)
        PlayerID = data["Player"]

        cursor = connection.cursor(dictionary=True)
        game = get_active_game(cursor, PlayerID)

        if not game:
            print(f"[ERROR] No active game found for PlayerID {PlayerID}")
            return

        game_start_date = game['StartDate'] if 'StartDate' in game else datetime.now()

        valid, msg = validate_data(data, "movement", game_start_date)
        if not valid:
            print(f"[INVALID MOVEMENT] {msg}")
            return

        # Inserção na tabela message
        cursor.execute("INSERT INTO message (Type, GameID) VALUES ('Move', %s)", (game['GameID'],))
        message_id = cursor.lastrowid
        connection.commit()

        marsami_id = 1

        # Inserção na tabela movement
        cursor.execute("""
            INSERT INTO movement (MessageID, MarsamiID, OriginRoom, DestinationRoom, Status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            message_id,
            marsami_id,
            data["RoomOrigin"],
            data["RoomDestiny"],
            data["Status"]
        ))
        connection.commit()

    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON payload: {e}")
    except mysql.connector.Error as err:
        print(f"[ERROR] MySQL movement insert failed: {err}")
    finally:
        cursor.close()

def store_sound(connection, payload):
    """
    Processa e armazena dados de som no MySQL após validação.
    """
    try:
        data = json.loads(payload)
        PlayerID = data["Player"]
        Sound = data["Sound"]
        TimeStamp = data["Hour"]

        cursor = connection.cursor(dictionary=True)
        game = get_active_game(cursor, PlayerID)

        if not game:
            print(f"[ERROR] No active game found for PlayerID {PlayerID}")
            return

        game_start_date = game['StartDate'] if 'StartDate' in game else datetime.now()

        valid, msg = validate_data(data, "sound", game_start_date)
        if not valid:
            print(f"[INVALID SOUND] {msg}")
            return

        # Inserção na tabela message
        cursor.execute("""
            INSERT INTO message (Type, GameID, RegisteredDate) 
            VALUES ('Sound', %s, %s)
        """, (game['GameID'], TimeStamp))
        message_id = cursor.lastrowid
        connection.commit()

        # Inserção na tabela sound
        cursor.execute("INSERT INTO sound (MessageID, Sound) VALUES (%s, %s)", (message_id, Sound))
        connection.commit()

    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON payload: {e}")
    except mysql.connector.Error as err:
        print(f"[ERROR] MySQL sound insert failed: {err}")
    finally:
        cursor.close()

def get_active_game(cursor, PlayerID):
    """
    Retorna o jogo ativo (GameOver = 1) de um jogador.
    """
    cursor.execute("SELECT * FROM game WHERE PlayerID = %s AND GameOver = 1", (PlayerID,))
    return cursor.fetchone()

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

# Conecta ao broker e inicia o loop para escutar mensagens
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()