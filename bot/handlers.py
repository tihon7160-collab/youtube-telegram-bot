import os
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiofiles

from utils import (
    extract_video_id, search_youtube, get_video_info,
    format_duration, format_views, download_video, get_stream_url
)
from config import WEBAPP_URL

router = Router()


class SearchState(StatesGroup):
    waiting_for_query = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Открыть YouTube Player", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="🔍 Поиск видео", callback_data="search")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])

    await message.answer(
        "👋 Добро пожаловать в YouTube Bot!\n\n"
        "Я помогу вам смотреть YouTube видео прямо в Telegram, "
        "даже если YouTube заблокирован в вашей стране.\n\n"
        "Что я умею:\n"
        "🎬 Открыть встроенный плеер\n"
        "🔍 Искать видео по запросу\n"
        "📺 Смотреть видео по ссылке\n"
        "⬇️ Скачивать видео\n\n"
        "Просто отправьте мне ссылку на YouTube видео или воспользуйтесь кнопками ниже!",
        reply_markup=keyboard
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help."""
    await message.answer(
        "📖 <b>Как пользоваться ботом:</b>\n\n"
        "1️⃣ <b>Просмотр по ссылке:</b>\n"
        "Просто отправьте ссылку на YouTube видео, и я открою его в мини-приложении.\n\n"
        "2️⃣ <b>Поиск видео:</b>\n"
        "Используйте команду /search или нажмите кнопку 'Поиск видео', "
        "затем введите запрос.\n\n"
        "3️⃣ <b>Встроенный плеер:</b>\n"
        "Нажмите кнопку 'Открыть YouTube Player' для запуска мини-приложения.\n\n"
        "4️⃣ <b>Скачивание видео:</b>\n"
        "После отправки ссылки, выберите опцию 'Скачать видео'.\n\n"
        "<b>Команды:</b>\n"
        "/start - Главное меню\n"
        "/search - Поиск видео\n"
        "/help - Помощь",
        parse_mode="HTML"
    )


@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    """Обработчик кнопки помощи."""
    await callback.message.edit_text(
        "📖 <b>Как пользоваться ботом:</b>\n\n"
        "1️⃣ <b>Просмотр по ссылке:</b>\n"
        "Просто отправьте ссылку на YouTube видео, и я открою его в мини-приложении.\n\n"
        "2️⃣ <b>Поиск видео:</b>\n"
        "Используйте команду /search или нажмите кнопку 'Поиск видео', "
        "затем введите запрос.\n\n"
        "3️⃣ <b>Встроенный плеер:</b>\n"
        "Нажмите кнопку 'Открыть YouTube Player' для запуска мини-приложения.\n\n"
        "4️⃣ <b>Скачивание видео:</b>\n"
        "После отправки ссылки, выберите опцию 'Скачать видео'.\n\n"
        "<b>Команды:</b>\n"
        "/start - Главное меню\n"
        "/search - Поиск видео\n"
        "/help - Помощь",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(Command("search"))
@router.callback_query(F.data == "search")
async def cmd_search(event, state: FSMContext):
    """Обработчик команды /search."""
    if isinstance(event, CallbackQuery):
        await event.message.answer("🔍 Введите поисковый запрос:")
        await event.answer()
    else:
        await event.answer("🔍 Введите поисковый запрос:")

    await state.set_state(SearchState.waiting_for_query)


@router.message(SearchState.waiting_for_query)
async def process_search(message: Message, state: FSMContext):
    """Обработка поискового запроса."""
    query = message.text.strip()

    if not query:
        await message.answer("❌ Пожалуйста, введите корректный запрос.")
        return

    await message.answer("🔍 Ищу видео...")

    results = search_youtube(query, max_results=5)

    if not results:
        await message.answer("❌ Ничего не найдено. Попробуйте другой запрос.")
        await state.clear()
        return

    for video in results:
        video_url = f"https://youtube.com/watch?v={video['id']}"
        caption = (
            f"🎬 <b>{video['title']}</b>\n\n"
            f"👤 {video['author']}\n"
            f"⏱ {format_duration(video['duration'])}\n"
            f"👁 {format_views(video['views'])} просмотров"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="▶️ Открыть в плеере",
                web_app=WebAppInfo(url=f"{WEBAPP_URL}?v={video['id']}")
            )],
            [
                InlineKeyboardButton(text="📋 Инфо", callback_data=f"info_{video['id']}"),
                InlineKeyboardButton(text="⬇️ Скачать", callback_data=f"download_{video['id']}")
            ]
        ])

        try:
            await message.answer(
                caption,
                parse_mode="HTML",
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Ошибка отправки результата: {e}")

    await state.clear()


@router.message(F.text.regexp(r'(youtube\.com|youtu\.be)'))
async def handle_youtube_link(message: Message):
    """Обработка YouTube ссылок."""
    video_id = extract_video_id(message.text)

    if not video_id:
        await message.answer("❌ Не удалось распознать YouTube ссылку.")
        return

    await message.answer("⏳ Получаю информацию о видео...")

    video_info = get_video_info(video_id)

    if not video_info:
        await message.answer("❌ Не удалось получить информацию о видео.")
        return

    caption = (
        f"🎬 <b>{video_info['title']}</b>\n\n"
        f"👤 {video_info['author']}\n"
        f"⏱ {format_duration(video_info['duration'])}\n"
        f"👁 {format_views(video_info['views'])} просмотров\n"
        f"👍 {format_views(video_info['likes'])} лайков\n\n"
        f"📝 {video_info['description']}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="▶️ Смотреть в плеере",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}?v={video_id}")
        )],
        [
            InlineKeyboardButton(text="⬇️ Скачать 720p", callback_data=f"download_720_{video_id}"),
            InlineKeyboardButton(text="⬇️ Скачать 480p", callback_data=f"download_480_{video_id}")
        ],
        [InlineKeyboardButton(text="🔗 Открыть в YouTube", url=f"https://youtube.com/watch?v={video_id}")]
    ])

    await message.answer(caption, parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data.startswith("info_"))
async def callback_video_info(callback: CallbackQuery):
    """Показать подробную информацию о видео."""
    video_id = callback.data.split("_")[1]

    await callback.answer("⏳ Загружаю информацию...")

    video_info = get_video_info(video_id)

    if not video_info:
        await callback.message.answer("❌ Не удалось получить информацию о видео.")
        return

    caption = (
        f"🎬 <b>{video_info['title']}</b>\n\n"
        f"👤 Автор: {video_info['author']}\n"
        f"⏱ Длительность: {format_duration(video_info['duration'])}\n"
        f"👁 Просмотров: {format_views(video_info['views'])}\n"
        f"👍 Лайков: {format_views(video_info['likes'])}\n\n"
        f"📝 Описание:\n{video_info['description']}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="▶️ Смотреть в плеере",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}?v={video_id}")
        )],
        [InlineKeyboardButton(text="⬇️ Скачать", callback_data=f"download_{video_id}")]
    ])

    await callback.message.answer(caption, parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data.startswith("download_"))
async def callback_download_video(callback: CallbackQuery):
    """Скачивание видео."""
    parts = callback.data.split("_")

    if len(parts) == 3:  # download_720_videoid
        quality = parts[1]
        video_id = parts[2]
    else:  # download_videoid
        quality = "best"
        video_id = parts[1]

    await callback.answer("⏳ Начинаю скачивание...")
    await callback.message.answer(
        f"⏳ Скачиваю видео (качество: {quality})...\n"
        "Это может занять некоторое время."
    )

    try:
        file_path = download_video(video_id, quality)

        if not file_path:
            await callback.message.answer(
                "❌ Не удалось скачать видео.\n"
                "Возможно, файл слишком большой (макс. 50 МБ)."
            )
            return

        # Отправляем файл пользователю
        await callback.message.answer("📤 Отправляю видео...")

        async with aiofiles.open(file_path, 'rb') as video_file:
            await callback.message.answer_video(
                video=video_file,
                caption=f"✅ Видео скачано (качество: {quality})"
            )

        # Удаляем файл после отправки
        os.remove(file_path)
        await callback.message.answer("✅ Видео успешно отправлено!")

    except Exception as e:
        await callback.message.answer(f"❌ Ошибка при скачивании: {str(e)}")
        print(f"Ошибка скачивания: {e}")
