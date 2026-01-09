import uvicorn
import os
import sys

def start_server():
    """
    Modern Sesli Asistan Başlatıcısı
    Bu script, server.py dosyasındaki FastAPI uygulamasını ayağa kaldırır.
    """
    print("\n🚀 SİSTEM BAŞLATILIYOR...")
    print("📂 Dosyalar kontrol ediliyor: server.py, templates/index.html")
    
    # Sunucuyu başlat (server dosyasındaki 'app' nesnesini çalıştır)
    # reload=True: Kodu değiştirdiğinde sunucuyu otomatik yeniler (Geliştirici dostu)
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n🛑 Sistem kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {e}")

if __name__ == "__main__":
    start_server()
