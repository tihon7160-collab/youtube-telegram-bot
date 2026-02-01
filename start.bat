@echo off
echo ========================================
echo YouTube Telegram Bot
echo ========================================
echo.

REM Проверка наличия .env файла
if not exist .env (
    echo [ERROR] Файл .env не найден!
    echo.
    echo Пожалуйста, скопируйте .env.example в .env и настройте его:
    echo   copy .env.example .env
    echo.
    pause
    exit /b 1
)

REM Проверка наличия виртуального окружения
if not exist venv (
    echo [INFO] Создание виртуального окружения...
    python -m venv venv
    echo.
)

REM Активация виртуального окружения
echo [INFO] Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Установка зависимостей
echo [INFO] Установка зависимостей...
pip install -r requirements.txt
echo.

REM Запуск бота
echo [INFO] Запуск бота...
echo.
python bot\main.py

pause
