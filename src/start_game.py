
import mysql.connector
import sys
import os

db_host = os.getenv("DB_HOST", "localhost") # DB host (default: localhost)
db_user = os.getenv("DB_USER", "root") # MySQL user (default: root)
db_password = os.getenv("DB_PASSWORD", "") # MySQL password (default: empty)
sql_db = os.getenv("SQL_DB", "marsami_game") # MySQL database (default: marsami_game)


# guardar argumentos recebidos
if len(sys.argv) != 4:
    print("Usage: python start_game.py user name description")
    sys.exit(1)


gameUser = sys.argv[1]
gameName = sys.argv[2]
gameDescription = sys.argv[3]

print("Arg1:", gameName)
print("Arg2:", gameDescription)

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

conn1 = connect_mysql_cloud()
cursor = conn1.cursor(dictionary=True)
cursor.execute("SELECT * FROM setupmaze")
settings = cursor.fetchone()

print(settings)

# settings["numberrooms"]

# Criar novo jogo na bd marsamis
#BaseSound: normalnoise, SoundVarTolerance: noisevartoleration, TotalMarsamis: numbermarsamis

conn2 = connect_mysql_pc2()
cursor = conn2.cursor(dictionary=True)

game_name = "Jogo Exemplo"
game_description = "Descrição do jogo"

# Chamar stored procedure com parâmetros
cursor.callproc("createGame", [
    int(gameUser),
    gameName,
    gameDescription,
    settings["numbermarsamis"],
    settings["noisevartoleration"],
    settings["normalnoise"]
])


# correr o jogo
