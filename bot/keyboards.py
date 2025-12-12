from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# URLs oficiales actualizadas (¡esto es lo principal que debes cambiar!)
WHATSAPP_CHANNEL_URL = "https://whatsapp.com/channel/0029VbBBXTr5fM5flFaxsO06"
TELEGRAM_BOT_URL = "https://t.me/ItsukiNew_bot"  # ⬅️ ¡URL CORREGIDA AQUÍ!

def get_main_menu():
    """Teclado principal del bot simplificado"""
    keyboard = [
        [InlineKeyboardButton("🎵 /play", callback_data="play_music")],
        [InlineKeyboardButton("🎀 Itsuki Info", callback_data="itsuki_info")],
        [InlineKeyboardButton("📢 Canal Oficial", url=WHATSAPP_CHANNEL_URL)],
        [InlineKeyboardButton("🤖 Bot Oficial", url=TELEGRAM_BOT_URL)]  # ← Usa la variable
    ]
    return InlineKeyboardMarkup(keyboard)

def get_itsuki_menu():
    """Menú de información de Itsuki simplificado"""
    keyboard = [
        [InlineKeyboardButton("🎵 Volver a /play", callback_data="play_music")],
        [InlineKeyboardButton("📢 Canal Oficial", url=WHATSAPP_CHANNEL_URL)],
        [InlineKeyboardButton("🤖 Bot Oficial", url=TELEGRAM_BOT_URL)]  # ← Usa la variable
    ]
    return InlineKeyboardMarkup(keyboard)

def get_play_menu():
    """Menú específico para /play"""
    keyboard = [
        [InlineKeyboardButton("🎀 Itsuki Info", callback_data="itsuki_info")],
        [InlineKeyboardButton("📢 Canal Oficial", url=WHATSAPP_CHANNEL_URL)],
        [InlineKeyboardButton("🤖 Bot Oficial", url=TELEGRAM_BOT_URL)]  # ← Usa la variable
    ]
    return InlineKeyboardMarkup(keyboard)

def get_simple_menu():
    """Menú simple para mensajes"""
    keyboard = [
        [
            InlineKeyboardButton("🎵 /play", callback_data="play_music"),
            InlineKeyboardButton("🎀 Info", callback_data="itsuki_info")
        ],
        [
            InlineKeyboardButton("📢 Canal", url=WHATSAPP_CHANNEL_URL),
            InlineKeyboardButton("🤖 Bot", url=TELEGRAM_BOT_URL)  # ← Usa la variable
        ]
    ]
    return InlineKeyboardMarkup(keyboard)