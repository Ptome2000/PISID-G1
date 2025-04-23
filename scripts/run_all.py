import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
current_player = os.getenv("CURRENT_PLAYER", 1) # current player

game = subprocess.Popen(
    f'cd .. && .\\game\\mazerun.exe {current_player}',
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)
# Stream output live
for line in game.stdout:
    print(line, end='')

game.wait()
