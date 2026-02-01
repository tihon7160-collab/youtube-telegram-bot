# 📖 Примеры использования

## Примеры взаимодействия с ботом

### 1. Поиск видео

**Пользователь:**
```
/search
```

**Бот:**
```
🔍 Введите поисковый запрос:
```

**Пользователь:**
```
python tutorial for beginners
```

**Бот отправляет:**
- 5-10 видео с превью
- Кнопки для каждого видео:
  - ▶️ Открыть в плеере
  - 📋 Инфо
  - ⬇️ Скачать

### 2. Просмотр по ссылке

**Пользователь:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Бот отправляет:**
```
🎬 Rick Astley - Never Gonna Give You Up

👤 Rick Astley
⏱ 3:33
👁 1.2B просмотров
👍 15M лайков

📝 The official video for "Never Gonna Give You Up"...

[▶️ Смотреть в плеере]
[⬇️ Скачать 720p] [⬇️ Скачать 480p]
[🔗 Открыть в YouTube]
```

### 3. Скачивание видео

**Пользователь нажимает:** `⬇️ Скачать 720p`

**Бот:**
```
⏳ Скачиваю видео (качество: 720p)...
Это может занять некоторое время.

📤 Отправляю видео...

[Видео отправлено]

✅ Видео успешно отправлено!
```

### 4. Использование мини-приложения

**Пользователь нажимает:** `🎬 Открыть YouTube Player`

Открывается мини-приложение с:
- Поисковой строкой
- Популярными видео
- Встроенным плеером

**Поиск в мини-приложении:**
1. Ввод запроса: `react hooks tutorial`
2. Отображение результатов
3. Клик на видео → воспроизведение

## Примеры кода для расширения

### Добавление новой команды

В `bot/handlers.py`:

```python
@router.message(Command("top"))
async def cmd_top(message: Message):
    """Показать топ видео."""
    await message.answer("⏳ Загружаю топ видео...")

    # Используем Invidious для получения популярных видео
    try:
        url = f"{INVIDIOUS_INSTANCE}/api/v1/trending"
        response = requests.get(url, timeout=10)
        videos = response.json()[:10]

        for video in videos:
            caption = (
                f"🎬 <b>{video['title']}</b>\n\n"
                f"👤 {video['author']}\n"
                f"👁 {format_views(video['viewCount'])} просмотров"
            )

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="▶️ Открыть",
                    web_app=WebAppInfo(url=f"{WEBAPP_URL}?v={video['videoId']}")
                )]
            ])

            await message.answer(caption, parse_mode="HTML", reply_markup=keyboard)

    except Exception as e:
        await message.answer("❌ Ошибка загрузки топа")
```

### Добавление кнопок в главное меню

В `bot/handlers.py`:

```python
@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 YouTube Player", web_app=WebAppInfo(url=WEBAPP_URL))],
        [
            InlineKeyboardButton(text="🔍 Поиск", callback_data="search"),
            InlineKeyboardButton(text="🔥 Популярное", callback_data="trending")
        ],
        [
            InlineKeyboardButton(text="📚 Подписки", callback_data="subscriptions"),
            InlineKeyboardButton(text="⭐ Избранное", callback_data="favorites")
        ],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])

    await message.answer(
        "👋 Добро пожаловать!",
        reply_markup=keyboard
    )
```

### Сохранение истории просмотров

Создайте `bot/database.py`:

```python
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='history.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS watch_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                video_id TEXT,
                title TEXT,
                watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_to_history(self, user_id: int, video_id: str, title: str):
        self.conn.execute(
            'INSERT INTO watch_history (user_id, video_id, title) VALUES (?, ?, ?)',
            (user_id, video_id, title)
        )
        self.conn.commit()

    def get_history(self, user_id: int, limit: int = 10):
        cursor = self.conn.execute(
            'SELECT video_id, title, watched_at FROM watch_history WHERE user_id = ? ORDER BY watched_at DESC LIMIT ?',
            (user_id, limit)
        )
        return cursor.fetchall()
```

Использование в `bot/handlers.py`:

```python
from database import Database

db = Database()

@router.message(Command("history"))
async def cmd_history(message: Message):
    """Показать историю просмотров."""
    history = db.get_history(message.from_user.id)

    if not history:
        await message.answer("📭 История пуста")
        return

    text = "📚 <b>История просмотров:</b>\n\n"

    for video_id, title, watched_at in history:
        text += f"🎬 {title}\n"
        text += f"🕐 {watched_at}\n"
        text += f"🔗 youtube.com/watch?v={video_id}\n\n"

    await message.answer(text, parse_mode="HTML")

# В функции playVideo добавьте:
db.add_to_history(message.from_user.id, video_id, video_info['title'])
```

