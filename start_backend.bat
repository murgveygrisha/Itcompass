@echo off
chcp 65001 > nul
echo ===================================================
echo     ITCompass — Запуск Python Backend (FastAPI)
echo ===================================================
echo.

cd /d "%~dp0backend"

echo [1/3] Перевірка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ПОМИЛКА] Python не знайдено в системній змінній PATH!
    echo Будь ласка, встановіть Python з https://www.python.org/ та оберіть галочку "Add Python to PATH".
    pause
    exit /b
)

echo [2/3] Встановлення залежностей (FastAPI, Uvicorn, Pydantic)...
pip install -r requirements.txt

echo.
echo [3/3] Запуск сервера ITCompass на порту 8000...
echo.
echo ---------------------------------------------------
echo  * Головний сайт:         http://127.0.0.1:8000/
echo  * Каталог професій:      http://127.0.0.1:8000/professions.html
echo  * Swagger API документація: http://127.0.0.1:8000/docs
echo  * Redoc документація:    http://127.0.0.1:8000/redoc
echo ---------------------------------------------------
echo Для зупинки сервера натисніть Ctrl + C.
echo.

start http://127.0.0.1:8000/docs
python app.py

pause
