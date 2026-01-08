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

```mermaid
graph LR
    A[Kullanıcı Sesi] --WebSocket--> B(FastAPI Server)
    B --Ses Verisi--> C{Faster-Whisper AI}
    C --Metin--> B
    B --Cevap--> D[Web Arayüzü]
    B --Loglama--> E[(SQLite Veritabanı)]

Tabi ki! Hem teknik açıdan dolu görünen hem de GitHub profilini ziyaret edenlerin "Vay be, mimariyi güzel kurmuş" diyeceği, sıfırdan ve hatasız bir README taslağı hazırladım.

Senin GitHub kullanıcı adına (Mirauiel) ve proje ismine (sesli-asistan) göre linkleri de tam olarak ayarladım.

Bunu kopyalayıp direkt yapıştırabilirsin:

Nasıl Uygulayacaksın?
nano README.md yazıp dosyayı aç.

CTRL + K tuşlarına basılı tutarak veya defalarca basarak içindeki her şeyi sil.

Aşağıdaki metni kopyala ve yapıştır.

CTRL + O -> Enter -> CTRL + X ile kaydet ve çık.

İşte Yeni README İçeriğin:
Markdown

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

```mermaid
graph LR
    A[Kullanıcı Sesi] --WebSocket--> B(FastAPI Server)
    B --Ses Verisi--> C{Faster-Whisper AI}
    C --Metin--> B
    B --Cevap--> D[Web Arayüzü]
    B --Loglama--> E[(SQLite Veritabanı)]


🛠️ Kurulum ve Çalıştırma
Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

1. Projeyi Klonlayın

git clone [https://github.com/Mirauiel/sesli-asistan.git](https://github.com/Mirauiel/sesli-asistan.git)
cd sesli-asistan

2. Sanal Ortamı Kurun (Tavsiye Edilen)

python3 -m venv venv
source venv/bin/activate

3. Gerekli Paketleri Yükleyin

pip install -r requirements.txt

Not: Linux kullanıcıları için ses işleme aracı gerekebilir:
sudo apt install ffmpeg libespeak1

4. Asistanı Başlatın 🚀

python3 server.py

Terminalde Uvicorn running on http://0.0.0.0:8000 yazısını gördüğünüzde tarayıcınızdan http://localhost:8000 adresine gidin.

🔮 Gelecek Planları (Roadmap)
[ ] Cross-Platform: Hem Windows hem Linux tam uyumluluğu.

[ ] LLM Entegrasyonu: Gemini/GPT veya Local LLM (Llama) ile doğal sohbet yeteneği.

[ ] Web Scraping: "Yemek tarifi bul" dendiğinde internetten veriyi çekip okuma.

[ ] IoT Kontrolü: Akıllı ev aletleri entegrasyonu.

🤝 İletişim & Geliştirici
Geliştirici: Utku Kalender (Mirauiel)

Bu proje, Bilgisayar Mühendisliği çalışmaları kapsamında geliştirilmektedir.
