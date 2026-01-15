import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os
import datetime
import sys

class LLMEngine:
    def __init__(self, model_path="models/sera_adapter"):
        print("\n⚙️  Sera AI Motoru (CPU) Yükleniyor... Lütfen bekleyin.")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, "models", "sera_adapter")
        
        self.base_model_name = "unsloth/Qwen2.5-3B-Instruct"
        self.device = "cpu"
        
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

        if os.path.exists(self.model_path):
            print(f"🔗 Sera Kişiliği Bağlanıyor...")
            try:
                self.model = PeftModel.from_pretrained(self.base_model, self.model_path)
                self.model = self.model.merge_and_unload()
                print("✅ Adaptör başarıyla birleştirildi.")
            except Exception as e:
                print(f"⚠️ Adaptör yüklenirken hata: {e}\nVarsayılan model kullanılıyor.")
                self.model = self.base_model
        else:
            print(f"⚠️  UYARI: Adaptör bulunamadı ({self.model_path})! Varsayılan model çalışacak.")
            self.model = self.base_model

        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
        print("✅ Sera Hazır ve Emrinizde!\n")

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
            system_prompt += f"\n\nEK BİLGİ (Hafıza):\n{context}"

        full_prompt = f"""Aşağıda bir görevi tanımlayan bir talimat ve bağlam sağlayan bir girdi bulunmaktadır. İsteği uygun şekilde tamamlayan bir yanıt yazın.

### Instruction:
{system_prompt}
Kullanıcı Soru: {user_input}

### Input:

### Response:
"""
        try:
            inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=250,
                    temperature=0.6,
                    do_sample=True,
                    repetition_penalty=1.2
                )
                
            full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            if "### Response:" in full_text:
                response = full_text.split("### Response:")[-1].strip()
            else:
                response = full_text

            
            if "#" in response:
                response = response.split("#")[0].strip()

            response = response.replace("Intel", "Utku Kalender")
            response = response.replace("OpenAI", "Utku Kalender")
            response = response.replace("tarafından geliştirilen bir yapay zeka modeliyim", "Utku Kalender tarafından geliştirilen Sera'yım")

            return response
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            return "Beynimde anlık bir işlem hatası oluştu Utku."

if __name__ == "__main__":
    motor = LLMEngine()
    print("Sera:", motor.generate_response("Merhaba, seni kim yaptı?"))
