import json
import random
import os


INPUT_FILE = "dataset.jsonl"
OUTPUT_FILE = "dataset_1k.jsonl"
TARGET_COUNT = 1000


actions = ["nasıl kurulur?", "nasıl silinir?", "nasıl güncellenir?", "versiyonuna nasıl bakılır?", "durumu nasıl kontrol edilir?"]
packages = ["python3", "docker", "git", "vim", "nano", "htop", "curl", "wget", "nginx", "ufw", "openssh-server", "ffmpeg"]
python_tasks = ["bir liste oluştur", "bir fonksiyon tanımla", "dosya okuma yap", "json verisi işle", "bir sınıf oluştur", "hata yakalama yap"]
system_cmds = ["Sesi aç", "Sesi kapat", "Ekran parlaklığını artır", "Wifi'yi kapat", "Bilgisayarı kilitle"]
iot_devices = ["Salon ışığını", "Mutfak lambasını", "Klimayı", "Televizyonu", "Akıllı prizi"]
iot_states = ["aç", "kapat", "durumu nedir?", "yüzde 50 yap", "rengini kırmızı yap"]
greetings = ["Selam Sera", "Günaydın", "İyi akşamlar", "Hey Sera", "Merhaba", "Selamlar"]

def generate_linux():
    pkg = random.choice(packages)
    action = random.choice(actions)
    return {"instruction": f"Linux'ta {pkg} paketi {action}", "input": "", "output": f"Komut: `sudo apt install {pkg}` veya ilgili komut."}

def generate_python():
    task = random.choice(python_tasks)
    return {"instruction": f"Python ile {task}.", "input": "", "output": "Python dokümantasyonuna bakabilirsin."}

def generate_system():
    cmd = random.choice(system_cmds)
    return {"instruction": f"{cmd}.", "input": "", "output": "Tamam, işlem yapılıyor."}

def generate_iot():
    dev = random.choice(iot_devices)
    state = random.choice(iot_states)
    return {"instruction": f"{dev} {state}.", "input": "", "output": "Cihaz güncellendi."}

def generate_chat():
    greet = random.choice(greetings)
    return {"instruction": f"{greet}.", "input": "", "output": "Selam Utku!"}

dataset = []

if os.path.exists(INPUT_FILE):
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip(): dataset.append(json.loads(line))
    print(f"✅ Orijinal veri: {len(dataset)} adet.")

current_count = len(dataset)
needed = TARGET_COUNT - current_count

print(f"⚙️ {needed} adet sentetik veri üretiliyor...")

for i in range(needed):
    cat = random.choice([generate_linux, generate_python, generate_system, generate_iot, generate_chat])
    dataset.append(cat())

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for entry in dataset:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")

print(f"🎉 BİTTİ! Toplam {len(dataset)} satır hazır.")
