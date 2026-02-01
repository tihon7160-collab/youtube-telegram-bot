# 🎬 YouTube Telegram Bot

Telegram бот с мини-приложением для просмотра YouTube видео без ограничений и VPN в России.

## ✨ Возможности

- 🔍 **Поиск видео** - ищите видео прямо в боте
- 📺 **Просмотр по ссылке** - отправьте ссылку на YouTube видео
- 🎮 **Встроенный плеер** - смотрите видео в мини-приложении Telegram
- ⬇️ **Скачивание видео** - сохраняйте видео на устройство
- 🌐 **Обход блокировок** - работает в России без VPN
- 🎨 **Telegram-дизайн** - адаптируется под тему Telegram

## 🏗️ Структура проекта

```
youtube-telegram-bot/
├── bot/                    # Backend бота
│   ├── main.py            # Основной файл запуска
│   ├── handlers.py        # Обработчики команд
│   ├── config.py          # Конфигурация
│   └── utils.py           # Вспомогательные функции
├── webapp/                # Frontend мини-приложения
│   ├── index.html         # Интерфейс
│   ├── styles.css         # Стили
│   └── script.js          # JavaScript логика
├── proxy_server.py        # Прокси-сервер (опционально)
├── requirements.txt       # Зависимости Python
├── .env.example          # Пример конфигурации
└── README.md             # Документация
```

## 📋 Требования

- Python 3.8+
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
- Web-сервер для размещения мини-приложения (GitHub Pages, Vercel, Netlify, или свой сервер)
- (Опционально) Прокси-сервер для обхода блокировок

## 🚀 Установка

### 1. Клонирование репозитория

```bash
cd youtube-telegram-bot
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка конфигурации

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
# Токен бота от @BotFather
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# URL мини-приложения (после деплоя webapp/)
WEBAPP_URL=https://your-username.github.io/youtube-bot/webapp

# Прокси (опционально)
PROXY_URL=socks5://127.0.0.1:1080

# Invidious инстанс
INVIDIOUS_INSTANCE=https://invidious.io

# Путь для скачиваний
DOWNLOAD_PATH=./downloads

# Максимальный размер файла (MB)
MAX_FILE_SIZE=50
```

### 4. Создание бота в Telegram

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Придумайте имя и username для бота
4. Скопируйте токен и вставьте в `.env`

### 5. Настройка мини-приложения

**Вариант A: GitHub Pages (бесплатно)**

1. Создайте репозиторий на GitHub
2. Загрузите папку `webapp/` в репозиторий
3. Включите GitHub Pages в настройках репозитория
4. URL будет вида: `https://username.github.io/repo-name/webapp`

**Вариант B: Vercel/Netlify (бесплатно)**

