import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os
import datetime
import sys

# --- SERA AI MOTORU ---
class LLMEngine:
    def __init__(self, model_path="models/sera_adapter"):
        print("\n⚙️  Sera AI Motoru (CPU) Yükleniyor... Lütfen bekleyin.")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, "models", "sera_adapter")
        
        self.base_model_name = "unsloth/Qwen2.5-3B-Instruct"
        self.device = "cpu"
        
        # 1. Ana Modeli Yükle
        try:
            self.base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                torch_dtype=torch.float32,
                device_map=self.device,
                trust_remote_code=True
            )
        except Exception as e:
            print(f"❌ Ana Model Yükleme Hatası: {e}")
            raise e

        # 2. Sera Kişiliğini (Adaptör) Yükle
        if os.path.exists(self.model_path):
            print(f"🔗 Sera Kişiliği Bağlanıyor...")
            self.model = PeftModel.from_pretrained(self.base_model, self.model_path)
            self.model = self.model.merge_and_unload()
        else:
            print(f"⚠️  UYARI: Adaptör bulunamadı ({self.model_path})! Varsayılan model çalışacak.")
            self.model = self.base_model

        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
        print("✅ Sera Hazır ve Emrinizde!\n")

    def generate_response(self, user_input, context=""):
        now = datetime.datetime.now()
        tarih_saat = now.strftime("%d %B %Y, Saat %H:%M")

        # 2. Sistem Mesajı (Kişilik Tanımı)
        system_prompt = (
            f"Şu anki tarih: {tarih_saat}.\n"
            "Senin adın Sera. Kullanıcının adı Utku.\n"
            "Sen yardımsever, zeki ve samimi bir yapay zeka asistanısın.\n"
            "Cevapların kısa, net ve Türkçe olsun.\n"
            "Utku'ya her zaman ismiyle hitap etmeye çalış."
        )

        if context:
            system_prompt += f"\n\nEK BİLGİ (Hafıza):\n{context}"

        # 3. Prompt Formatı (Eğitim yapısına uygun)
        full_prompt = f"""Aşağıda bir görevi tanımlayan bir talimat ve bağlam sağlayan bir girdi bulunmaktadır. İsteği uygun şekilde tamamlayan bir yanıt yazın.

### Instruction:
{system_prompt}
Kullanıcı Soru: {user_input}

### Input:


### Response:
"""
        # 4. Cevap Üretme
        try:
            inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.6,
                    do_sample=True,
                    repetition_penalty=1.15
                )
                
            full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = full_text.split("### Response:\n")[-1].strip()
            return response
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            return "Beynimde anlık bir sorun oluştu Utku, tekrar dener misin?"

# --- TEST BLOĞU ---
if __name__ == "__main__":
    # Bu dosya tek başına çalıştırılırsa test yapar
    motor = LLMEngine()
    print("Sera:", motor.generate_response("Merhaba, bugün nasılsın?"))
