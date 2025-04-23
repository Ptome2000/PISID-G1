@echo off
:: Autoelevar a execu��o se n�o estiver como administrador
:: Este bloco relan�a o script com permiss�es elevadas via PowerShell

fsutil dirty query %systemdrive% >nul 2>&1
if errorlevel 1 (
    echo A relancar como Administrador...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

chcp 1252 >nul
echo A encerrar todas as inst�ncias do MongoDB...

:: Usar PowerShell para terminar todos os mongod.exe
powershell -Command "Get-Process mongod -ErrorAction SilentlyContinue | Stop-Process -Force"

echo Todos os processos mongod foram encerrados (caso existissem).
powershell -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; [System.Windows.Forms.MessageBox]::Show('Todos os processos mongod foram encerrados (caso existissem).', 'MongoDB R�plica Set', 'OK', 'Information')"