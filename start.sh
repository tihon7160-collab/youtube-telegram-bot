#!/bin/bash

echo "========================================"
echo "YouTube Telegram Bot"
echo "========================================"
echo ""

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "[ERROR] Файл .env не найден!"
    echo ""
    echo "Пожалуйста, скопируйте .env.example в .env и настройте его:"
    echo "  cp .env.example .env"
    echo ""
    exit 1
fi

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "[INFO] Создание виртуального окружения..."
    python3 -m venv venv
    echo ""
fi

# Активация виртуального окружения
echo "[INFO] Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "[INFO] Установка зависимостей..."
pip install -r requirements.txt
echo ""

# Запуск бота
echo "[INFO] Запуск бота..."
echo ""
python bot/main.py
