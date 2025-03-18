import paho.mqtt.client as mqtt
import mysql.connector
import json

# Configurações do MQTT
MQTT_BROKER = "broker.mqtt-dashboard.com"
MQTT_PORT = 1883
#MQTT_TOPICS = [("pisid_g1_movimento_1", 0), ("pisid_g1_ruido_1", 0)]
MQTT_TOPICS = "pisid_g1_movimento_1"

# Configurações do MySQL
MYSQL_HOST = "localhost"
MYSQL_DATABASE = "marsami_game"
MYSQL_USER = "root"  # Default MySQL user
MYSQL_PASSWORD = ""  # Empty password

# Função de callback quando a conexão ao MQTT for estabelecida
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe(MQTT_TOPICS)
    client.subscribe("pisid_g1_ruido_1")

# Função de callback quando uma mensagem for recebida
def on_message(client, userdata, msg):
    print(f"New Message received: {msg.topic} -> {msg.payload.decode()}")
    store_mySQL(userdata['connection'], msg.topic, msg.payload.decode())

# Função para conectar à BD local do MySQL (PC2)
def connect_mySQL():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        # When a user starts the game a new row is inserted into the game table (mock)
        #cursor.execute("INSERT INTO game (PlayerID, GameOver, ConfigID, UserID) VALUES ('1', '1', '1', '1')")
        #connection.commit()

        # Test connection (PASSING)
        '''
        print(f"Connection to SQL established with cursor: {cursor}")
        cursor.execute("SELECT * FROM game WHERE PlayerID = 1 AND GameOver = 1")
        game = cursor.fetchone()
        print(f"Game found: {game}")

        # Test insert (PASSING)
        cursor.execute("INSERT INTO message (Type, GameID) VALUES ('Move', '1')")
        message_id = cursor.lastrowid # Gets the ID of the last inserted message
        connection.commit()
        '''
    
        return connection
    except mysql.connector.Error as err:
        print(f"Error while connecting to SQL: {err}")

# Função para armazenar os dados recebidos do MQTT na BD local do MySQL (PC2)
def store_mySQL(connection, topic, payload):
    try:
        if topic == "":
            store_movement(connection, payload)
        elif topic == "pisid_g1_ruido_1":
            store_sound(connection, payload)
        else:
            print(f"Unknown topic: {topic}")

    except mysql.connector.Error as err:
        print(f"Error while storing data: {err}")

def store_movement(connection, payload):
    try: 
        # Parse the payload to extract the data
        data = json.loads(payload)
        PlayerID = data["Player"]
        Marsami = data["Marsami"]
        RoomOrigin = data["RoomOrigin"]
        RoomDestiny = data["RoomDestiny"]
        Status = data["Status"]

        cursor = connection.cursor(dictionary=True) # Returns the results as a dictionary (No need to use tuples)

        # Validate which game is active
        game = get_active_game(cursor, PlayerID)

        if game:
            # Store the message in the database
            cursor.execute("INSERT INTO message (Type, GameID) VALUES ('Move', %s)", (game['GameID'],))
            message_id = cursor.lastrowid # Gets the ID of the last inserted message
            connection.commit()

            # TODO: O marsami ID deve ser obtido da tabela Marsami, onde o GameID é igual ao GameID do jogo ativo e o MarsamiNumber é igual ao Marsami do movimento
            marsami_id = 1

            cursor.execute("INSERT INTO movement (MessageID, MarsamiID, OriginRoom, DestinationRoom, Status) VALUES (%s, %s, %s, %s, %s)", (message_id, marsami_id, RoomOrigin, RoomDestiny, Status))
            connection.commit()
        else:
            print(f"No active game found for PlayerID {PlayerID}")

    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON payload: {json_err}")
    except mysql.connector.Error as err:
        print(f"Error while storing movement data: {err}")
    finally:
        cursor.close()

def store_sound(connection, payload):
    try:
        data = json.loads(payload)
        PlayerID = data["Player"]
        Sound = data["Sound"]
        TimeStamp = data["Hour"]

        cursor = connection.cursor(dictionary=True)
        game = get_active_game(cursor, PlayerID)

        if game:
            # Store the message in the database
            cursor.execute("INSERT INTO message (Type, GameID, RegisteredDate) VALUES ('Sound', %s, %s)", (game['GameID'], TimeStamp))
            message_id = cursor.lastrowid # Gets the ID of the last inserted message
            connection.commit()

            cursor.execute("INSERT INTO sound (MessageID, Sound) VALUES (%s, %s, %s, %s, %s)", (message_id, Sound,))
            connection.commit()
        else:
            print(f"No active game found for PlayerID {PlayerID}")

    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON payload: {json_err}")
    except mysql.connector.Error as err:
        print(f"Error while storing movement data: {err}")
    finally:
        cursor.close()


def get_active_game(cursor, PlayerID):
    cursor.execute("SELECT * FROM game WHERE PlayerID = %s AND GameOver = 1", (PlayerID,))
    game = cursor.fetchone() # Fetch the first row (in this case we only expect a single row to match the query as each player will have only 1 game active at a time)
    return game

def deal_marsami():
    pass

# Configuração do cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Ligação ao MySQL e armazenamento da conexão e do cursor na userdata do cliente MQTT
connection = connect_mySQL()
client.user_data_set({'connection': connection})

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()