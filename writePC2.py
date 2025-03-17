import paho.mqtt.client as mqtt
import mysql.connector

# Configurações do MQTT
MQTT_BROKER = "broker.mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_TOPICS = [("pisid_g1_movimento_1", 0), ("pisid_g1_ruido_1", 0)]

# Configurações do MySQL
MYSQL_HOST = "seu_host_mysql"
MYSQL_USER = "seu_usuario_mysql"
MYSQL_PASSWORD = "sua_senha_mysql"
MYSQL_DATABASE = "seu_banco_de_dados_mysql"

# Função de callback quando a conexão ao MQTT for estabelecida
def on_connect(client, userdata, flags, rc):
    print("Conectado ao MQTT Broker com código de resultado: " + str(rc))
    client.subscribe(MQTT_TOPICS)

# Função de callback quando uma mensagem for recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida: {msg.topic} -> {msg.payload.decode()}")
    save_to_mysql(msg.topic, msg.payload.decode())

# Função para salvar os dados no MySQL
def save_to_mysql(topic, payload):
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = connection.cursor()

        if topic == "pisid_g1_movimento_1":
            query = "INSERT INTO movimento (coluna1, coluna2) VALUES (%s, %s)"
            data = (valor1, valor2)  # Substitua pelos valores reais extraídos do payload
        elif topic == "pisid_g1_ruido_1":
            query = "INSERT INTO ruido (coluna1, coluna2) VALUES (%s, %s)"
            data = (valor1, valor2)  # Substitua pelos valores reais extraídos do payload

        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()