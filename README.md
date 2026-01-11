k# 🧠 Jarvis AI Asistan (Python + Local LLM)

Bu proje, tamamen yerel donanım üzerinde çalışan (Offline), sesli komutları algılayan ve Qwen 2.5 yapay zeka modelini kullanan modüler bir asistandır.

## 🚀 Özellikler
- **Yerel LLM:** Ollama üzerinden Qwen 2.5 (3B) modeli ile Türkçe sohbet.
- **Sesli Etkileşim:** `Faster-Whisper` ile duyma, `gTTS/mpg123` ile konuşma.
- **Modüler Mimari:** Kolay geliştirilebilir parça parça yapı (Core, Audio, LLM).
- **Sistem Kontrolü:** Hesap makinesi açma, internet araması yapma (DuckDuckGo).
- **Web Arayüzü:** WebSocket tabanlı modern sohbet ekranı.

## 📂 Proje Yapısı (Modüler)
```text
📁 asistan_proje/
├── 📄 main.py          # Orkestra Şefi (Sistemi Başlatır)
├── 📄 config.py        # Tüm Ayarlar (Model, Yollar)
├── 📂 core/            # Sistemin Beyni ve Organları
│   ├── 📄 llm.py       # Yapay Zeka Entegrasyonu (Ollama)
│   ├── 📄 audio.py     # Ses İşleme (STT / TTS)
│   ├── 📄 system.py    # PC Kontrol & Araçlar
│   └── 📄 memory.py    # Hafıza Sistemi (Geliştirme Aşamasında)
└── 📂 templates/       # HTML Arayüzü


🛠️ Kurulum & Çalıştırma

1 - Gereksinimleri Yükle:

pip install -r requirements.txt

sudo apt install portaudio19-dev mpg123

2 - Ollama Motorunu Başlat:

ollama serve

3 - Asistanı Çalıştır:

python3 main.py

⚠️ Gereksinimler

Linux (Tercihen Ubuntu/Pop!_OS)

Python 3.10+

Min 8GB RAM (Qwen 2.5 için)
