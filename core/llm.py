import ollama
import sys
import os
import datetime

# Config dosyasını çekelim
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def ask_llm(text, context=""):
    print(f"🧠 LLM Düşünüyor: {text}")
    
    # 1. ZAMANI AL (Hatanın sebebi bu satırın eksik olmasıydı)
    now = datetime.datetime.now()
    # Örn: "11 Ocak 2026, Saat 19:45" formatında
    tarih_saat = now.strftime("%d %B %Y, Saat %H:%M")
    
    # 2. SİSTEM MESAJI (Sadeleştirilmiş Hali)
    system_prompt = (
        f"Şu anki tarih ve saat: {tarih_saat}\n"
        "Senin adın Jarvis. Kullanıcının adı Utku.\n"
        "Sen yardımsever bir yapay zeka asistanısın.\n"
        "Kurallar:\n"
        "1. Çok kısa ve düzgün Türkçe cümleler kur.\n"
        "2. Felsefe yapma, sadece soruya cevap ver.\n"
        "3. Kullanıcıya her zaman 'Utku' diye hitap et."
    )
    
    # Eğer hafıza veya internet sonucu varsa ekle
    if context:
        system_prompt += f"\n\nEK BİLGİ:\n{context}"

    try:
        response = ollama.chat(model=config.LLM_MODEL, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': text},
        ], options={'temperature': 0.1}) 
        
        return response['message']['content']
    
    except Exception as e:
        print(f"❌ LLM Hatası: {e}")
        return "Beynimde geçici bir sorun var."
