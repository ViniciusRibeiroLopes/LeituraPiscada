@echo off
title LeituraPisca
echo ==============================================
echo Iniciando o programa LeituraPisca...
echo Por favor aguarde a webcam ligar.
echo ==============================================
cd /d "%~dp0"
call .venv10\Scripts\python main.py
pause
