# 🌐 Развертывание (Deployment)

Руководство по развертыванию бота на различных платформах.

## 📱 Развертывание Web App

### 1. GitHub Pages (Бесплатно, рекомендуется)

**Преимущества:**
- Бесплатно
- HTTPS из коробки
- Простая настройка

**Шаги:**

1. Создайте репозиторий на GitHub
2. Загрузите папку `webapp/` в корень репозитория
3. Перейдите в Settings → Pages
4. Source: выберите `main` branch
5. Сохраните и дождитесь деплоя
6. URL будет: `https://username.github.io/repo-name/webapp/`

**Автоматизация с GitHub Actions:**

Создайте `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./webapp
```

### 2. Vercel (Бесплатно)

**Преимущества:**
- Автоматический деплой
- Быстрый CDN
- Простая интеграция с Git

**Шаги:**

1. Зарегистрируйтесь на [vercel.com](https://vercel.com)
2. Нажмите "New Project"
3. Импортируйте репозиторий или загрузите папку
4. Root Directory: укажите `webapp`
5. Deploy
6. URL будет: `https://project-name.vercel.app`

### 3. Netlify (Бесплатно)

**Шаги:**

1. Зарегистрируйтесь на [netlify.com](https://netlify.com)
2. Drag & drop папку `webapp/` в Netlify
3. Или подключите Git репозиторий
4. Deploy
5. URL будет: `https://project-name.netlify.app`

### 4. Cloudflare Pages (Бесплатно)

**Шаги:**

1. Зарегистрируйтесь на [pages.cloudflare.com](https://pages.cloudflare.com)
2. Create a project
3. Connect your Git repository
4. Build settings: Root directory = `webapp`
5. Deploy

## 🤖 Развертывание Бота

### 1. VPS (DigitalOcean, Hetzner, etc.)

**Установка на Ubuntu 20.04+:**

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и зависимостей
sudo apt install python3 python3-pip python3-venv git -y

# Клонирование проекта
git clone https://github.com/yourusername/youtube-telegram-bot.git
cd youtube-telegram-bot

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка .env
cp .env.example .env
nano .env  # Отредактируйте конфигурацию
```

**Создание systemd службы:**

```bash
sudo nano /etc/systemd/system/youtube-bot.service
```

```ini
[Unit]
Description=YouTube Telegram Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/yourusername/youtube-telegram-bot
Environment="PATH=/home/yourusername/youtube-telegram-bot/venv/bin"
ExecStart=/home/yourusername/youtube-telegram-bot/venv/bin/python bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Запуск:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable youtube-bot
sudo systemctl start youtube-bot
sudo systemctl status youtube-bot
```

**Просмотр логов:**

```bash
sudo journalctl -u youtube-bot -f
```

### 2. Docker

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов
COPY bot/ ./bot/
COPY .env .

# Создание директории для скачиваний
RUN mkdir -p downloads

# Запуск
CMD ["python", "bot/main.py"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: youtube-telegram-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./downloads:/app/downloads
    networks:
      - bot-network

  # Опционально: прокси-сервер
  proxy:
    build: .
    container_name: youtube-proxy
    command: python proxy_server.py
    restart: unless-stopped
    ports:
      - "8080:8080"
    env_file:
      - .env
    networks:
      - bot-network

networks:
  bot-network:
    driver: bridge
```

**Запуск:**

```bash
docker-compose up -d
```

**Просмотр логов:**

```bash
docker-compose logs -f bot
```

### 3. Heroku (Бесплатный tier)

**Создайте файлы:**

`Procfile`:
```
worker: python bot/main.py
```

`runtime.txt`:
```
python-3.10.8
```

**Деплой:**

```bash
# Установка Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Логин
heroku login

# Создание приложения
heroku create youtube-telegram-bot

# Установка переменных окружения
heroku config:set BOT_TOKEN=your_token
heroku config:set WEBAPP_URL=your_webapp_url
heroku config:set INVIDIOUS_INSTANCE=https://invidious.io

# Деплой
git push heroku main

# Запуск
heroku ps:scale worker=1

# Логи
heroku logs --tail
```

### 4. Railway (Бесплатно)

1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Выберите репозиторий
4. Добавьте переменные окружения
5. Deploy

### 5. Fly.io

**fly.toml:**

```toml
app = "youtube-telegram-bot"

[build]
  builder = "paketobuildpacks/builder:base"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80
```

**Деплой:**

```bash
# Установка flyctl
curl -L https://fly.io/install.sh | sh

# Логин
flyctl auth login

# Запуск
flyctl launch

# Установка секретов
flyctl secrets set BOT_TOKEN=your_token
flyctl secrets set WEBAPP_URL=your_url

# Деплой
flyctl deploy
```

## 🔒 Настройка HTTPS для Web App

Telegram требует HTTPS для мини-приложений!

### Вариант 1: Использовать готовые платформы

GitHub Pages, Vercel, Netlify - уже имеют HTTPS.

### Вариант 2: Let's Encrypt + Nginx

```bash
# Установка certbot
sudo apt install certbot python3-certbot-nginx -y

# Настройка nginx
sudo nano /etc/nginx/sites-available/youtube-webapp
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /var/www/youtube-webapp;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
# Активация сайта
sudo ln -s /etc/nginx/sites-available/youtube-webapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Получение SSL сертификата
sudo certbot --nginx -d yourdomain.com

# Копирование файлов webapp
sudo mkdir -p /var/www/youtube-webapp
sudo cp -r webapp/* /var/www/youtube-webapp/
```

## 📊 Мониторинг

### Логирование

Добавьте в `bot/main.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

# Настройка логирования в файл
handler = RotatingFileHandler(
    'bot.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logging.getLogger().addHandler(handler)
```

### Уведомления об ошибках

Настройте отправку ошибок себе в Telegram:

```python
ADMIN_ID = 123456789  # Ваш Telegram ID

async def notify_admin(message: str):
    try:
        await bot.send_message(ADMIN_ID, f"⚠️ Ошибка:\n{message}")
    except:
        pass
```

## 🔄 Автообновление

### GitHub Webhook + автоматический деплой

```bash
#!/bin/bash
# update.sh

cd /path/to/youtube-telegram-bot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart youtube-bot
```

Настройте webhook в GitHub Settings → Webhooks.

## 💡 Рекомендации

1. **Используйте .env для секретов** - никогда не коммитьте токены в Git
2. **Логирование** - настройте логи для отладки
3. **Мониторинг** - используйте UptimeRobot или подобные сервисы
4. **Backup** - регулярно делайте резервные копии
5. **Обновления** - следите за обновлениями зависимостей

## 🆘 Помощь

Если возникли проблемы, проверьте:
- Логи бота
- Правильность переменных окружения
- Доступность Web App по HTTPS
- Настройки в @BotFather
