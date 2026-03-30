@echo off
echo ==============================================================
echo CERRANDO CHROME PARA REABRIRLO EN MODO CONTROL REMOTO DEL BOT
echo ==============================================================
echo Cerrando instancias previas de Chrome...
taskkill /F /IM chrome.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo Abriendo Chrome con el puerto 9222...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins="*"
