import os

# --- YOL AYARLARI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "database")
LOG_DB_PATH = os.path.join(DB_FOLDER, "logs.db")
MEMORY_DB_PATH = os.path.join(DB_FOLDER, "beyin.db")

# --- YAPAY ZEKA AYARLARI ---
LLM_MODEL = "qwen2.5:3b"  # Model ismini buradan değiştiririz
LLM_TEMP = 0.1            # Yaratıcılık ayarı

# --- SES AYARLARI ---
WHISPER_MODEL_SIZE = "small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE = "int8"
TTS_LANG = "tr"

# --- KLASÖR KONTROLÜ ---
# Database klasörü yoksa oluştur
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)
