@echo off
chcp 65001 > nul
echo ===================================================
echo     ITCompass — Запуск Python Backend (Flask)
echo ===================================================
echo.

cd /d "%~dp0backend"

echo [1/3] Перевірка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ПОМИЛКА] Python не знайдено в системній змінній PATH!
    echo Будь ласка, встановіть Python з https://www.python.org/ та поставте галочку "Add Python to PATH".
    pause
    exit /b
)

echo [2/3] Встановлення залежностей (Flask, Flask-Cors)...
pip install -r requirements.txt

echo.
echo [3/3] Запуск сервера ITCompass на порту 5000...
echo.
echo ---------------------------------------------------
echo  * Головний сайт:         http://127.0.0.1:5000/
echo  * Каталог професій:      http://127.0.0.1:5000/professions.html
echo  * Панель адміністратора: http://127.0.0.1:5000/admin
echo  * REST API професій:     http://127.0.0.1:5000/api/professions
echo ---------------------------------------------------
echo Для зупинки сервера натисніть Ctrl + C у цьому вікні.
echo.

start http://127.0.0.1:5000/admin
start http://127.0.0.1:5000/
python app.py

pause
