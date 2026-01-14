import sqlite3
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class MemorySystem:
    def __init__(self):
        self.db_path = config.MEMORY_DB_PATH
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.create_tables()

    def create_tables(self):
        """
        Gerekli tabloları oluşturur.
        Şimdilik sadece sohbet geçmişi var.
        İleride buraya 'iot_devices' tablosu da eklenecek.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,    -- 'user' veya 'bot'
                content TEXT, -- Mesaj içeriği
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        print("💾 Hafıza sistemi (Veritabanı) hazır.")

    def add_message(self, role, content):
        """Yeni bir mesajı hafızaya kaydeder"""
        try:
            self.cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Hafıza Yazma Hatası: {e}")

    def get_context(self, limit=5):
        """
        Son konuşmaları getirir.
        limit=5 -> Son 5 mesajı alıp Sera'ya hatırlatır.
        """
        try:
            self.cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,))
            rows = self.cursor.fetchall()
            
            history = []
            for role, content in reversed(rows):
                isim = "Utku" if role == "user" else "Sera"
                history.append(f"{isim}: {content}")
            
            return "\n".join(history)
        except Exception as e:
            print(f"⚠️ Hafıza Okuma Hatası: {e}")
            return ""

    def clear_memory(self):
        """Hafızayı sıfırlar (Eğitim öncesi temizlik için gerekebilir)"""
        self.cursor.execute("DELETE FROM messages")
        self.conn.commit()
        print("🧹 Hafıza temizlendi.")

# --- Test Bloğu ---
if __name__ == "__main__":
    mem = MemorySystem()
    mem.add_message("user", "Merhaba Sera, nasılsın?")
    mem.add_message("bot", "İyiyim Utku, teşekkürler.")
    print("--- Mevcut Hafıza ---")
    print(mem.get_context())
