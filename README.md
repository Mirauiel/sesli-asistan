# 🧠 Sera AI Asistan (Offline & Fine-Tuned)

Bu proje, tamamen yerel donanım üzerinde çalışan (Offline), internet bağlantısına ihtiyaç duymadan (arama hariç) sohbet edebilen ve özel olarak eğitilmiş **Sera** kişiliğine sahip bir yapay zeka asistanıdır.

**Ollama veya harici bir API kullanmaz.** Doğrudan PyTorch ve PEFT kütüphaneleri ile ince ayar yapılmış (Fine-Tuned) Qwen 2.5 modelini RAM üzerinde çalıştırır.

## 🚀 Özellikler
- **Tamamen Yerel (Local):** Verileriniz bilgisayarınızdan çıkmaz. `Qwen 2.5-3B` modeli işlemci (CPU) üzerinde çalışır.
- **Özel Kişilik (Sera):** Model, LoRA (Low-Rank Adaptation) yöntemiyle eğitilmiş özel bir kişiliğe sahiptir.
- **Sesli Etkileşim:** `Faster-Whisper` ile yüksek doğrulukta duyma, `gTTS` ile doğal konuşma.
- **Sistem Kontrolü:** "Not defteri aç", "Hesap makinesi aç" gibi komutlarla bilgisayarı yönetme.
- **İnternet Araması:** DuckDuckGo motoru ile internetten bilgi çekip özetleme.
- **Web Arayüzü:** FastAPI ve WebSocket tabanlı, reaktif modern sohbet ekranı.

## 📂 Proje Yapısı
```text
📁 Sera_Asistan/
├── 📄 main.py            # 🧠 Ana Başlatıcı (FastAPI Sunucusu)
├── 📄 requirements.txt   # Kütüphane Listesi
├── 📂 core/              # Sistemin Organları
│   ├── 📄 llm.py         # Yapay Zeka Motoru (PyTorch + PEFT)
│   ├── 📄 audio.py       # Kulak ve Ağız (STT / TTS)
│   └── 📄 system.py      # Refleksler (PC Kontrol & Arama)
├── 📂 models/            # ⚠️ Model Dosyaları (GitHub'da Yoktur)
│   └── 📂 sera_adapter/  # Eğitilmiş LoRA Adaptör Dosyaları
└── 📂 templates/         # HTML Arayüzü
```
## ⚠️ Önemli Not (Model Dosyası)
Bu proje, çalışmak için özel eğitilmiş **Sera Adapter** modeline ihtiyaç duyar.
Model dosyaları boyut sınırları nedeniyle bu repoya eklenmemiştir.

Geliştirme süreci devam etmektedir. Modelin son hali hazır olduğunda Hugging Face üzerinden paylaşılacaktır.
Şu an çalıştırmak için kendi `adapter_model.safetensors` dosyanızı `models/sera_adapter/` klasörüne koymanız gerekir.


🛠️ Kurulum

1. Projeyi Klonlayın

git clone [https://github.com/Mirauiel/sesli-asistan.git](https://github.com/Mirauiel/sesli-asistan.git)

cd sesli-asistan

2. Sanal Ortamı Kurun (Önemli)

python3 -m venv venv

source venv/bin/activate  # Linux/Mac

# venv\Scripts\activate   # Windows

3. Gereksinimleri Yükleyin

Önemli: PyTorch'un CPU sürümünü kurmak için önce şu komutu çalıştırın:

pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)

Ardından diğer gereksinimleri kurun:

pip install -r requirements.txt

4. Sistem Araçlarını Yükleyin (Linux için)

Ses çalma ve işleme için gereklidir:

sudo apt update

sudo apt install mpg123 portaudio19-dev -y

5. Model Dosyası

Bu proje Qwen2.5-3B-Instruct temel modelini ve Sera Adaptörünü kullanır.

İlk çalıştırmada Temel Model (Base Model) otomatik indirilir.

Sera Adaptörü (models/sera_adapter) ise özel eğitim dosyasıdır. (Kendi adaptörünüzü models klasörüne koymalısınız).

Çalıştırma

python3 main.py

Tarayıcıdan http://localhost:8000 adresine gidin ve mikrofon butonuna basın.

Gereksinimler

OS: Linux (Ubuntu/Pop!_OS önerilir) veya Windows.

RAM: Minimum 8GB (CPU Modu için).

Python: 3.10 ve üzeri.

