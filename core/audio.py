import os
import time
import speech_recognition as sr
from faster_whisper import WhisperModel
from gtts import gTTS
import threading
import sys

# Config dosyasını çekelim
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# --- 1. MODELİ YÜKLE ---
print("📥 Whisper Modeli yükleniyor...")
# Config'deki ayarları kullanıyoruz
model = WhisperModel(
    config.WHISPER_MODEL_SIZE, 
    device=config.WHISPER_DEVICE, 
    compute_type=config.WHISPER_COMPUTE
)
print("✅ Whisper (Kulak) Hazır!")

# --- 2. DİNLEME FONKSİYONU ---
def listen_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Dinliyorum...")
        try:
            # 5 saniye bekle, konuşma başlarsa en fazla 6 saniye dinle
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
            print("⏳ Ses işleniyor...")
            
            # Geçici dosya oluştur
            temp_wav = os.path.join(config.BASE_DIR, "temp.wav")
            with open(temp_wav, "wb") as f:
                f.write(audio.get_wav_data())
            
            # Whisper ile yazıya çevir
            segments, _ = model.transcribe(temp_wav, beam_size=5, language="tr")
            text = " ".join([segment.text for segment in segments])
            
            # Temizlik
            if os.path.exists(temp_wav): os.remove(temp_wav)
            
            return text
        except Exception as e:
            # Ses yoksa veya hata varsa sessizce dön
            return None

# --- 3. KONUŞMA FONKSİYONU (TTS) ---
def speak_thread(text):
    try:
        # Dosya yolunu ayarla
        output_file = os.path.join(config.BASE_DIR, "yanit.mp3")
        
        # Eğer eski dosya varsa sil (Çakışmayı önle)
        if os.path.exists(output_file):
            os.remove(output_file)
            
        tts = gTTS(text=text, lang=config.TTS_LANG)
        tts.save(output_file)
        
        # Linux ses komutu (mpg123)
        # -q: sessiz mod (terminale yazı basmaz)
        os.system(f"mpg123 -q --buffer 1024 {output_file}")
        
    except Exception as e:
        print(f"🔊 Ses Hatası: {e}")

def speak(text):
    # Konuşmayı arkaplanda yap ki sistem donmasın
    t = threading.Thread(target=speak_thread, args=(text,), daemon=True)
    t.start()
