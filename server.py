from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import subprocess
from faster_whisper import WhisperModel
import speech_recognition as sr
from gtts import gTTS
from playsound3 import playsound
import os
import asyncio
import sqlite3
import datetime

# --- AYARLAR ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")
MODEL_SIZE = "small"

print("Model yükleniyor...")
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
print("Model hazır!")

# --- VERİTABANI BAĞLANTISI ---
conn = sqlite3.connect("asistan_logs.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS konusma_gecmisi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarih TEXT,
        komut TEXT,
        cevap TEXT
    )
""")
conn.commit()

def log_to_db(komut, cevap):
    """Konuşmayı veritabanına kaydeder"""
    zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO konusma_gecmisi (tarih, komut, cevap) VALUES (?, ?, ?)", (zaman, komut, cevap))
    conn.commit()

def speak(text):
    """Metni sese çevirir"""
    try:
        tts = gTTS(text=text, lang='tr')
        filename = "yanit.mp3"
        if os.path.exists(filename): os.remove(filename)
        tts.save(filename)
        playsound(filename)
    except:
        pass

def listen_mic():
    """Mikrofonu dinler"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())
            segments, _ = model.transcribe("temp.wav", beam_size=5, language="tr")
            return "".join([s.text for s in segments]).strip().lower()
        except:
            return ""

# --- ENDPOINTLER ---

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_text()
        
        if data == "start_listening":
            await websocket.send_json({"type": "info", "text": "Dinliyorum..."})
            text = listen_mic()
            
            if text:
                await websocket.send_json({"type": "user", "text": text})
                
                response_text = ""
                
                # --- KOMUTLAR ---
                if "hesap makinesi" in text:
                    response_text = "Hesap makinesini açıyorum."
                    subprocess.Popen(['gnome-calculator'])
                
                elif "sistem durumu" in text or "bilgisayar nasıl" in text:
                    # Linux'ta yük durumunu okuma
                    load1, load5, load15 = os.getloadavg()
                    response_text = f"İşlemci yükü şu an yüzde {int(load1 * 100)} seviyesinde. Sistem stabil."

                elif "nasılsın" in text:
                    response_text = "İyiyim, tüm servislerim aktif."
                    
                elif "saat kaç" in text:
                    now = datetime.datetime.now().strftime("%H:%M")
                    response_text = f"Saat şu an {now}"
                    
                else:
                    response_text = "Bunu tam anlayamadım, tekrar eder misin?"

                # --- CEVAP VE LOGLAMA ---
                # 1. Veritabanına kaydet
                log_to_db(text, response_text)
                
                # 2. Arayüze gönder ve seslendir
                await websocket.send_json({"type": "bot", "text": response_text})
                speak(response_text)
            else:
                await websocket.send_json({"type": "info", "text": "Ses algılanamadı."})
                await websocket.send_json({"type": "bot", "text": "Bir şey duyamadım."})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
