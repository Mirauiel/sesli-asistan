# 🎙️ Türkçe Yapay Zeka Sesli Asistan (Local AI Assistant)

Bu proje, Python kullanılarak geliştirilmiş, **internet bağlantısına ihtiyaç duymadan (offline)** çalışabilen ve modern bir web arayüzü üzerinden kontrol edilen akıllı bir sesli asistandır.

Proje; hız, gizlilik ve düşük kaynak kullanımı (CPU Optimization) odaklı tasarlanmıştır.

## 🌟 Öne Çıkan Özellikler

* **⚡ Yüksek Performanslı STT:** `Faster-Whisper` modeli kullanılarak ve `int8 quantization` optimizasyonu yapılarak, GPU gerektirmeden CPU üzerinde şimşek hızında "Sesten Yazıya" çeviri.
* **🌐 Modern Mimari:** `FastAPI` ve `WebSocket` teknolojileri sayesinde "Request-Response" beklemesi olmadan gerçek zamanlı (Real-time) iletişim.
* **🔒 Tam Gizlilik:** Ses verileri dışarıya (Google/Amazon sunucularına) gönderilmez, tamamen yerel makinenizde işlenir.
* **💾 Akıllı Hafıza:** SQLite veritabanı entegrasyonu ile tüm konuşma geçmişini loglar ve hatırlar.
* **🖥️ Sistem Kontrolü:** İşletim sistemi komutlarını (Hesap makinesi açma, sistem durumu sorgulama vb.) sesle yönetebilme.

## 🏗️ Proje Mimarisi

```text
    [ Kullanıcı ]
         │
    (Sesli Komut)
         ▼
[ Web Arayüzü ] <─── WebSocket ───> [ Server (FastAPI) ]
                                          │    │
                                          │    ├───> [ Faster-Whisper AI ]
                                          │    │     (Sesi Yazıya Çevir)
                                          │    │
                                          │    └───> [ SQLite Veritabanı ]
                                          │          (Loglama Yap)
                                          │
                                          ▼
                                 [ İşletim Sistemi ]
                                 (Hesap Makinesi, Tarayıcı vb.)
```

🛠️ Kurulum ve Çalıştırma
Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

1. Projeyi Klonlayın

git clone https://github.com/Mirauiel/sesli-asistan.git

cd sesli-asistan

2. Sanal Ortamı Kurun (Tavsiye Edilen)
Kütüphanelerin sisteminizi etkilememesi için sanal ortam oluşturun:

python3 -m venv venv

source venv/bin/activate

3. Gerekli Paketleri Yükleyin

pip install -r requirements.txt

Not: Linux kullanıcıları için ses işleme aracı gerekebilir:

sudo apt install ffmpeg libespeak1

4. Asistanı Başlatın 🚀

python3 server.py

erminalde Uvicorn running on http://0.0.0.0:8000 yazısını gördüğünüzde tarayıcınızdan http://localhost:8000 adresine gidin.

🔮 Gelecek Planları (Roadmap)
[ ] Cross-Platform: Hem Windows hem Linux tam uyumluluğu.

[ ] LLM Entegrasyonu: Gemini/GPT veya Local LLM (Llama) ile doğal sohbet yeteneği.

[ ] Web Scraping: "Yemek tarifi bul" dendiğinde internetten veriyi çekip okuma.

[ ] IoT Kontrolü: Akıllı ev aletleri entegrasyonu.

🤝 İletişim & Geliştirici
Geliştirici: Utku Kalender (Mirauiel)

Bu proje, Bilgisayar Mühendisliği çalışmaları kapsamında geliştirilmektedir.
