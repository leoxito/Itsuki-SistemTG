from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config

def get_main_menu():
    """Teclado principal del bot"""
    keyboard = [
        [
            InlineKeyboardButton(f"{Config.ITSUKI_INFO['emoji']} Sobre Itsuki", callback_data="itsuki_info"),
            InlineKeyboardButton("🎭 Personalidad", callback_data="personality")
        ],
        [
            InlineKeyboardButton("🍜 Comida Favorita", callback_data="food"),
            InlineKeyboardButton("🎨 Pasatiempos", callback_data="hobby")
        ],
        [
            InlineKeyboardButton("🏫 Mi Sueño", callback_data="study"),
            InlineKeyboardButton("💭 Frase Aleatoria", callback_data="quote")
        ],
        [
            InlineKeyboardButton("📚 Ayuda", callback_data="help_command"),
            InlineKeyboardButton("🎀 Estado", callback_data="user_status")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_itsuki_menu():
    """Menú específico de Itsuki"""
    keyboard = [
        [
            InlineKeyboardButton("🎭 Mi Personalidad", callback_data="personality"),
            InlineKeyboardButton("🍜 Mi Comida", callback_data="food")
        ],
        [
            InlineKeyboardButton("🎨 Mis Hobbies", callback_data="hobby"),
            InlineKeyboardButton("🏫 Mi Sueño", callback_data="study")
        ],
        [
            InlineKeyboardButton("💭 Una de mis Frases", callback_data="quote"),
            InlineKeyboardButton("📚 Consejos", callback_data="study_tips")
        ],
        [InlineKeyboardButton("🔙 Menú Principal", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)