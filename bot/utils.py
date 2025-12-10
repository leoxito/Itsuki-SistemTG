import random
from datetime import datetime

def get_time_based_greeting():
    """Obtiene saludo basado en la hora del día"""
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "¡Ohayou gozaimasu! (Buenos días) 🌅"
    elif 12 <= hour < 18:
        return "¡Konnichiwa! (Buenas tardes) ☀️"
    elif 18 <= hour < 22:
        return "¡Konbanwa! (Buenas noches) 🌙"
    else:
        return "¿Aún despierto? Oyasumi... (Buenas noches) 🌃"

def get_random_food_emoji():
    """Obtiene un emoji de comida aleatorio"""
    food_emojis = ["🍜", "🍙", "🍣", "🍛", "🍱", "🥟", "🍢", "🍡", "🍮", "🍰", "🍫", "🍩", "🍎", "🍓"]
    return random.choice(food_emojis)

def format_quote(quote, category="itsuki"):
    """Formatea una frase con emojis según categoría"""
    emoji_map = {
        "itsuki": "💭",
        "comida": "🍜",
        "educacion": "📚",
        "hobby": "🎨",
        "personal": "🎀"
    }
    
    emoji = emoji_map.get(category, "🎀")
    return f"{emoji} *Itsuki dice:*\n\n\"{quote}\""

def calculate_friendship_level(interactions):
    """Calcula el nivel de amistad basado en interacciones"""
    if interactions >= 100:
        return 10, "💕 Familia del Corazón"
    elif interactions >= 80:
        return 9, "💫 Conexión Especial"
    elif interactions >= 60:
        return 8, "👑 Amigos del Alma"
    elif interactions >= 40:
        return 7, "🌟 Mejores Amigos"
    elif interactions >= 30:
        return 6, "💖 Compañeros de Confianza"
    elif interactions >= 20:
        return 5, "🏫 Amistad Confirmada"
    elif interactions >= 15:
        return 4, "🍜 Compartimos Comida"
    elif interactions >= 10:
        return 3, "📚 Compartimos Estudios"
    elif interactions >= 5:
        return 2, "🎀 Amigo Casual"
    elif interactions >= 1:
        return 1, "🍙 Conocido"
    else:
        return 0, "👋 Nuevo Amigo"