# 🧠 Yerel Sesli Yapay Zeka Asistanı (Jarvis Clone)

Bu proje, tamamen **Offline (İnternetsiz)** ve **Yerel** kaynaklarla çalışan, sesli komutları algılayan, internette arama yapabilen ve LLM (Büyük Dil Modeli) ile sohbet edebilen modern bir asistan uygulamasıdır.

![Python](https://img.shields.io/badge/Python-3.10-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Modern-green) ![Ollama](https://img.shields.io/badge/AI-Ollama-orange)

## 🚀 Özellikler

* **🗣️ Ses Algılama (STT):** `Faster-Whisper` modeli ile (int8 quantization) işlemci dostu, yüksek doğruluklu Türkçe ses tanıma.
* **🧠 Yapay Zeka Beyni (LLM):** `Ollama` üzerinden çalışan **Qwen 2.5 (3B)** modeli ile mantıklı sohbet yeteneği ve kod yazma desteği.
* **🔊 Sesli Cevap (TTS):** Asistanın cevaplarını `gTTS` ve `mpg123` optimizasyonu ile takılmadan seslendirme.
* **🌐 İnternet Araması:** DuckDuckGo API ile anlık bilgi çekme ve kartlar halinde gösterme.
* **💻 Sistem Kontrolü:** Hesap makinesi, not defteri gibi uygulamaları sesle açabilme.
* **🎨 Modern Arayüz:** WebSocket tabanlı, gecikmesiz (real-time) akan sohbet ekranı (HTML/JS).

## 🛠️ Kurulum

1.  **Gereksinimleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Sistem Paketlerini Kurun (Linux):**
    ```bash
    sudo apt install mpg123
    ```

3.  **Ollama ve Modeli Kurun:**
    * [Ollama](https://ollama.com) indirin.
    * Modeli çekin: `ollama run qwen2.5:3b`

## ▶️ Kullanım

Uygulamayı başlatmak için tek komut yeterlidir:

```bash
python3 main.py

Tarayıcınızda http://localhost:8000 adresine gidin ve mikrofon butonuna basın.

🏗️ Mimari
Backend: Python FastAPI (WebSocket)

Frontend: HTML5, CSS3, Vanilla JS

AI Engine: Ollama (Local LLM)

Database: SQLite (Sohbet geçmişi logları için)

Geliştirici: Utku Kalender
