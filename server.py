import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import sqlite3
import json
from faster_whisper import WhisperModel
import speech_recognition as sr
import os
import time
import platform
import subprocess
import webbrowser
from duckduckgo_search import DDGS  # YENİ: DuckDuckGo Kütüphanesi

# --- 1. AYARLAR VE MODEL YÜKLEME ---
app = FastAPI()

# İşletim Sistemi Tespiti
CURRENT_OS = platform.system()
print(f"🖥️  Algılanan İşletim Sistemi: {CURRENT_OS}")

# Veritabanı Bağlantısı
conn = sqlite3.connect("asistan.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_text TEXT,
    bot_response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Whisper Modelini Yükle (Int8 - CPU Optimize)
print("📥 Model yükleniyor (small, int8)...")
model = WhisperModel("small", device="cpu", compute_type="int8")
print("✅ Model hazır!")

# --- 2. YARDIMCI FONKSİYONLAR ---

def log_to_db(user_text, bot_response):
    """Konuşmayı veritabanına kaydeder."""
    cursor.execute("INSERT INTO logs (user_text, bot_response) VALUES (?, ?)", (user_text, bot_response))
    conn.commit()

def open_application(app_name):
    """İşletim sistemine göre doğru uygulamayı açar."""
    try:
        if CURRENT_OS == "Windows":
            if app_name == "hesap_makinesi":
                subprocess.Popen("calc.exe")
            elif app_name == "notepad":
                subprocess.Popen("notepad.exe")
            
        elif CURRENT_OS == "Linux":
            if app_name == "hesap_makinesi":
                subprocess.Popen(["gnome-calculator"])
            elif app_name == "gedit":
                subprocess.Popen(["gedit"])
        
        return True
    except Exception as e:
        print(f"❌ Uygulama açma hatası: {e}")
        return False

def listen_mic():
    """Mikrofonu dinler ve sesi metne çevirir."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Dinliyorum...")
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("⏳ İşleniyor...")
            
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            segments, _ = model.transcribe("temp.wav", beam_size=5, language="tr")
            text = " ".join([segment.text for segment in segments])
            
            if os.path.exists("temp.wav"):
                os.remove("temp.wav")
                
            return text

        except sr.WaitTimeoutError:
            print("timeout")
            return None
        except Exception as e:
            print(f"Hata: {e}")
            return None

# --- 3. ANA SUNUCU (WEBSOCKET) ---

@app.get("/")
async def get():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_text()
        
        if data == "start_listening":
            await websocket.send_json({"type": "info", "text": "Dinliyorum..."})
            
            text = listen_mic()
            
            if text:
                print(f"👤 Kullanıcı: {text}")
                await websocket.send_json({"type": "user", "text": text})
                
                response_text = ""
                text_lower = text.lower()
                
                # --- AKILLI KOMUT MERKEZİ ---
                
                # 1. Uygulama Açma Komutları
                if "hesap makinesi" in text_lower:
                    success = open_application("hesap_makinesi")
                    response_text = "Hesap makinesini açıyorum." if success else "Uygulamayı bulamadım."
                
                elif "not defteri" in text_lower or "notepad" in text_lower:
                    if CURRENT_OS == "Windows":
                        open_application("notepad")
                    else:
                        open_application("gedit")
                    response_text = "Not defterini açıyorum."

                # 2. İnternet Araması (DuckDuckGo - Güvenli ve Hızlı)
                elif "ara" in text_lower or "bul" in text_lower:
                    search_query = text_lower.replace("ara", "").replace("bul", "").replace("bana", "").strip()
                    
                    if search_query:
                        response_text = f"🦆 DuckDuckGo'da '{search_query}' aranıyor..."
                        await websocket.send_json({"type": "bot", "text": response_text})
                        
                        results = []
                        try:
                            # DuckDuckGo ile arama yap
                            ddgs = DDGS()
                            # max_results=3 ile ilk 3 sonucu al
                            ddg_results = ddgs.text(search_query, max_results=3)
                            
                            for r in ddg_results:
                                results.append({
                                    "title": r['title'],
                                    "url": r['href'],
                                    "desc": r['body']
                                })
                            
                            if not results:
                                response_text = "Maalesef sonuç bulamadım."
                            else:
                                await websocket.send_json({"type": "search_results", "data": results})
                            
                        except Exception as e:
                            print(f"Arama hatası: {e}")
                            await websocket.send_json({"type": "bot", "text": "Arama sırasında bağlantı hatası oluştu."})
                            
                    else:
                        response_text = "Ne aramam gerektiğini anlamadım."
                        await websocket.send_json({"type": "bot", "text": response_text})

                # 3. Sohbet / Durum
                elif "nasılsın" in text_lower:
                    response_text = "Sistemlerim %100 çalışıyor, teşekkürler!"
                elif "saat kaç" in text_lower:
                    from datetime import datetime
                    now = datetime.now().strftime("%H:%M")
                    response_text = f"Saat şu an {now}"
                
                else:
                    response_text = "Bunu henüz öğrenmedim ama kaydediyorum."

                # Cevabı Gönder ve Kaydet (Arama kartı gönderilmediyse)
                if response_text and not response_text.startswith("🦆"):
                    log_to_db(text, response_text)
                    await websocket.send_json({"type": "bot", "text": response_text})

# --- 4. BAŞLATMA ---
if __name__ == "__main__":
    import uvicorn
    print("🚀 Sunucu başlatılıyor: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
