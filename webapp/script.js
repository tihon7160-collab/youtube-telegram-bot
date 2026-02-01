// Инициализация Telegram Web App
const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

// API endpoint (замените на ваш backend или используйте Invidious)
const INVIDIOUS_API = 'https://invidious.io/api/v1';

// Элементы DOM
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const searchResults = document.getElementById('searchResults');
const playerContainer = document.getElementById('playerContainer');
const videoPlayer = document.getElementById('videoPlayer');
const videoTitle = document.getElementById('videoTitle');
const videoAuthor = document.getElementById('videoAuthor');
const videoViews = document.getElementById('videoViews');
const videoDuration = document.getElementById('videoDuration');
const closePlayerBtn = document.getElementById('closePlayerBtn');
const loader = document.getElementById('loader');
const errorMessage = document.getElementById('errorMessage');
const trendingVideos = document.getElementById('trendingVideos');

// Текущее видео
let currentVideoId = null;

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    // Применяем тему Telegram
    applyTelegramTheme();

    // Проверяем параметры URL
    const urlParams = new URLSearchParams(window.location.search);
    const videoId = urlParams.get('v');

    if (videoId) {
        playVideo(videoId);
    } else {
        loadTrendingVideos();
    }

    // События
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    closePlayerBtn.addEventListener('click', closePlayer);
});

// Применение темы Telegram
function applyTelegramTheme() {
    const root = document.documentElement;
    root.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color || '#ffffff');
    root.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color || '#000000');
    root.style.setProperty('--tg-theme-hint-color', tg.themeParams.hint_color || '#999999');
    root.style.setProperty('--tg-theme-link-color', tg.themeParams.link_color || '#2481cc');
    root.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color || '#2481cc');
    root.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color || '#ffffff');
}

// Поиск видео
async function handleSearch() {
    const query = searchInput.value.trim();

    if (!query) {
        showError('Введите поисковый запрос');
        return;
    }

    // Проверка на YouTube ссылку
    const videoId = extractVideoId(query);
    if (videoId) {
        playVideo(videoId);
        return;
    }

    // Поиск видео
    showLoader(true);
    hideError();
    searchResults.innerHTML = '';

    try {
        const videos = await searchVideos(query);

        if (videos.length === 0) {
            showError('Ничего не найдено');
            return;
        }

        displaySearchResults(videos);
    } catch (error) {
        console.error('Ошибка поиска:', error);
        showError('Ошибка при поиске видео');
    } finally {
        showLoader(false);
    }
}

// Поиск видео через Invidious API
async function searchVideos(query) {
    const response = await fetch(`${INVIDIOUS_API}/search?q=${encodeURIComponent(query)}&type=video`);

    if (!response.ok) {
        throw new Error('Ошибка при поиске');
    }

    const data = await response.json();
    return data.slice(0, 10);
}

// Получение информации о видео
async function getVideoInfo(videoId) {
    const response = await fetch(`${INVIDIOUS_API}/videos/${videoId}`);

    if (!response.ok) {
        throw new Error('Ошибка при получении информации о видео');
    }

    return await response.json();
}

// Загрузка популярных видео
async function loadTrendingVideos() {
    showLoader(true);

    try {
        const response = await fetch(`${INVIDIOUS_API}/trending`);
        const videos = await response.json();

        displayTrendingVideos(videos.slice(0, 12));
    } catch (error) {
        console.error('Ошибка загрузки популярных видео:', error);
    } finally {
        showLoader(false);
    }
}

// Отображение результатов поиска
function displaySearchResults(videos) {
    searchResults.innerHTML = '';

    videos.forEach(video => {
        const card = createVideoCard(video);
        searchResults.appendChild(card);
    });
}

// Отображение популярных видео
function displayTrendingVideos(videos) {
    trendingVideos.innerHTML = '';

    videos.forEach(video => {
        const card = createVideoCard(video);
        trendingVideos.appendChild(card);
    });
}

// Создание карточки видео
function createVideoCard(video) {
    const card = document.createElement('div');
    card.className = 'video-card';
    card.onclick = () => playVideo(video.videoId);

    const thumbnail = video.videoThumbnails?.[0]?.url || '';

    card.innerHTML = `
        <div class="video-card-thumbnail">
            <img src="${thumbnail}" alt="${video.title}" loading="lazy">
            <span class="video-duration">${formatDuration(video.lengthSeconds)}</span>
        </div>
        <div class="video-card-info">
            <div class="video-card-title">${video.title}</div>
            <div class="video-card-author">${video.author}</div>
            <div class="video-card-views">${formatViews(video.viewCount)} просмотров</div>
        </div>
    `;

    return card;
}

// Воспроизведение видео
async function playVideo(videoId) {
    showLoader(true);
    hideError();

    try {
        const videoInfo = await getVideoInfo(videoId);

        currentVideoId = videoId;

        // Используем Invidious для проигрывания
        const embedUrl = `https://invidious.io/embed/${videoId}?autoplay=1`;
        videoPlayer.src = embedUrl;

        // Обновляем информацию о видео
        videoTitle.textContent = videoInfo.title;
        videoAuthor.textContent = videoInfo.author;
        videoViews.textContent = `👁 ${formatViews(videoInfo.viewCount)} просмотров`;
        videoDuration.textContent = `⏱ ${formatDuration(videoInfo.lengthSeconds)}`;

        // Показываем плеер
        playerContainer.classList.remove('hidden');
        playerContainer.scrollIntoView({ behavior: 'smooth' });

        // Уведомляем Telegram о воспроизведении
        tg.HapticFeedback.impactOccurred('medium');
    } catch (error) {
        console.error('Ошибка воспроизведения:', error);
        showError('Не удалось загрузить видео');
    } finally {
        showLoader(false);
    }
}

// Закрытие плеера
function closePlayer() {
    videoPlayer.src = '';
    playerContainer.classList.add('hidden');
    currentVideoId = null;
}

// Извлечение ID видео из YouTube URL
function extractVideoId(url) {
    const patterns = [
        /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/,
        /youtube\.com\/embed\/([a-zA-Z0-9_-]{11})/,
        /youtube\.com\/v\/([a-zA-Z0-9_-]{11})/,
    ];

    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match) {
            return match[1];
        }
    }

    return null;
}

// Форматирование длительности
function formatDuration(seconds) {
    if (!seconds) return '0:00';

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
        return `${hours}:${padZero(minutes)}:${padZero(secs)}`;
    }
    return `${minutes}:${padZero(secs)}`;
}

// Форматирование просмотров
function formatViews(views) {
    if (!views) return '0';

    if (views >= 1000000) {
        return `${(views / 1000000).toFixed(1)}M`;
    } else if (views >= 1000) {
        return `${(views / 1000).toFixed(1)}K`;
    }
    return views.toString();
}

// Добавление нуля
function padZero(num) {
    return num.toString().padStart(2, '0');
}

// Показать/скрыть загрузку
function showLoader(show) {
    if (show) {
        loader.classList.remove('hidden');
    } else {
        loader.classList.add('hidden');
    }
}

// Показать ошибку
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    setTimeout(() => {
        hideError();
    }, 5000);
}

// Скрыть ошибку
function hideError() {
    errorMessage.classList.add('hidden');
}

// Обработка кнопки "Назад" Telegram
tg.BackButton.onClick(() => {
    if (currentVideoId) {
        closePlayer();
    } else {
        tg.close();
    }
});

// Показываем кнопку "Назад" когда видео открыто
if (currentVideoId) {
    tg.BackButton.show();
}
