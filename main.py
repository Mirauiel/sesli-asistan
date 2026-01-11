import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import os

# --- MODÜLLERİMİZİ ÇAĞIRIYORUZ ---
import config
from core import audio, llm, system

# (Hafıza modülünü sonra ekleyeceğiz, şimdilik yorum satırı)
# from core import memory 

app = FastAPI()

@app.get("/")
async def get():
    # HTML Dosyasını Yükle
    template_path = os.path.join(config.BASE_DIR, "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        # Frontend'den mesaj bekle
        data = await websocket.receive_text()
        
        if data == "start_listening":
            await websocket.send_json({"type": "info", "text": "Dinliyorum..."})
            
            # 1. ADIM: KULAK (Duyma)
            user_text = audio.listen_mic()
            
            if user_text:
                print(f"👤 Kullanıcı: {user_text}")
                await websocket.send_json({"type": "user", "text": user_text})
                
                response_text = ""
                speak_text = ""
                text_lower = user_text.lower()
                
                # 2. ADIM: SİSTEM KONTROLÜ (Komut mu?)
                
                # Hesap Makinesi
                if system.check_similarity(text_lower, "hesap makinesi aç"):
                    response_text = system.open_application("hesap_makinesi")
                    speak_text = response_text
                
                # Not Defteri
                elif system.check_similarity(text_lower, "not defteri aç"):
                    response_text = system.open_application("notepad")
                    speak_text = response_text
                
                # İnternet Araması (Örn: "Python nedir ara")
                elif "ara" in text_lower or "bul" in text_lower:
                    query = text_lower.replace("ara", "").replace("bul", "").replace("bana", "").strip()
                    if query:
                        await websocket.send_json({"type": "info", "text": "🔎 İnternette aranıyor..."})
                        results = system.search_web(query)
                        
                        if results:
                            # Sonuçları karta bas
                            await websocket.send_json({"type": "search_results", "data": results})
                            response_text = f"'{query}' için bulduklarım ekranda."
                            speak_text = "Bulduklarımı ekrana getirdim."
                        else:
                            response_text = "Maalesef internette bir şey bulamadım."
                            speak_text = response_text

                # 3. ADIM: BEYİN (Yapay Zeka Sohbeti)
                else:
                    await websocket.send_json({"type": "info", "text": "🧠 Düşünüyorum..."})
                    
                    # Şimdilik hafızasız soruyoruz (Bir sonraki aşamada burası değişecek)
                    llm_response = llm.ask_llm(user_text)
                    
                    response_text = llm_response
                    speak_text = llm_response

                # 4. ADIM: AĞIZ (Cevap ve Seslendirme)
                if response_text:
                    await websocket.send_json({"type": "bot", "text": response_text})
                
                if speak_text:
                    audio.speak(speak_text)

if __name__ == "__main__":
    print(f"🚀 Asistan Başlatılıyor... (Model: {config.LLM_MODEL})")
    uvicorn.run(app, host="0.0.0.0", port=8000)
