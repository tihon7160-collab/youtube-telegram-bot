import re
import requests
import yt_dlp
from typing import Optional, Dict, List
from config import PROXY_URL, INVIDIOUS_INSTANCE, DOWNLOAD_PATH, MAX_FILE_SIZE


def extract_video_id(url: str) -> Optional[str]:
    """Извлекает ID видео из YouTube URL."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def search_youtube(query: str, max_results: int = 10) -> List[Dict]:
    """Поиск видео на YouTube через Invidious API."""
    try:
        url = f"{INVIDIOUS_INSTANCE}/api/v1/search"
        params = {
            'q': query,
            'type': 'video',
            'sort_by': 'relevance'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        videos = response.json()[:max_results]

        results = []
        for video in videos:
            results.append({
                'id': video.get('videoId'),
                'title': video.get('title'),
                'author': video.get('author'),
                'duration': video.get('lengthSeconds', 0),
                'views': video.get('viewCount', 0),
                'thumbnail': video.get('videoThumbnails', [{}])[0].get('url', '')
            })

        return results
    except Exception as e:
        print(f"Ошибка поиска: {e}")
        return []


def get_video_info(video_id: str) -> Optional[Dict]:
    """Получает информацию о видео через Invidious API."""
    try:
        url = f"{INVIDIOUS_INSTANCE}/api/v1/videos/{video_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            'id': video_id,
            'title': data.get('title'),
            'author': data.get('author'),
            'description': data.get('description', '')[:200] + '...',
            'duration': data.get('lengthSeconds', 0),
            'views': data.get('viewCount', 0),
            'likes': data.get('likeCount', 0),
            'thumbnail': data.get('videoThumbnails', [{}])[0].get('url', ''),
            'formats': data.get('formatStreams', [])
        }
    except Exception as e:
        print(f"Ошибка получения информации о видео: {e}")
        return None


def format_duration(seconds: int) -> str:
    """Форматирует длительность видео."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_views(views: int) -> str:
    """Форматирует количество просмотров."""
    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M"
    elif views >= 1_000:
        return f"{views / 1_000:.1f}K"
    return str(views)


def download_video(video_id: str, quality: str = 'best') -> Optional[str]:
    """Скачивает видео используя yt-dlp."""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            'format': f'{quality}[ext=mp4]/best[ext=mp4]/best',
            'outtmpl': f'{DOWNLOAD_PATH}/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }

        # Добавляем прокси если указан
        if PROXY_URL:
            ydl_opts['proxy'] = PROXY_URL

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # Проверяем размер файла
            import os
            file_size_mb = os.path.getsize(filename) / (1024 * 1024)

            if file_size_mb > MAX_FILE_SIZE:
                os.remove(filename)
                return None

            return filename
    except Exception as e:
        print(f"Ошибка скачивания видео: {e}")
        return None


def get_stream_url(video_id: str, quality: str = '720p') -> Optional[str]:
    """Получает прямую ссылку на видео поток через Invidious."""
    try:
        info = get_video_info(video_id)
        if not info or 'formats' not in info:
            return None

        # Ищем формат с нужным качеством
        for fmt in info['formats']:
            if quality in fmt.get('qualityLabel', ''):
                return fmt.get('url')

        # Если не найдено, возвращаем первый доступный
        if info['formats']:
            return info['formats'][0].get('url')

        return None
    except Exception as e:
        print(f"Ошибка получения ссылки на видео: {e}")
        return None
