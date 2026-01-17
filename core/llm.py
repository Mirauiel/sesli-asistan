import os
import sys
import datetime
from llama_cpp import Llama

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class LLMEngine:
    def __init__(self):
        print("\n⚙️  Sera AI Motoru (GGUF) Yükleniyor...")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, "models", "sera_v2.gguf") 
        
        if not os.path.exists(self.model_path):
            print(f"❌ HATA: Model bulunamadı: {self.model_path}")
            sys.exit(1)

        try:
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=4096,
                n_threads=6,
                n_batch=512,
                verbose=False
            )
            print("✅ Sera Zihni Açıldı!\n")
        except Exception as e:
            print(f"❌ Model Yükleme Hatası: {e}")
            raise e

    def generate_response(self, user_input, context=""):
        now = datetime.datetime.now()
        tarih_saat = now.strftime("%d %B %Y, Saat %H:%M")

        system_prompt = (
            f"Tarih: {tarih_saat}.\n"
            "Senin adın Sera. Sen Türkçe konuşan, zeki, yardımsever ve kibar bir yapay zeka asistanısın.\n"
            "Kullanıcının adı Utku Kalender.\n"
            "Kurallar:\n"
            "1. Sadece Türkçe cevap ver. Asla İngilizce kelime kullanma.\n"
            "2. Cevapların kısa, net ve anlaşılır olsun.\n"
            "3. Gramer kurallarına uy. 'Ben Sera'sın' deme, 'Ben Sera'yım' de.\n"
            "4. Kullanıcı 'Benim adım ne?' derse 'Senin adın Utku' de.\n"
            "5. Halüsinasyon görme, uydurma kelimeler kullanma."
        )

        if context:
            system_prompt += f"\n\nGeçmiş Konuşmalar:\n{context}"

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
                stop=["<|im_end|>", "User:", "Utku:", "Sistem:"], 
                temperature=0.1,
                top_p=0.9,
                repeat_penalty=1.1,
                echo=False
            )
            
            response = output["choices"][0]["text"].strip()
            
            response = response.replace("Sera'sın", "Sera'yım")
            response = response.replace("OpenAI", "Utku Kalender")
            
            return response
            
        except Exception as e:
            print(f"❌ Cevap Üretme Hatası: {e}")
            return "Şu an odaklanamıyorum Utku, bir hata oluştu."

if __name__ == "__main__":
    motor = LLMEngine()
    print("Test Cevabı:", motor.generate_response("Merhaba, benim adım ne?"))
