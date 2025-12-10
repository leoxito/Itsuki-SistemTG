import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("8569171281:AAEpO-gN-djiSZVzkz_6pUXr-oQnQnwcs_Q")
    ADMIN_ID = int(os.getenv("8362904205", 0))
    
    # Información de Itsuki Nakano
    ITSUKI_INFO = {
        "name": "Itsuki Nakano",
        "japanese_name": "中野 五月",
        "anime": "5-toubun no Hanayome (Las Quintillisas)",
        "position": "Quinta hermana (la más joven)",
        "birthday": "5 de Mayo",
        "personality": [
            "Tímida pero determinada",
            "Amante de la comida",
            "Responsable y estudiosa", 
            "Aspirante a profesora",
            "Preocupada por los demás"
        ],
        "hobbies": ["Comer", "Estudiar", "Leer", "Cocinar"],
        "comida_favorita": ["Ramen", "Onigiri", "Dulces", "Curry"],
        "color": "#FF6B9D",
        "emoji": "🍙"
    }