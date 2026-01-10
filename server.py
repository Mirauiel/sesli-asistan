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
from thefuzz import fuzz
import ollama  # YENİ: Beyin Kütüphanesi

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
print("📥 Whisper Modeli yükleniyor (small, int8)...")
model = WhisperModel("small", device="cpu", compute_type="int8")
print("✅ Whisper Modeli hazır!")

# --- 2. YARDIMCI FONKSİYONLAR ---

def ask_llm(text):
    """Qwen 2.5 (3B) - Ciddi ve Teknik Mod"""
    print(f"🧠 LLM Düşünüyor: {text}")
    try:
        response = ollama.chat(model='qwen2.5:3b', messages=[
            {
                'role': 'system', 
    		'content': (
        	"Kullanıcının adı Utku. Sen onun akıllı ve yardımsever yapay zeka asistanısın. "
        	"Kurallar: "
        	"1. Her zaman TÜRKÇE konuş. Asla Çince (Kanji), Japonca veya Kiril alfabesi kullanma. "
        	"2. Cevapların kısa, net ve bilgi odaklı olsun. "
        	"3. Matematik ve tarih sorularında kesin ol. "
        	"4. Kendinden bahsederken 'Ben bir Yapay Zeka Asistanıyım' de."
    		)
            },
            {
                'role': 'user', 
                'content': text
            },
        ], options={'temperature': 0.1}) # Temperature'ı 0.1 yaptık (Daha robotik ve kesin olsun diye)
        return response['message']['content']
    except Exception as e:
        print(f"LLM Hatası: {e}")
        return "Beynimde bir hata oluştu."

def check_similarity(user_text, command_key):
    ratio = fuzz.partial_ratio(user_text.lower(), command_key.lower())
    return ratio >= 75

def speak_thread(text):
    try:
        tts = gTTS(text=text, lang='tr')
        filename = "yanit.mp3"
        if os.path.exists(filename): os.remove(filename)
        tts.save(filename)
        time.sleep(0.2)
        os.system(f"mpg123 -q --buffer 1024 {filename}")
        if os.path.exists(filename): os.remove(filename)
    except Exception as e:
        print(f"🔊 Ses Hatası: {e}")

def speak(text):
    t = threading.Thread(target=speak_thread, args=(text,), daemon=True)
    t.start()

def log_to_db(user_text, bot_response):
    cursor.execute("INSERT INTO logs (user_text, bot_response) VALUES (?, ?)", (user_text, bot_response))
    conn.commit()

def open_application(app_name):
    try:
        if CURRENT_OS == "Windows":
            if app_name == "hesap_makinesi": subprocess.Popen("calc.exe")
            elif app_name == "notepad": subprocess.Popen("notepad.exe")
        elif CURRENT_OS == "Linux":
            if app_name == "hesap_makinesi": subprocess.Popen(["gnome-calculator"])
            elif app_name == "gedit": subprocess.Popen(["gedit"])
        return True
    except:
        return False

def listen_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Dinliyorum...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
            print("⏳ Ses işleniyor...")
            with open("temp.wav", "wb") as f: f.write(audio.get_wav_data())
            segments, _ = model.transcribe("temp.wav", beam_size=5, language="tr", initial_prompt="merhaba asistan nasılsın saat kaç")
            text = " ".join([segment.text for segment in segments])
            if os.path.exists("temp.wav"): os.remove("temp.wav")
            return text
        except:
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
                
                # --- AKILLI KOMUT MERKEZİ ---
                
                # 1. Uygulama Açma
                if check_similarity(text_lower, "hesap makinesi aç") or "hesap" in text_lower:
                    open_application("hesap_makinesi")
                    response_text = "Hesap makinesi açıldı."
                    speak_text = response_text
                
                elif check_similarity(text_lower, "not defteri aç"):
                    open_application("gedit")
                    response_text = "Not defteri açıldı."
                    speak_text = response_text

                # 2. İnternet Araması (Özel Tetikleyici: "Ara", "Bul")
                elif "ara" in text_lower or "bul" in text_lower:
                    search_query = text_lower.replace("ara", "").replace("bul", "").replace("bana", "").strip()
                    if search_query:
                        response_text = f"🦆 DuckDuckGo: '{search_query}'"
                        speak_text = f"{search_query} için bulduklarım."
                        await websocket.send_json({"type": "bot", "text": response_text})
                        speak(speak_text)
                        
                        try:
                            ddgs = DDGS()
                            ddg_results = ddgs.text(search_query, max_results=3)
                            results = [{"title": r['title'], "url": r['href'], "desc": r['body']} for r in ddg_results]
                            if results:
                                await websocket.send_json({"type": "search_results", "data": results})
                            else:
                                await websocket.send_json({"type": "bot", "text": "Sonuç bulunamadı."})
                        except:
                            pass
                        speak_text = "" # Tekrar okumasın

                # 3. Basit Durumlar
                elif check_similarity(text_lower, "saat kaç"):
                    from datetime import datetime
                    now = datetime.now().strftime("%H:%M")
                    response_text = f"Saat şu an {now}"
                    speak_text = response_text
                
                # 4. YENİ: LLM ENTEGRASYONU (Her Şeyin Cevabı) 🧠
                else:
                    # Kullanıcıya düşündüğünü söyle
                    await websocket.send_json({"type": "info", "text": "🤔 Düşünüyorum..."})
                    
                    # Ollama'ya sor
                    llm_response = ask_llm(text)
                    
                    response_text = llm_response
                    speak_text = llm_response

                # Cevabı Gönder ve Oku
                if response_text and not response_text.startswith("🦆"):
                    log_to_db(text, response_text)
                    await websocket.send_json({"type": "bot", "text": response_text})
                
                if speak_text:
                    speak(speak_text)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
