import os
import speech_recognition as sr
from faster_whisper import WhisperModel
import threading
import sys
import subprocess
from ctypes import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# --- ALSA HATALARINI GİZLEME (LİNUX İÇİN) ---
# Bu blok terminaldeki gereksiz kırmızı yazıları engeller
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

try:
    model = WhisperModel(
        config.WHISPER_MODEL_SIZE, 
        device=config.WHISPER_DEVICE, 
        compute_type=config.WHISPER_COMPUTE,
        download_root=None,
        local_files_only=True
    )
    print("✅ Whisper (Kulak) Hazır! (Offline Mod)")
except Exception as e:
    print(f"⚠️ HATA: Model bulunamadı! İlk kez çalıştırıyorsan 'local_files_only=False' yapman gerekebilir. Hata: {e}")
    model = WhisperModel(config.WHISPER_MODEL_SIZE, device=config.WHISPER_DEVICE, compute_type=config.WHISPER_COMPUTE)

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

def piper_speak(text, output_file):
    """
    Piper TTS kullanarak tamamen offline ses üretir.
    DFKI (tr_TR-dfki-medium.onnx) modelini kullanır.
    """
    piper_binary = os.path.join(config.BASE_DIR, "piper_tts", "piper", "piper")
    
    model_path = os.path.join(config.BASE_DIR, "piper_tts", "tr_TR-dfki-medium.onnx")
    
    if not os.path.exists(piper_binary):
        print(f"❌ HATA: Piper programı bulunamadı: {piper_binary}")
        return
    if not os.path.exists(model_path):
        print(f"❌ HATA: Ses modeli bulunamadı: {model_path}")
        return

    try:
        command = [
            piper_binary,
            "--model", model_path,
            "--output_file", output_file
        ]
        
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
        
    except Exception as e:
        print(f"⚠️ Piper Hatası: {e}")

def speak_thread(text):
    output_file = os.path.join(config.BASE_DIR, "yanit.wav")
    
    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        piper_speak(text, output_file)
        
        if os.path.exists(output_file):
            os.system(f"aplay -q {output_file}")
        else:
            print("❌ Ses dosyası oluşturulamadı.")
            
    except Exception as e:
        print(f"🔊 Ses Oynatma Hatası: {e}")

def speak(text):
    t = threading.Thread(target=speak_thread, args=(text,), daemon=True)
    t.start()
