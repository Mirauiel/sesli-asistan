# Sera AI v2.0 - Tamamen Offline Linux Asistanı

Bu proje, **Pop!_OS (Linux)** sistemleri için optimize edilmiş, gizlilik odaklı ve **tamamen yerel (offline)** çalışabilen bir yapay zeka asistanıdır.

İnternet bağlantısına ihtiyaç duymaz. Sesinizi **Whisper** ile duyar, **Qwen** ile düşünür ve **Piper TTS** ile konuşur.

## 🚀 Özellikler

* **🧠 %100 Yerel Zeka (GGUF):** `llama.cpp` altyapısıyla `Qwen 2.5` modelini doğrudan RAM üzerinde çalıştırır.
* **🗣️ Offline Ses (Piper):** Nöral metin okuma motoru **Piper** ve `dfki-medium` modeli ile akıcı Türkçe konuşma sağlar. (İnternet gerektirmez).
* **👂 Hızlı Duyma:** `faster-whisper` altyapısı ile anlık Türkçe ses tanıma.
* **🐧 Linux Entegrasyonu:** `aplay` ile ses çalar, terminal komutlarını yönetir.
* **🌐 Web Arayüzü:** FastAPI ve WebSocket tabanlı sohbet ekranı.

## 📂 Proje Yapısı

```text
Sera_AI/
├── 📄 main.py            # 🚀 Ana Başlatıcı
├── 📄 config.py          # Ayar Dosyası
├── 📄 requirements.txt   # Kütüphane Listesi
├── 📄 dataset.jsonl      # 💎 Karakter Eğitimi İçin Özgün Veri Seti
├── 📂 core/              # Sistemin Organları
│   ├── 📄 llm.py         # Zeka Motoru (Llama-cpp-python)
│   ├── 📄 audio.py       # Ses İşleme (Whisper + Piper TTS)
│   └── 📄 system.py      # Refleksler
│   └── 📄 memory.py      # Hafıza (SQLite)
├── 📂 models/            # 🧠 Yapay Zeka Modelleri (GGUF)
│   └── 📄 sera_v2.gguf   # (Bu dosyayı indirmeniz gerekir)
├── 📂 piper_tts/         # 🗣️ Ses Modelleri ve Piper Motoru
│   ├── 📂 piper/         # Piper Binary dosyaları
│   └── 📄 tr_TR-dfki-medium.onnx  # Türkçe Ses Modeli
└── 📂 templates/         # HTML/JS Arayüzü
    └── 📄 index.html
    
🛠️ Kurulum

1. Projeyi Klonlayın
git clone [https://github.com/Mirauiel/sera-ai.git](https://github.com/Mirauiel/sera-ai.git)
cd sera-ai

2. Sanal Ortamı Kurun
python3 -m venv venv
source venv/bin/activate

3. Sistem Gereksinimleri (Linux)
Whisper ve ses çalma için gereklidir:
sudo apt update
sudo apt install ffmpeg portaudio19-dev alsa-utils -y

4. Python Kütüphanelerini Yükleyin
pip install -r requirements.txt

5. Modelleri Yerleştirin (ÖNEMLİ)
Sistemin çalışması için aşağıdaki dosya yapısını oluşturmalısınız:

A. LLM Modeli: models/ klasörüne sera_v2.gguf dosyasını koyun.

B. Piper TTS (Ses Motoru): piper_tts/ klasörü içine şunları indirin:

  1. Piper Binary: Linux için Piper binary dosyalarını piper_tts/piper/ klasörüne çıkarın.
  2. Ses Modeli: tr_TR-dfki-medium.onnx ve .json dosyasını piper_tts/ ana dizinine koyun.

Klasör yapısı şöyle görünmelidir:  
piper_tts/
  ├── tr_TR-dfki-medium.onnx
  ├── tr_TR-dfki-medium.onnx.json
  └── piper/
       └── piper (çalıştırılabilir dosya)
       
🚀 Çalıştırma
python3 main.py
Tarayıcınızda http://localhost:8000 adresine gidin.
