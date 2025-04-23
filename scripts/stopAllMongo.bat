@echo off
chcp 1252 >nul
echo A encerrar todas as instâncias do MongoDB...

:: Usar PowerShell para terminar todos os mongod.exe
powershell -Command "Get-Process mongod -ErrorAction SilentlyContinue | Stop-Process -Force"

echo Todos os processos mongod foram encerrados (caso existissem).
powershell -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; [System.Windows.Forms.MessageBox]::Show('Todos os processos mongod foram encerrados (caso existissem).', 'MongoDB Réplica Set', 'OK', 'Information')"