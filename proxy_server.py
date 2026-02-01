"""
Простой прокси-сервер для обхода блокировок YouTube.
Используется для проксирования запросов к YouTube API и видео потокам.
"""

from aiohttp import web
import aiohttp
import asyncio
from typing import Optional


class YouTubeProxyServer:
    """Прокси-сервер для YouTube."""

    def __init__(self, proxy_url: Optional[str] = None, port: int = 8080):
        self.proxy_url = proxy_url
        self.port = port
        self.app = web.Application()
        self.setup_routes()

    def setup_routes(self):
        """Настройка маршрутов."""
        self.app.router.add_route('GET', '/proxy/video', self.proxy_video)
        self.app.router.add_route('GET', '/proxy/api/{path:.*}', self.proxy_api)
        self.app.router.add_route('GET', '/health', self.health_check)

    async def proxy_video(self, request: web.Request) -> web.StreamResponse:
        """Проксирование видео потока."""
        video_url = request.query.get('url')

        if not video_url:
            return web.json_response({'error': 'URL not provided'}, status=400)

        try:
            async with aiohttp.ClientSession() as session:
                proxy = self.proxy_url if self.proxy_url else None

                async with session.get(video_url, proxy=proxy) as resp:
                    if resp.status != 200:
                        return web.json_response(
                            {'error': 'Failed to fetch video'},
                            status=resp.status
                        )

                    # Создаем потоковый ответ
                    response = web.StreamResponse(
                        status=200,
                        headers={
                            'Content-Type': resp.headers.get('Content-Type', 'video/mp4'),
                            'Content-Length': resp.headers.get('Content-Length', '0'),
                            'Accept-Ranges': 'bytes',
                        }
                    )

                    await response.prepare(request)

                    # Потоково передаем данные
                    async for chunk in resp.content.iter_chunked(8192):
                        await response.write(chunk)

                    await response.write_eof()
                    return response

        except Exception as e:
            print(f"Ошибка проксирования видео: {e}")
            return web.json_response({'error': str(e)}, status=500)

    async def proxy_api(self, request: web.Request) -> web.Response:
        """Проксирование API запросов."""
        path = request.match_info['path']
        api_url = f"https://www.googleapis.com/youtube/v3/{path}"

        # Добавляем параметры запроса
        if request.query_string:
            api_url += f"?{request.query_string}"

        try:
            async with aiohttp.ClientSession() as session:
                proxy = self.proxy_url if self.proxy_url else None

                async with session.get(api_url, proxy=proxy) as resp:
                    data = await resp.json()
                    return web.json_response(data, status=resp.status)

        except Exception as e:
            print(f"Ошибка проксирования API: {e}")
            return web.json_response({'error': str(e)}, status=500)

    async def health_check(self, request: web.Request) -> web.Response:
        """Проверка здоровья сервера."""
        return web.json_response({
            'status': 'ok',
            'proxy_enabled': self.proxy_url is not None
        })

    def run(self):
        """Запуск сервера."""
        print(f"🚀 Прокси-сервер запущен на порту {self.port}")
        print(f"📡 Прокси: {self.proxy_url or 'Не используется'}")
        web.run_app(self.app, port=self.port)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    proxy_url = os.getenv('PROXY_URL', '')
    port = int(os.getenv('PROXY_SERVER_PORT', 8080))

    server = YouTubeProxyServer(proxy_url=proxy_url, port=port)
    server.run()
