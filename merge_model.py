import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

base_model_name = "unsloth/Qwen2.5-3B-Instruct"  
adapter_path = "./models/sera_adapter"          
output_dir = "./models/sera_merged"             

print(f"🔄 Yükleniyor: {base_model_name}...")

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float16,
    device_map="cpu",
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(base_model_name)

print(f"🔗 Adaptör bağlanıyor: {adapter_path}")
model = PeftModel.from_pretrained(base_model, adapter_path)

print("🧩 Ağırlıklar birleştiriliyor...")
model = model.merge_and_unload()

print(f"💾 Kaydediliyor: {output_dir}")
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print("✅ BİRLEŞTİRME BAŞARILI!")
