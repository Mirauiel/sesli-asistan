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
import threading
from duckduckgo_search import DDGS
from gtts import gTTS
from thefuzz import fuzz  # YENİ: Bulanık Mantık Kütüphanesi

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

def check_similarity(user_text, command_key):
    """
    Kullanıcının söylediği ile komut arasındaki benzerliği ölçer.
    Örnek: "Sadkaç" ile "saat kaç" -> %85 Benzer -> True döner.
    """
    ratio = fuzz.partial_ratio(user_text.lower(), command_key.lower())
    return ratio >= 75  # %75 ve üzeri benzerliği kabul et

def speak_thread(text):
    """Sesi arka planda oluşturur ve çalar (Optimize Edilmiş Versiyon)."""
    try:
        tts = gTTS(text=text, lang='tr')
        filename = "yanit.mp3"
        
        # Eski dosya varsa sil
        if os.path.exists(filename):
            os.remove(filename)
            
        tts.save(filename)
        
        # KRİTİK AYAR 1: Dosya yazma işlemi bitene kadar minik bir bekleme
        time.sleep(0.2) 
        
        # KRİTİK AYAR 2: --buffer komutu ile takılmayı önle
        # -q: Sessiz mod, --buffer 1024: Ön bellek
        os.system(f"mpg123 -q --buffer 1024 {filename}")
        
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"🔊 Ses Hatası: {e}")

def speak(text):
    # daemon=True: Program kapanırsa bu thread'i bekleme, direkt kapat.
    t = threading.Thread(target=speak_thread, args=(text,), daemon=True)
    t.start()

def log_to_db(user_text, bot_response):
    cursor.execute("INSERT INTO logs (user_text, bot_response) VALUES (?, ?)", (user_text, bot_response))
    conn.commit()

def open_application(app_name):
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
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Gürültü ayarını biraz kıstık, çok bekletmesin
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Dinliyorum...")
        
        try:
            # phrase_time_limit=5: Kullanıcıyı çok uzun dinleyip beklemesin
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("⏳ İşleniyor...")
            
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            # initial_prompt: Modele "Kopya" veriyoruz. Bu kelimeleri bekle diyoruz.
            segments, _ = model.transcribe(
                "temp.wav", 
                beam_size=5, 
                language="tr",
                initial_prompt="merhaba asistan nasılsın saat kaç hesap makinesi not defteri ara bul youtube google"
            )
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
                speak_text = ""
                text_lower = text.lower()
                
                # --- AKILLI KOMUT MERKEZİ (ARTIK DAHA ZEKİ 🧠) ---
                
                # 1. Uygulama Açma (Fuzzy Logic ile)
                if check_similarity(text_lower, "hesap makinesi aç") or "hesap" in text_lower:
                    success = open_application("hesap_makinesi")
                    response_text = "Hesap makinesini açıyorum." if success else "Uygulamayı bulamadım."
                    speak_text = response_text
                
                elif check_similarity(text_lower, "not defteri aç") or "notepad" in text_lower:
                    if CURRENT_OS == "Windows":
                        open_application("notepad")
                    else:
                        open_application("gedit")
                    response_text = "Not defterini açıyorum."
                    speak_text = response_text

                # 2. İnternet Araması (DuckDuckGo)
                # 'ara' kelimesi kısa olduğu için fuzzy yerine 'in' kullanmak daha güvenli
                elif "ara" in text_lower or "bul" in text_lower:
                    search_query = text_lower.replace("ara", "").replace("bul", "").replace("bana", "").strip()
                    
                    if search_query:
                        response_text = f"🦆 DuckDuckGo'da '{search_query}' aranıyor..."
                        speak_text = f"{search_query} için bulduğum sonuçlar."
                        
                        await websocket.send_json({"type": "bot", "text": response_text})
                        speak(speak_text)
                        
                        results = []
                        try:
                            ddgs = DDGS()
                            ddg_results = ddgs.text(search_query, max_results=3)
                            
                            for r in ddg_results:
                                results.append({
                                    "title": r['title'],
                                    "url": r['href'],
                                    "desc": r['body']
                                })
                            
                            if not results:
                                response_text = "Sonuç bulamadım."
                            else:
                                await websocket.send_json({"type": "search_results", "data": results})
                            
                        except Exception as e:
                            print(f"Arama hatası: {e}")
                            await websocket.send_json({"type": "bot", "text": "Arama hatası."})
                        
                        speak_text = "" 

                    else:
                        response_text = "Ne aramam gerektiğini anlamadım."
                        speak_text = response_text

                # 3. Sohbet / Durum (Fuzzy Logic ile)
                elif check_similarity(text_lower, "nasılsın"):
                    response_text = "Sistemlerim %100 çalışıyor, teşekkürler!"
                    speak_text = response_text
                
                elif check_similarity(text_lower, "saat kaç") or "saat" in text_lower:
                    from datetime import datetime
                    now = datetime.now().strftime("%H:%M")
                    response_text = f"Saat şu an {now}"
                    speak_text = response_text
                
                else:
                    response_text = "Bunu henüz öğrenmedim ama kaydediyorum."
                    speak_text = "Bunu henüz bilmiyorum."

                if response_text and not response_text.startswith("🦆"):
                    log_to_db(text, response_text)
                    await websocket.send_json({"type": "bot", "text": response_text})
                
                if speak_text:
                    speak(speak_text)

# --- 4. BAŞLATMA ---
if __name__ == "__main__":
    import uvicorn
    print("🚀 Sunucu başlatılıyor: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
