import os
import time
import subprocess
from faster_whisper import WhisperModel
import speech_recognition as sr
from gtts import gTTS
from playsound3 import playsound

MODEL_SIZE = "small" 

print("\n--- SİSTEM BAŞLATILIYOR ---")
print("Model yükleniyor... (İlk seferde model indirileceği için 1-2 dk sürebilir)")

model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
print("✅ Model yüklendi! Hazırım.")

def speak(text):
    """Metni sese çevirir ve çalar"""
    print(f"🤖 Asistan: {text}")
    try:
        tts = gTTS(text=text, lang='tr')
        filename = "yanit.mp3"

        if os.path.exists(filename):
            os.remove(filename)
        tts.save(filename)

        playsound(filename)
    except Exception as e:
        print(f"Ses hatası: {e}")

def listen_and_transcribe():
    """Mikrofondan sesi dinler ve yazıya çevirir"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Dinliyorum... (Konuşabilirsin)")

        r.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("⏳ İşleniyor...")
            
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            segments, info = model.transcribe("temp.wav", beam_size=5, language="tr")
            full_text = "".join([segment.text for segment in segments]).strip()
            
            return full_text.lower()
        
        except sr.WaitTimeoutError:
            print("Ses algılanmadı.")
            return ""
        except Exception as e:
            print(f"Hata oluştu: {e}")
            return ""

def process_command(text):
    """Komutları işleyen beyin fonksiyonu"""
    if not text:
        return

    print(f"🗣️  Algılanan: {text}")

    if "hesap makinesi" in text:
        speak("Hesap makinesini açıyorum.")
        subprocess.Popen(['gnome-calculator']) 
    
    elif "nasılsın" in text:
        speak("Sistemlerim gayet stabil çalışıyor, teşekkürler. Sen nasılsın?")
        
    elif "saat kaç" in text or "saati söyle" in text:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        speak(f"Saat şu an {now}")
        
    elif "kapat" in text or "çıkış" in text:
        speak("Sistem kapatılıyor. İyi günler.")
        exit()
    
    else:
        speak("Bunu henüz anlayamadım ama öğreniyorum.")

if __name__ == "__main__":
    speak("Merhaba Utku, asistanın aktif.")
    while True:
        text = listen_and_transcribe()
        if text:
            process_command(text)