1. Зарегистрируйтесь на [Vercel](https://vercel.com) или [Netlify](https://netlify.com)
2. Подключите репозиторий или загрузите папку `webapp/`
3. Скопируйте полученный URL

**Вариант C: Свой сервер**

```bash
# Установите nginx
sudo apt install nginx

# Скопируйте файлы
sudo cp -r webapp/ /var/www/html/youtube-bot/

# Настройте nginx для HTTPS (обязательно!)
# Telegram требует HTTPS для мини-приложений
```

### 6. Настройка Web App в боте

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте `/mybots` → выберите бота → `Bot Settings` → `Menu Button`
3. Выберите `Configure menu button`
4. Введите URL вашего мини-приложения
5. Введите текст кнопки: "Открыть YouTube"

## 🔧 Запуск

### Запуск бота

```bash
cd bot
python main.py
```

### Запуск прокси-сервера (опционально)

Если у вас есть прокси и вы хотите использовать свой прокси-сервер:

```bash
python proxy_server.py
```

## 📱 Использование

### Команды бота

- `/start` - Главное меню
- `/search` - Поиск видео
- `/help` - Помощь

### Как пользоваться

1. **Поиск видео:**
   - Отправьте `/search`
   - Введите запрос
   - Выберите видео из результатов

2. **Просмотр по ссылке:**
   - Отправьте ссылку на YouTube видео
   - Нажмите "Смотреть в плеере"

3. **Встроенный плеер:**
   - Нажмите кнопку "Открыть YouTube Player"
   - Используйте поиск или вставьте ссылку

4. **Скачивание:**
   - Отправьте ссылку на видео
   - Выберите качество (720p/480p)
   - Дождитесь загрузки

## 🔐 Настройка прокси

### Использование Invidious (рекомендуется)

Invidious - это альтернативный фронтенд для YouTube, который работает в России.

Публичные инстансы:
- https://invidious.io
- https://yewtu.be
- https://inv.riverside.rocks

Настройте в `.env`:
```env
INVIDIOUS_INSTANCE=https://invidious.io
```

### Использование SOCKS5/HTTP прокси

Если у вас есть прокси-сервер:

```env
PROXY_URL=socks5://username:password@host:port
# или
PROXY_URL=http://host:port
```

### Настройка собственного прокси

**Вариант 1: Shadowsocks**

```bash
# Установка
pip install shadowsocks

# Запуск
sslocal -s server_ip -p server_port -l 1080 -k password -m aes-256-cfb

# В .env
PROXY_URL=socks5://127.0.0.1:1080
```

**Вариант 2: V2Ray**

```bash
# Установка v2ray
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)

# Настройка config.json
# Запуск
systemctl start v2ray

# В .env
PROXY_URL=socks5://127.0.0.1:1080
```

## 🌐 Деплой на сервер

### Использование systemd (Linux)

Создайте файл `/etc/systemd/system/youtube-bot.service`:

```ini
[Unit]
Description=YouTube Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/youtube-telegram-bot/bot
ExecStart=/usr/bin/python3 /path/to/youtube-telegram-bot/bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запуск:

```bash
sudo systemctl daemon-reload
sudo systemctl enable youtube-bot
sudo systemctl start youtube-bot
sudo systemctl status youtube-bot
```

### Использование Docker

Создайте `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/
COPY .env .

CMD ["python", "bot/main.py"]
```

Создайте `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bot:
    build: .
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./downloads:/app/downloads
```

Запуск:

```bash
docker-compose up -d
```

## ⚠️ Важные замечания

1. **HTTPS обязателен** - Telegram требует HTTPS для мини-приложений
2. **Размер файлов** - Telegram ограничивает размер файлов до 50 МБ для ботов
3. **Прокси** - Для работы в России рекомендуется использовать Invidious или прокси
4. **Легальность** - Убедитесь, что использование бота соответствует законодательству вашей страны

## 🐛 Решение проблем

### Бот не отвечает

- Проверьте токен в `.env`
- Проверьте интернет-соединение
- Проверьте логи: `python bot/main.py`

### Не работает мини-приложение

- Убедитесь, что используется HTTPS
- Проверьте правильность URL в `.env` и настройках бота
- Откройте консоль браузера для проверки ошибок

### Не удается скачать видео

- Проверьте размер видео (макс. 50 МБ)
- Убедитесь, что установлен `yt-dlp`
- Проверьте наличие прокси в `.env`

### Видео не воспроизводится

- Попробуйте другой Invidious инстанс
- Проверьте настройки прокси
- Убедитесь, что видео доступно

## 📝 Лицензия

MIT License

## 🤝 Вклад в проект

Приветствуются pull requests и issue reports!

## 📧 Поддержка

Если у вас возникли вопросы, создайте issue в репозитории.

## ⭐ Благодарности

- [aiogram](https://github.com/aiogram/aiogram) - Фреймворк для Telegram ботов
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Загрузчик YouTube видео
- [Invidious](https://github.com/iv-org/invidious) - Альтернативный фронтенд YouTube

---

**Дисклеймер:** Этот проект создан в образовательных целях. Убедитесь, что его использование соответствует законодательству вашей страны и условиям использования YouTube.