### Добавление подписок на каналы

В `bot/database.py`:

```python
def subscribe_channel(self, user_id: int, channel_id: str, channel_name: str):
    self.conn.execute(
        'INSERT OR IGNORE INTO subscriptions (user_id, channel_id, channel_name) VALUES (?, ?, ?)',
        (user_id, channel_id, channel_name)
    )
    self.conn.commit()

def get_subscriptions(self, user_id: int):
    cursor = self.conn.execute(
        'SELECT channel_id, channel_name FROM subscriptions WHERE user_id = ?',
        (user_id,)
    )
    return cursor.fetchall()
```

### Webhook вместо polling

В `bot/main.py`:

```python
from aiohttp import web

async def webhook(request):
    """Обработка webhook от Telegram."""
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response(text="ok")

async def on_startup():
    """Установка webhook при старте."""
    webhook_url = f"https://your-domain.com/webhook/{BOT_TOKEN}"
    await bot.set_webhook(webhook_url)

async def on_shutdown():
    """Удаление webhook при остановке."""
    await bot.delete_webhook()

if __name__ == '__main__':
    app = web.Application()
    app.router.add_post(f'/webhook/{BOT_TOKEN}', webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host='0.0.0.0', port=8080)
```

## Примеры настройки прокси

### SOCKS5 прокси

```env
PROXY_URL=socks5://username:password@proxy-server.com:1080
```

### HTTP прокси

```env
PROXY_URL=http://username:password@proxy-server.com:8080
```

### Shadowsocks

```bash
# Запуск shadowsocks клиента
sslocal -s server_ip -p 8388 -l 1080 -k password -m aes-256-gcm

# В .env
PROXY_URL=socks5://127.0.0.1:1080
```

### Несколько Invidious инстансов (fallback)

В `bot/utils.py`:

```python
INVIDIOUS_INSTANCES = [
    'https://invidious.io',
    'https://yewtu.be',
    'https://inv.riverside.rocks',
    'https://invidious.privacydev.net'
]

def search_youtube(query: str, max_results: int = 10):
    for instance in INVIDIOUS_INSTANCES:
        try:
            url = f"{instance}/api/v1/search"
            response = requests.get(url, params={'q': query}, timeout=5)

            if response.status_code == 200:
                return response.json()[:max_results]
        except:
            continue

    return []
```

## Интеграция с другими сервисами

### Отправка статистики в Google Analytics

В `webapp/script.js`:

```javascript
// Добавьте в <head>
gtag('event', 'video_play', {
    'video_id': videoId,
    'video_title': videoInfo.title
});
```

### Интеграция с базой данных (PostgreSQL)

```bash
pip install asyncpg
```

В `bot/database.py`:

```python
import asyncpg

class AsyncDatabase:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            'postgresql://user:password@localhost/youtube_bot'
        )

    async def add_to_history(self, user_id: int, video_id: str):
        async with self.pool.acquire() as conn:
            await conn.execute(
                'INSERT INTO watch_history (user_id, video_id) VALUES ($1, $2)',
                user_id, video_id
            )
```

## Полезные фишки

### Автоматическое удаление старых скачанных файлов

```python
import os
import time

def cleanup_old_files(directory: str, max_age_hours: int = 1):
    """Удаляет файлы старше указанного времени."""
    now = time.time()
    max_age_seconds = max_age_hours * 3600

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if now - os.path.getmtime(filepath) > max_age_seconds:
                os.remove(filepath)
                print(f"Удален старый файл: {filename}")
```

### Ограничение количества запросов от одного пользователя

```python
from collections import defaultdict
from datetime import datetime, timedelta

user_requests = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 10

def check_rate_limit(user_id: int) -> bool:
    """Проверка лимита запросов."""
    now = datetime.now()
    minute_ago = now - timedelta(minutes=1)

    # Удаляем старые запросы
    user_requests[user_id] = [
        req_time for req_time in user_requests[user_id]
        if req_time > minute_ago
    ]

    if len(user_requests[user_id]) >= MAX_REQUESTS_PER_MINUTE:
        return False

    user_requests[user_id].append(now)
    return True
```

Использование:

```python
@router.message(Command("search"))
async def cmd_search(message: Message):
    if not check_rate_limit(message.from_user.id):
        await message.answer("⚠️ Слишком много запросов. Подождите минуту.")
        return

    # ... остальной код
```
