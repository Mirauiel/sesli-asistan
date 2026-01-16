import os
import speech_recognition as sr
from faster_whisper import WhisperModel
import threading
import sys
import asyncio
import edge_tts
from ctypes import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# --- ALSA HATALARINI GİZLEME BLOĞU (LİNUX İÇİN) ---
# Bu blok, terminali kirleten "ALSA lib pcm.c..." hatalarını susturur.
# Eğer kütüphane bulunamazsa program çökmez, sadece susturma özelliği devre dışı kalır.
try:
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
    def py_error_handler(filename, line, function, err, fmt):
        pass
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    
    try:
        asound = cdll.LoadLibrary('libasound.so.2')
    except OSError:
        asound = cdll.LoadLibrary('libasound.so')
        
    asound.snd_lib_error_set_handler(c_error_handler)
except Exception:
    pass

print("📥 Whisper Modeli yükleniyor...")
model = WhisperModel(config.WHISPER_MODEL_SIZE, device=config.WHISPER_DEVICE, compute_type=config.WHISPER_COMPUTE)
print("✅ Whisper (Kulak) Hazır!")

def listen_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Dinliyorum...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("⏳ Ses işleniyor...")
            
            temp_wav = os.path.join(config.BASE_DIR, "temp.wav")
            with open(temp_wav, "wb") as f:
                f.write(audio.get_wav_data())
            
            segments, _ = model.transcribe(temp_wav, beam_size=5, language="tr")
            text = " ".join([segment.text for segment in segments])
            
            if os.path.exists(temp_wav): os.remove(temp_wav)
            return text
        except Exception:
            return None

async def generate_audio(text, output_file):
    communicate = edge_tts.Communicate(text, "tr-TR-NeslihanNeural")
    await communicate.save(output_file)

def speak_thread(text):
    try:
        output_file = os.path.join(config.BASE_DIR, "yanit.mp3")
        
        if os.path.exists(output_file):
            os.remove(output_file)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate_audio(text, output_file))
        loop.close()
        
        os.system(f"mpg123 -q --buffer 1024 {output_file}")
        
    except Exception as e:
        print(f"🔊 Ses Hatası: {e}")

def speak(text):
    t = threading.Thread(target=speak_thread, args=(text,), daemon=True)
    t.start()
