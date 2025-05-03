import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
current_player = os.getenv("CURRENT_PLAYER", 1) # current player

print('starting replicas...')
# subprocess.run('startReplicaSet.bat')

print('starting Script1: mqtt_to_mongo_ingest.py')
mqtt_proc = subprocess.Popen(
    f'start "MQTT To Mongo - Ingest" python ../src/mqtt_to_mongo_ingest.py',
    shell=True,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)

print('starting Script2: mongo_to_mqtt_publisher.py')
mongo_proc = subprocess.Popen(
    f'start "Mongo To MQTT - Publisher" python ../src/mongo_to_mqtt_publisher.py',
    shell=True,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)

# print('starting Script2: mongo_to_mqtt_publisher.py')
# mongo_proc = subprocess.Popen(
#     f'start "MQTT To MYSQL - Writer" python ../src/mqtt_to_mysql_writer.py',
#     shell=True,
#     creationflags=subprocess.CREATE_NEW_CONSOLE,
# )

# print('starting Game mazerun...')
# mazerun_proc = subprocess.Popen(
#     f'start "Mazerun" ../game/mazerun.exe {current_player}',
#     shell=True,
#     creationflags=subprocess.CREATE_NEW_CONSOLE,
# )


