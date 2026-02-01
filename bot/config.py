import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Settings
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-domain.com/webapp')

# Proxy Settings
PROXY_URL = os.getenv('PROXY_URL', '')

# Invidious Settings
INVIDIOUS_INSTANCE = os.getenv('INVIDIOUS_INSTANCE', 'https://invidious.io')

# Download Settings
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', './downloads')
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 50))  # MB

# Create downloads directory if not exists
os.makedirs(DOWNLOAD_PATH, exist_ok=True)
