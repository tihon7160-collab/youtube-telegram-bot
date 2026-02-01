# 🚀 Быстрый старт

## За 5 минут

### 1. Создайте бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Придумайте имя: например, `My YouTube Bot`
4. Придумайте username: например, `my_youtube_bot`
5. Скопируйте полученный токен

### 2. Установите зависимости

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройте бота

Создайте файл `.env`:

```env
BOT_TOKEN=ваш_токен_от_BotFather
WEBAPP_URL=https://your-username.github.io/youtube-bot/webapp
INVIDIOUS_INSTANCE=https://invidious.io
DOWNLOAD_PATH=./downloads
MAX_FILE_SIZE=50
```

### 4. Разместите мини-приложение

**GitHub Pages (рекомендуется для начала):**

1. Создайте репозиторий на GitHub
2. Загрузите папку `webapp/`
3. Settings → Pages → Source: main branch
4. Скопируйте URL (типа `https://username.github.io/repo-name/`)
5. Обновите `WEBAPP_URL` в `.env`

### 5. Настройте Menu Button

1. Откройте [@BotFather](https://t.me/BotFather)
2. `/mybots` → выберите бота
3. `Bot Settings` → `Menu Button` → `Configure menu button`
4. Введите URL: `https://your-username.github.io/youtube-bot/webapp/`
5. Текст кнопки: `YouTube Player`

### 6. Запустите бота

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

Или напрямую:
```bash
python bot/main.py
```

### 7. Протестируйте

1. Найдите бота в Telegram
2. Отправьте `/start`
3. Отправьте ссылку на YouTube видео
4. Или нажмите кнопку "Открыть YouTube Player"

## 🎉 Готово!

Ваш бот работает! Теперь можете:

- Искать видео командой `/search`
- Отправлять ссылки на видео
- Скачивать видео
- Смотреть в мини-приложении

## 🔧 Настройка для России

Если YouTube заблокирован, используйте один из вариантов:

### Вариант 1: Invidious (проще)

Уже настроено по умолчанию! Просто убедитесь, что в `.env`:

```env
INVIDIOUS_INSTANCE=https://invidious.io
```

Если не работает, попробуйте другие инстансы:
- https://yewtu.be
- https://inv.riverside.rocks
- https://invidious.privacydev.net

### Вариант 2: Прокси (надежнее)

Если у вас есть SOCKS5/HTTP прокси:

```env
PROXY_URL=socks5://127.0.0.1:1080
```

## ❓ Проблемы?

### Бот не отвечает
- Проверьте правильность токена в `.env`
- Убедитесь, что бот запущен
- Проверьте логи в консоли

### Мини-приложение не открывается
- Убедитесь, что URL использует HTTPS
- Проверьте правильность URL в настройках бота
- Попробуйте открыть URL в браузере

### Видео не воспроизводится
- Смените Invidious инстанс в `.env`
- Проверьте, что видео доступно
- Попробуйте настроить прокси

## 📚 Дальше

- Прочитайте полную документацию в [README.md](README.md)
- Настройте автозапуск на сервере
- Используйте Docker для деплоя
