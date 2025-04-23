@echo off
setlocal EnableDelayedExpansion

chcp 1252 >nul

echo Encerrando instâncias anteriores do MongoDB...
powershell -Command "Get-Process mongod -ErrorAction SilentlyContinue | Stop-Process -Force"

echo A preparar pastas de dados e de logs...

if not exist C:\mongodb\data\r1 mkdir C:\mongodb\data\r1
if not exist C:\mongodb\data\r2 mkdir C:\mongodb\data\r2
if not exist C:\mongodb\data\r3 mkdir C:\mongodb\data\r3
if not exist C:\mongodb\log mkdir C:\mongodb\log

echo A iniciar os nós do MongoDB...

start "MongoDB Node 1" mongod --replSet rs0 --port 27017 --dbpath C:\mongodb\data\r1 --bind_ip localhost --logpath C:\mongodb\log\r1.log --logappend
timeout /t 2 >nul
start "MongoDB Node 2" mongod --replSet rs0 --port 27018 --dbpath C:\mongodb\data\r2 --bind_ip localhost --logpath C:\mongodb\log\r2.log --logappend
timeout /t 2 >nul
start "MongoDB Node 3" mongod --replSet rs0 --port 27019 --dbpath C:\mongodb\data\r3 --bind_ip localhost --logpath C:\mongodb\log\r3.log --logappend

echo.
echo A aguardar que o nó primário (27017) fique disponível...
set /a waitSeconds=0
:waitForMongo
set /a waitSeconds+=3
echo A aguardar... !waitSeconds! segundos
ping 127.0.0.1 -n 3 >nul
mongosh --port 27017 --quiet --eval "db.runCommand({ ping: 1 })" >nul 2>&1
if errorlevel 1 goto waitForMongo

echo.
echo Verificando o estado do Replica Set...

for /f "usebackq delims=" %%i in (`mongosh --port 27017 --quiet --eval "try { rs.status().ok } catch (e) { 0 }"`) do set STATUS=%%i

if "%STATUS%"=="0" (
    echo Replica Set ainda não iniciado. A iniciar...
    mongosh --port 27017 --eval "rs.initiate({_id: 'rs0', members: [{_id: 0, host: 'localhost:27017'}, {_id: 1, host: 'localhost:27018'}, {_id: 2, host: 'localhost:27019'}]})"
) else (
    echo Replica Set já se encontra iniciado.
)

echo.
echo A aguardar que todos os nós fiquem prontos...
set /a readySeconds=0
:waitReady
set /a readySeconds+=4
echo A aguardar... !readySeconds! segundos
ping 127.0.0.1 -n 4 >nul

for /f "usebackq delims=" %%i in (`mongosh --port 27017 --quiet --eval "try { rs.status().members.filter(m => m.stateStr == 'PRIMARY' || m.stateStr == 'SECONDARY').length } catch(e) { 0 }"`) do set MEMBERS_READY=%%i

if not "%MEMBERS_READY%"=="3" goto waitReady

echo.
echo Todos os nós estão operacionais. Configuração concluída com êxito!

:: Mostrar janela popup com mensagem final
powershell -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; [System.Windows.Forms.MessageBox]::Show('Todos os nós estão operacionais. Configuração concluída com êxito!', 'MongoDB Réplica Set', 'OK', 'Information')"

endlocal
