# 🎙️ Türkçe Yapay Zeka Sesli Asistan

Python tabanlı, yerel (offline) çalışan ve web arayüzü üzerinden kontrol edilebilen, modüler bir sesli asistan projesi.

## 🚀 Özellikler
- **Ses Algılama:** `SpeechRecognition` ile ortam gürültüsüne duyarlı dinleme.
- **STT (Speech-to-Text):** `Faster-Whisper` (int8 quantization) ile yüksek performanslı Türkçe model.
- **Backend:** `FastAPI` ve `WebSocket` ile gerçek zamanlı, asenkron iletişim.
- **Frontend:** Modern ve duyarlı (responsive) HTML/JS arayüzü.
- **Veritabanı:** SQLite ile tüm konuşma geçmişinin loglanması.

## 🛠️ Kurulum ve Çalıştırma

1. Repoyu klonlayın:
   ```bash
   git clone [https://github.com/Mirauiel/sesli-asistan.git](https://github.com/KULLANICI_ADIN/python-sesli-asistan.git)
   cd sesli-asistan

Sanal ortam oluşturun ve kütüphaneleri yükleyin:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt install ffmpeg libespeak1  # Linux sistemler için

Uygulamayı başlatın:

python3 server.py
