import os
import datetime
import sys
from llama_cpp import Llama

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class LLMEngine:
    def __init__(self):
        print("\n⚙️  Sera AI Motoru (GGUF/CPU) Yükleniyor... Lütfen bekleyin.")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, "models", "sera_v2.gguf") 
        
        if not os.path.exists(self.model_path):
            print(f"❌ HATA: Model dosyası bulunamadı: {self.model_path}")
            sys.exit(1)

        try:
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=4096,
                n_threads=6,
                n_batch=512,
                verbose=False
            )
            print("✅ Sera (GGUF) Hazır ve Çok Hızlı!\n")
        except Exception as e:
            print(f"❌ Model Yükleme Hatası: {e}")
            raise e

    def generate_response(self, user_input, context=""):
        now = datetime.datetime.now()
        tarih_saat = now.strftime("%d %B %Y, Saat %H:%M")

        system_prompt = (
            f"Şu anki tarih: {tarih_saat}.\n"
            "Senin adın Sera. Utku Kalender tarafından geliştirilen, yerel ağda çalışan asistanımsın.\n"
            "Sorulara kısa, net ve yardımsever Türkçe cevaplar ver.\n"
            "ASLA hashtag (#), etiket listesi veya gereksiz emoji yığını kullanma."
        )

        if context:
            system_prompt += f"\n\nGEÇMİŞ KONUŞMALAR:\n{context}"

        prompt = f"""<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{user_input}<|im_end|>
<|im_start|>assistant
"""

        try:
            output = self.model(
                prompt,
                max_tokens=250,
                stop=["<|im_end|>", "User:", "Utku:"],
                temperature=0.6,
                top_p=0.9,
                echo=False
            )
            
            response = output["choices"][0]["text"].strip()
            
            response = response.replace("Intel", "Utku Kalender")
            response = response.replace("OpenAI", "Utku Kalender")
            
            return response
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            return "Beynimde anlık bir işlem hatası oluştu Utku."

if __name__ == "__main__":
    motor = LLMEngine()
    start = datetime.datetime.now()
    print("Sera:", motor.generate_response("Merhaba, nasılsın?"))
    end = datetime.datetime.now()
    print(f"Süre: {(end-start).total_seconds()} saniye")
