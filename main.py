import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import os
import sys

import config
from core import audio, llm, system

print("🚀 Sistem Başlatılıyor...")
try:
    sera = llm.LLMEngine()
except Exception as e:
    print(f"💥 Kritik Hata: Yapay Zeka Modeli Yüklenemedi! detay: {e}")
    sys.exit(1)

app = FastAPI()

@app.get("/")
async def get():
    template_path = os.path.join(config.BASE_DIR, "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        try:
            data = await websocket.receive_text()
        except Exception:
            break
        
        if data == "start_listening":
            await websocket.send_json({"type": "info", "text": "Dinliyorum..."})
            
            user_text = audio.listen_mic()
            
            if user_text:
                print(f"👤 Kullanıcı: {user_text}")
                await websocket.send_json({"type": "user", "text": user_text})
                
                response_text = ""
                speak_text = ""
                text_lower = user_text.lower()
                
                
                if system.check_similarity(text_lower, "hesap makinesi aç"):
                    response_text = system.open_application("hesap_makinesi")
                    speak_text = response_text
                
                elif system.check_similarity(text_lower, "not defteri aç"):
                    response_text = system.open_application("notepad")
                    speak_text = response_text
                
                elif "ara" in text_lower or "bul" in text_lower:
                    query = text_lower.replace("ara", "").replace("bul", "").replace("bana", "").strip()
                    if query:
                        await websocket.send_json({"type": "info", "text": "🔎 İnternette aranıyor..."})
                        results = system.search_web(query)
                        
                        if results:
                            await websocket.send_json({"type": "search_results", "data": results})
                            response_text = f"'{query}' için bulduklarım ekranda."
                            speak_text = "Bulduklarımı ekrana getirdim."
                        else:
                            response_text = "Maalesef internette bir şey bulamadım."
                            speak_text = response_text

                else:
                    await websocket.send_json({"type": "info", "text": "🧠 Sera Düşünüyor..."})
                    
                    llm_response = sera.generate_response(user_text)
                    
                    response_text = llm_response
                    speak_text = llm_response

                if response_text:
                    await websocket.send_json({"type": "bot", "text": response_text})
                
                if speak_text:
                    audio.speak(speak_text)

if __name__ == "__main__":
    print(f"🌍 Web Arayüzü: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
