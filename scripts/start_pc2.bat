@echo off
REM Argumentos: utilizador, nome do jogo, descrição
set DBUSER=%1
set GAMENAME=%2
set GAMEDESC=%3

REM Mover para a pasta certa
cd /d C:\xampp\htdocs\mazerun

REM (Opcional) Ativar ambiente virtual, se usares
REM call venv\Scripts\activate.bat

REM Instalar dependências só se necessário
pip install -r requirements.txt

REM Executar o script Python com os argumentos
python src\start_game.py %DBUSER% %GAMENAME% %GAMEDESC%

REM (Opcional) Pausar para debug
REM pause
