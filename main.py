import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot import handlers
from config import Config

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Función principal del bot - Versión simplificada"""
    
    # Crear aplicación
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # ========== COMANDOS BÁSICOS ==========
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(CommandHandler("itsuki", handlers.itsuki_info))
    application.add_handler(CommandHandler("personalidad", handlers.personality_info))
    application.add_handler(CommandHandler("comida", handlers.food_info))
    application.add_handler(CommandHandler("frase", handlers.random_quote))
    application.add_handler(CommandHandler("hobby", handlers.hobby_info))
    application.add_handler(CommandHandler("estudio", handlers.study_info))
    application.add_handler(CommandHandler("estado", handlers.user_status))
    
    # ========== COMANDOS DE MÚSICA ==========
    application.add_handler(CommandHandler("play", handlers.play_music))
    application.add_handler(CommandHandler("music", handlers.play_music))
    application.add_handler(CommandHandler("cancion", handlers.play_music))
    application.add_handler(CommandHandler("musica", handlers.play_music))
    
    # ========== HANDLERS DE MENSAJES ==========
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message))
    
    # Handler para fotos si existe
    if hasattr(handlers, 'handle_photo_simple'):
        application.add_handler(MessageHandler(filters.PHOTO, handlers.handle_photo_simple))
    
    # ========== INICIAR BOT ==========
    print("=" * 50)
    print("🚀 ITSUKI NAKANO BOT INICIANDO...")
    print("🎵 Sistema de música: DESCARGAS DIRECTAS")
    print("=" * 50)
    
    # Iniciar polling
    application.run_polling(
        poll_interval=1,
        timeout=30,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()