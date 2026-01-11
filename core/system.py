import subprocess
import platform
from duckduckgo_search import DDGS
from thefuzz import fuzz

CURRENT_OS = platform.system()

def check_similarity(user_text, command_key):
    """Bulanık mantıkla komut kontrolü (Örn: %75 benzerlik)"""
    ratio = fuzz.partial_ratio(user_text.lower(), command_key.lower())
    return ratio >= 75

def open_application(app_name):
    """Uygulama açma mantığı"""
    try:
        if CURRENT_OS == "Linux":
            if app_name == "hesap_makinesi":
                subprocess.Popen(["gnome-calculator"])
                return "Hesap makinesi açıldı."
            elif app_name == "notepad":
                subprocess.Popen(["gedit"])
                return "Not defteri açıldı."
        
        # Buraya ileride Windows/Mac eklenebilir
        return "Bu uygulama şu an desteklenmiyor."
    except Exception as e:
        return f"Uygulama açılırken hata: {e}"

def search_web(query):
    """DuckDuckGo ile internet araması"""
    try:
        ddgs = DDGS()
        # 'text' yerine 'keywords' veya eski versiyonsa direkt parametre
        # Kütüphanenin güncel hali için .text() metodu kullanılır
        results = ddgs.text(query, max_results=3)
        
        # Sonuçları düzenle
        formatted_results = []
        for r in results:
            formatted_results.append({
                "title": r['title'],
                "url": r['href'],
                "desc": r['body']
            })
        return formatted_results
    except Exception as e:
        print(f"Arama Hatası: {e}")
        return []
