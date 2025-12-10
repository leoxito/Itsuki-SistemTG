import random
import json
from .music import music_handler
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import Config
from . import keyboards
from . import database

# Cargar frases de Itsuki
def load_quotes():
    quotes = {
        "itsuki": [
            "¡La comida es lo más importante en la vida! 🍜",
            "Quiero ser una profesora que inspire a sus estudiantes...",
            "A veces me da vergüenza, pero trato de ser valiente.",
            "¡No soy glotona! Solo... aprecio profundamente la buena comida.",
            "Estudiar puede ser difícil, pero es necesario para alcanzar los sueños.",
            "Cada platillo tiene su propia historia y sabor único.",
            "La paciencia es una virtud que todos debemos cultivar.",
            "Un buen profesor puede cambiar la vida de un estudiante para siempre.",
            "Ser auténtica es más importante que intentar ser perfecta.",
            "La perseverancia siempre supera al talento natural.",
            "Me gusta cuando las cosas están en orden y son predecibles.",
            "A veces me enojo cuando me confunden con mis hermanas...",
            "Los libros de texto son mis mejores amigos después de la comida.",
            "Creo que la educación es el regalo más valioso que podemos dar.",
            "¡El ramen cura cualquier mal humor!",
            "Me esfuerzo mucho en todo lo que hago, aunque no siempre lo muestre.",
            "La honestidad fortalece cualquier relación verdadera.",
            "Prefiero observar primero antes de participar en algo nuevo.",
            "Los pequeños gestos de bondad pueden hacer una gran diferencia.",
            "Sueño con tener mi propia clase llena de estudiantes entusiastas."
        ],
        "educacion": [
            "El conocimiento es el único tesoro que aumenta al compartirlo.",
            "Un buen estudiante hoy, un gran maestro mañana.",
            "La educación abre puertas que ni siquiera sabías que existían.",
            "Cada lección aprendida es un paso hacia tu futuro.",
            "No hay atajos para el verdadero aprendizaje."
        ],
        "comida": [
            "¡El primer bocado siempre es mágico!",
            "Cocinar para otros es una forma de mostrar amor.",
            "La comida une a las personas como nada más puede hacerlo.",
            "Cada cultura tiene sabores únicos que contar.",
            "Un buen día siempre empieza con un buen desayuno."
        ]
    }
    return quotes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensaje de bienvenida de Itsuki"""
    user = update.effective_user
    user_id = user.id
    
    # Registrar usuario
    database.register_user(user_id, user.first_name, user.username)
    
    welcome_text = f"""
{Config.ITSUKI_INFO['emoji']} *¡Konichiwa {user.first_name}-san!* {Config.ITSUKI_INFO['emoji']}

*¡Yo soy {Config.ITSUKI_INFO['name']}!* ({Config.ITSUKI_INFO['japanese_name']})

Soy {Config.ITSUKI_INFO['position']} y {Config.ITSUKI_INFO['personality'][0].lower()}.
{Config.ITSUKI_INFO['personality'][1]} y {Config.ITSUKI_INFO['personality'][3].lower()}.

*🍙 ¿Qué te gustaría hacer?*

Puedes usar estos comandos:
/itsuki - Mi información completa
/personalidad - Cómo soy realmente
/comida - Mi pasión gastronómica 🍜
/frase - Una frase mía aleatoria
/hobby - Mis pasatiempos favoritos
/estudio - Mi camino para ser profesora
/estado - Tu progreso conmigo
/help - Todos los comandos disponibles

O simplemente... ¡háblame como a un amigo! 😊
    """
    
    keyboard = keyboards.get_main_menu()
    await update.message.reply_text(
        welcome_text, 
        parse_mode='Markdown',
        reply_markup=keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra todos los comandos disponibles"""
    help_text = f"""
*{Config.ITSUKI_INFO['emoji']} Comandos de {Config.ITSUKI_INFO['name']} {Config.ITSUKI_INFO['emoji']}*

*📋 Comandos principales:*
/start - Inicia nuestra conversación
/help - Muestra esta ayuda completa
/itsuki - Todo sobre mí

*🎭 Mi personalidad:*
/personalidad - Cómo soy realmente
/comida - Mi amor por la gastronomía 🍜
/hobby - Mis pasatiempos favoritos
/estudio - Mi sueño de ser profesora

*💬 Interactuar:*
/frase - Una frase aleatoria mía
/estado - Tu progreso en nuestra amistad

*💭 También puedes:*
- Hablarme directamente sobre cualquier tema
- Enviarme fotos (¡me encantan!)
- Usar los botones del menú
- Preguntarme sobre comida, estudios o anime

*🎀 Dato curioso:* Mi color es {Config.ITSUKI_INFO['color']} y mi cumpleaños es {Config.ITSUKI_INFO['birthday']}!
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def itsuki_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información completa sobre Itsuki"""
    info_text = f"""
*{Config.ITSUKI_INFO['emoji']} *{Config.ITSUKI_INFO['name']}* ({Config.ITSUKI_INFO['japanese_name']}) {Config.ITSUKI_INFO['emoji']}*

*🎬 Anime:* {Config.ITSUKI_INFO['anime']}
*🎂 Cumpleaños:* {Config.ITSUKI_INFO['birthday']}
*🎀 Posición:* {Config.ITSUKI_INFO['position']}
*🎨 Color:* {Config.ITSUKI_INFO['color']}

*👤 *Personalidad:*
• {Config.ITSUKI_INFO['personality'][0]}
• {Config.ITSUKI_INFO['personality'][1]}
• {Config.ITSUKI_INFO['personality'][2]}
• {Config.ITSUKI_INFO['personality'][3]}
• {Config.ITSUKI_INFO['personality'][4]}

*🍜 *Comida Favorita:*
{chr(10).join(['• ' + comida for comida in Config.ITSUKI_INFO['comida_favorita']])}

*🎯 *Pasatiempos:*
{chr(10).join(['• ' + hobby for hobby in Config.ITSUKI_INFO['hobbies']])}

*🏫 *Mi Sueño:*
Aspiro a convertirme en una profesora que inspire a mis estudiantes y les muestre la belleza del aprendizaje. Creo que la educación es la llave para un futuro mejor.

*💖 *Curiosidad:*
Soy conocida por mi amor incondicional por la comida y mi determinación para lograr mis metas, aunque a veces me pongo nerviosa en situaciones nuevas.
    """
    
    keyboard = keyboards.get_itsuki_menu()
    await update.message.reply_text(info_text, parse_mode='Markdown', reply_markup=keyboard)

async def personality_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detalles sobre la personalidad de Itsuki"""
    personality_text = f"""
*🎭 Personalidad de {Config.ITSUKI_INFO['name']}*

*🌟 *Mis Rasgos Principales:*

*1. Tímida pero Valiente* 🦋
Aunque me pongo nerviosa en situaciones nuevas, enfrento mis miedos cuando es importante.

*2. Amante de la Comida* 🍜
¡No es que sea glotona! Simplemente aprecio profundamente la buena comida y creo que compartir una comida une a las personas.

*3. Estudiosa y Responsable* 📚
Tomo mis estudios muy en serio porque quiero ser una buena profesora. Creo en el esfuerzo constante.

*4. Determinada* 💪
Una vez que me propongo algo, no me rindo fácilmente. Mi sueño de ser profesora me motiva cada día.

*5. Cariñosa y Protectora* 🛡️
Me preocupo mucho por las personas importantes para mí, aunque a veces no sé cómo expresarlo bien.

*🎯 *Cómo soy en el día a día:*
- Organizada y metódica
- Prefiero la rutina y lo predecible
- Observadora antes de actuar
- Leal con mis amigos
- Sensible pero fuerte internamente

*💬 *Mi filosofía:*
"El crecimiento verdadero viene de enfrentar nuestros miedos, no de evitarlos. Y siempre, siempre hay lugar para una buena comida después."
    """
    
    await update.message.reply_text(personality_text, parse_mode='Markdown')

async def food_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre la comida favorita de Itsuki"""
    # Seleccionar 3 comidas aleatorias
    selected_foods = random.sample(Config.ITSUKI_INFO['comida_favorita'], 
                                  min(3, len(Config.ITSUKI_INFO['comida_favorita'])))
    
    food_text = f"""
*🍜 *La Pasión Gastronómica de Itsuki* 🍜*

*🎯 *Mis Comidas Favoritas del Día:*
{chr(10).join(['• ' + comida for comida in selected_foods])}

*🌟 *Por qué amo la comida:*
Para mí, la comida no es solo nutrición. Es:
• *Memoria:* Cada sabor trae recuerdos
• *Conexión:* Compartir comida crea lazos
• *Arte:* La preparación es creatividad
• *Consuelo:* Un buen platillo mejora cualquier día
• *Cultura:* Cada cocina cuenta una historia

*👩‍🍳 *Mi enfoque culinario:*
1. Disfrutar cada bocado conscientemente
2. Apreciar el esfuerzo del cocinero
3. Probar cosas nuevas con mente abierta
4. Compartir descubrimientos gastronómicos
5. Nunca dejar comida en el plato (¡es respeto!)

*🏆 *Top 5 Momentos Gastronómicos:*
1. El primer ramen del año nuevo 🍜
2. Onigiri casero en un picnic 🍙
3. Postre compartido con amigos 🍰
4. Comida reconfortante en días lluviosos ☔
5. Descubrir un nuevo restaurante 🎉

*💭 *Mi pensamiento sobre comida:*
"La comida es el lenguaje universal del cuidado. Cuando cocinas para alguien, le dices 'te importo' sin palabras. Y cuando compartes una comida, construyes puentes entre corazones."

*🍽️ *Consejo de Itsuki:*
"¡Nunca rechaces una invitación a comer! Cada comida es una nueva aventura esperando ser saboreada."
    """
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🍜 Ramen Especial", callback_data="food_ramen")],
        [InlineKeyboardButton("🍙 Receta de Onigiri", callback_data="food_onigiri")],
        [InlineKeyboardButton("🎂 Postre Recomendado", callback_data="food_dessert")]
    ])
    
    await update.message.reply_text(food_text, parse_mode='Markdown', reply_markup=keyboard)

async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Frase aleatoria de Itsuki"""
    quotes = load_quotes()
    
    # Seleccionar categoría aleatoria
    category = random.choice(list(quotes.keys()))
    quote = random.choice(quotes[category])
    
    # Emoji según categoría
    emojis = {
        "itsuki": "💭",
        "educacion": "📚",
        "comida": "🍜"
    }
    
    quote_text = f"{emojis.get(category, '🎀')} *Itsuki dice:*\n\n\"{quote}\""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💭 Otra frase", callback_data="another_quote")],
        [InlineKeyboardButton("🍜 Frase sobre comida", callback_data="food_quote")]
    ])
    
    await update.message.reply_text(quote_text, parse_mode='Markdown', reply_markup=keyboard)

async def hobby_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre hobbies de Itsuki"""
    hobby_text = f"""
*🎨 *Pasatiempos de {Config.ITSUKI_INFO['name']}* 🎨*

*📚 *Mis Actividades Favoritas:*

*1. Leer Libros Educativos* 📖
Me encanta aprender cosas nuevas, especialmente sobre pedagogía y diferentes culturas.

*2. Cocinar* 👩‍🍳
Experimentar en la cocina es terapéutico para mí. Me gusta recrear platillos que pruebo.

*3. Organizar* 🗂️
Tener todo en su lugar me da paz mental. Mis apuntes siempre están perfectamente ordenados.

*4. Ver Documentales* 🎬
Sobre todo de historia y culturas del mundo. ¡Aprendo mucho!

*5. Probar Nuevos Restaurantes* 🍽️
Mi aventura semanal favorita. Siempre llevo un pequeño diario de sabores.

*6. Estudiar Técnicas de Enseñanza* 🍎
Prepararme para mi futuro como profesora es mi hobby más serio.

*🌟 *Por qué estos hobbies:*
• Me ayudan a crecer como persona
• Son actividades que puedo disfrutar sola o acompañada
• Me preparan para mi sueño profesional
• Me mantienen curiosa sobre el mundo

*💡 *Consejo de Itsuki:*
"Encuentra un hobby que alimente tu alma y otro que desafíe tu mente. El equilibrio es la clave para una vida plena."

*🎯 *Mi filosofía sobre el tiempo libre:*
"Cada momento de ocio es una oportunidad para invertir en uno mismo. Ya sea aprendiendo algo nuevo o simplemente disfrutando de una buena comida."
    """
    
    await update.message.reply_text(hobby_text, parse_mode='Markdown')

async def study_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre los estudios de Itsuki y su sueño de ser profesora"""
    study_text = f"""
*🏫 *El Camino de Itsuki hacia la Enseñanza* 🍎*

*🎓 *Mi Sueño:*
Convertirme en una profesora que no solo enseñe materias, sino que inspire a sus estudiantes a amar el aprendizaje.

*📚 *Por qué quiero ser profesora:*
1. *Impacto Positivo:* Un buen profesor puede cambiar vidas
2. *Compartir Conocimiento:* Me encanta la idea de ayudar a otros a descubrir
3. *Legado Duradero:* Las lecciones importantes perduran generaciones
4. *Crear Confianza:* Quiero ser esa profesora en la que los estudiantes confíen

*📖 *Mis Materias Favoritas:*
• Historia 📜 - Para entender de dónde venimos
• Literatura 📖 - Las historias enseñan sobre la humanidad
• Ciencias Sociales 🏛️ - Cómo funcionan las sociedades
• Pedagogía 👩‍🏫 - El arte de enseñar

*🌟 *Mi Método de Estudio:*
1. *Horario Regular:* Estudio a la misma hora cada día
2. *Apuntes Organizados:* Color-coded y con resúmenes
3. *Repaso Constante:* Pequeñas sesiones diarias
4. *Aplicación Práctica:* Busco cómo usar lo aprendido
5. *Descansos con Comida:* ¡Recompensas gastronómicas! 🍙

*💪 *Desafíos que Supero:*
• Timidez al hablar en público
• Perfeccionismo excesivo
• Miedo a no ser lo suficientemente buena
• Equilibrar estudios con vida personal

*🎯 *Consejos de Estudio de Itsuki:*
1. "Encuentra tu ritmo natural de aprendizaje"
2. "No memorices, comprende"
3. "Asocia conceptos con cosas que ya amas"
4. "Recompénsate después de lograr metas"
5. "Nunca temas hacer preguntas"

*💖 *Mi Mensaje para Futuros Estudiantes:*
"El aprendizaje no es una carrera, es un viaje. Disfruta cada descubrimiento, celebra cada pequeño logro, y recuerda que incluso los profesores seguimos aprendiendo cada día."
    """
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Consejos de Estudio", callback_data="study_tips")],
        [InlineKeyboardButton("🍎 Motivación", callback_data="study_motivation")]
    ])
    
    await update.message.reply_text(study_text, parse_mode='Markdown', reply_markup=keyboard)

async def user_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Estado del usuario y su interacción con Itsuki"""
    user_id = update.effective_user.id
    user_data = database.get_user(user_id)
    
    if user_data:
        # Calcular nivel de amistad
        interactions = user_data.get('interaction_count', 0)
        friendship_level = min(interactions // 10, 10)
        
        # Título según nivel
        titles = [
            "Conocido", "Amigo Casual", "Compañero de Conversación",
            "Amigo Confiable", "Amigo Cercano", "Mejor Amigo",
            "Amigo del Alma", "Compañero de Vida", "Alter Ego", "Família"
        ]
        
        title = titles[min(friendship_level, len(titles)-1)]
        
        # Emojis según nivel
        level_emojis = ["🍙", "📚", "🍜", "🎀", "🏫", "💖", "🌟", "👑", "💫", "💕"]
        level_emoji = level_emojis[friendship_level] if friendship_level < len(level_emojis) else "💕"
        
        status_text = f"""
*{level_emoji} *Tu Estado con {Config.ITSUKI_INFO['name']}* {level_emoji}*

*👤 *Tu Información:*
• *Nombre:* {user_data.get('name', 'Amigo')}
• *Título:* {title}
• *Nivel de Amistad:* {friendship_level}/10
• *Interacciones:* {interactions}

*📊 *Tu Progreso:*
{level_emoji} {'⭐' * friendship_level}{'☆' * (10 - friendship_level)}

*🏆 *Logros Desbloqueados:*
{get_achievements(friendship_level)}

*🎯 *Próximo Nivel:*
Necesitas {max(0, 10 - (interactions % 10))} interacciones más para subir de nivel.

*💭 *Mi pensamiento sobre ti:*
{get_friendship_comment(friendship_level)}
        """
    else:
        status_text = f"""
*🍙 *¡Hola nuevo amigo!*

Aún no hemos interactuado mucho... pero estoy emocionada de conocerte mejor.

*🎯 *Para empezar:*
1. Usa /start para registrarte
2. Háblame sobre cualquier tema
3. Pregúntame sobre comida o estudios
4. Comparte tus pensamientos conmigo

*💖 *Recuerda:* Cada conversación nos acerca más.
        """
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

def get_achievements(level):
    """Obtiene logros según el nivel"""
    achievements = [
        "🎀 Primer contacto",
        "📚 Primera conversación",
        "🍜 Hablamos de comida",
        "🏫 Compartimos sobre estudios",
        "💖 Amistad confirmada",
        "🌟 Compañeros de confianza",
        "👑 Mejores amigos",
        "💫 Amigos del alma",
        "💕 Conexión especial",
        "🤗 Familia del corazón"
    ]
    
    achieved = achievements[:min(level + 1, len(achievements))]
    return chr(10).join([f"• {ach}" for ach in achieved])

def get_friendship_comment(level):
    """Comentario según el nivel de amistad"""
    comments = [
        "¡Acabamos de conocernos! Estoy emocionada por esta nueva amistad. 😊",
        "Me gusta hablar contigo. Eres una persona interesante. 📚",
        "Ya podemos hablar de comida sin vergüenza. ¡Eso es progreso! 🍜",
        "Confío en ti lo suficiente para compartir mis sueños de ser profesora. 🏫",
        "Eres un verdadero amigo. Me siento cómoda siendo yo misma contigo. 💖",
        "Nuestras conversaciones son especiales. Valoro mucho tu amistad. 🌟",
        "Eres uno de mis mejores amigos. Siempre alegras mi día. 👑",
        "Compartimos una conexión única. Eres muy importante para mí. 💫",
        "Eres como familia para mí. Gracias por estar siempre ahí. 💕",
        "No hay palabras para describir lo especial que eres. Gracias por todo. 🤗"
    ]
    
    return comments[min(level, len(comments)-1)]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja mensajes de texto normales"""
    user_message = update.message.text.lower()
    user_id = update.effective_user.id
    
    # Incrementar contador de interacciones
    database.increment_interaction(user_id)
    
    # Detectar temas del mensaje
    responses = {
        "hola": ["¡Konichiwa! ¿Cómo estás hoy? 😊", "¡Hola! Me alegra verte de nuevo. 🎀"],
        "adiós": ["¡Sayonara! Hablamos pronto 👋", "Nos vemos. ¡Que tengas un buen día! 🌸"],
        "comida": [
            "¡Hablando de comida! ¿Has probado el ramen recientemente? 🍜",
            "La comida... mi tema favorito. ¿Qué te gusta comer? 🍙"
        ],
        "hambre": [
            "¡Yo también tengo hambre! ¿Qué tal si hablamos de comida? 🍜",
            "El hambre es una señal del cuerpo. ¡Es hora de comer algo delicioso! 🍽️"
        ],
        "estudiar": [
            "¡El estudio es importante! ¿Qué estás aprendiendo ahora? 📚",
            "Como futura profesora, me encanta hablar de estudios. 🍎"
        ],
        "profesora": [
            "¡Sí! Sueño con ser profesora. ¿Te gustaría ser mi primer estudiante? 🏫",
            "Ser profesora es mi mayor sueño. Quiero inspirar a los jóvenes. 💖"
        ],
        "tímida": [
            "Sí, soy un poco tímida... pero contigo me siento cómoda. 😊",
            "La timidez es parte de mí, pero trato de superarla cada día. 🌸"
        ],
        "gracias": [
            "¡De nada! Es un placer ayudarte. 🎀",
            "No hay de qué. Me gusta pasar tiempo contigo. 💖"
        ],
        "te amo": [
            "¡Oh! Eso es... lindo. Me sonrojo un poco. 😳",
            "Eres muy dulce. Valoro mucho nuestra amistad. 💕"
        ],
        "aburrido": [
            "¡Nunca hay que aburrirse! ¿Qué tal si hablamos de comida? O de estudios... 🍜📚",
            "Podemos charlar sobre algo interesante. ¿Te gusta leer? 📖"
        ],
        "anime": [
            "Soy de 5-toubun no Hanayome. ¿Has visto mi anime? 🎬",
            "¡Las quintillizas! Aunque solo soy yo aquí contigo. 😊"
        ]
    }
    
    # Buscar palabras clave
    response = None
    for keyword, reply_options in responses.items():
        if keyword in user_message:
            response = random.choice(reply_options)
            break
    
    # Respuesta por defecto (más personalizada)
    if not response:
        default_responses = [
            "Interesante... ¿puedes contarme más sobre eso?",
            "No estoy segura de entender completamente, pero me gusta conversar contigo. 😊",
            "Eso suena bien. ¿Qué opinas tú al respecto?",
            "¡Vaya! Nunca había pensado en eso desde esa perspectiva...",
            "La vida está llena de sorpresas interesantes, ¿no crees? 🌸",
            "Me haces pensar. Eso es bueno para una futura profesora. 📚",
            "¿Y eso te hace feliz? Es importante disfrutar las pequeñas cosas. 🎀",
            "Hablando de eso... ¿has comido algo bueno hoy? 🍜",
            "Eso me recuerda a algo que estudié recientemente. 🏫",
            "Gracias por compartir eso conmigo. Me ayuda a entenderte mejor. 💖"
        ]
        response = random.choice(default_responses)
    
    await update.message.reply_text(response)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja fotos enviadas por el usuario"""
    photo_responses = [
        "¡Qué bonita foto! ¿Es de comida? Porque ahora tengo hambre... 🍜",
        "Guau... esto es hermoso. ¿Puedo guardarlo en mis recuerdos especiales? 📸",
        "Las imágenes capturan momentos únicos. ¡Gracias por compartir este momento conmigo! 🌸",
        "Esto me da inspiración... ¡para mi próximo platillo! 😅",
        "¡Me encanta! Cada imagen cuenta una historia que merece ser escuchada. 📖",
        "Bonita foto. Me recuerda que debería tomar más fotos de mi comida. 🍙",
        "¿Esto es algo que estudias? Parece interesante desde un punto de vista académico. 📚",
        "La belleza en las cosas simples... eso es lo que veo en tu foto. 🎀",
        "¡Qué lindo! Esto alegra mi día. Gracias por compartirlo. 💖",
        "Esto me inspira para ser una mejor profesora. Cada imagen enseña algo nuevo. 🍎"
    ]
    
    response = random.choice(photo_responses)
    await update.message.reply_text(response)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja clicks en botones inline"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "itsuki_info":
        await itsuki_info(update, context)
    elif data == "personality":
        await personality_info(update, context)
    elif data == "food":
        await food_info(update, context)
    elif data == "hobby":
        await hobby_info(update, context)
    elif data == "study":
        await study_info(update, context)
    elif data == "quote":
        await random_quote(update, context)
    elif data == "another_quote":
        await random_quote(update, context)
    elif data == "food_quote":
        quotes = load_quotes()
        quote = random.choice(quotes["comida"])
        await query.edit_message_text(
            f"🍜 *Itsuki dice sobre comida:*\n\n\"{quote}\"",
            parse_mode='Markdown'
        )
    elif data == "food_ramen":
        await query.message.reply_text(
            "*🍜 Receta Especial de Ramen de Itsuki:*\n\n"
            "1. Caldo de pollo hecho en casa (8 horas)\n"
            "2. Fideos artesanales\n"
            "3. Huevo marinado por 24 horas\n"
            "4. Chashu (cerdo) lentamente cocido\n"
            "5. Cebollín fresco y nori\n\n"
            "✨ *Secreto:* El amor es el ingrediente más importante.",
            parse_mode='Markdown'
        )
    elif data == "food_onigiri":
        await query.message.reply_text(
            "*🍙 Onigiri Perfecto de Itsuki:*\n\n"
            "• Arroz recién hecho\n"
            "• Relleno: salmón o umeboshi\n"
            "• Forma triangular con las manos\n"
            "• Alga nori al momento de comer\n\n"
            "💡 *Tip:* Mojar las manos en agua salada evita que el arroz se pegue.",
            parse_mode='Markdown'
        )
    elif data == "food_dessert":
        await query.message.reply_text(
            "*🎂 Postre Recomendado por Itsuki:*\n\n"
            "• *Dorayaki:* Panqueques con anko (pasta de frijol)\n"
            "• *Matcha Parfait:* Capas de helado y matcha\n"
            "• *Taiyaki:* Pez dorado relleno de crema\n"
            "• *Mochi:* Suave y chewy, perfecto con té\n\n"
            "🍰 *Consejo:* Siempre guarda espacio para el postre.",
            parse_mode='Markdown'
        )
    elif data == "study_tips":
        tips = [
            "Estudia en intervalos de 25 minutos con descansos de 5",
            "Enseña lo aprendido a alguien (¡o a un peluche!)",
            "Asocia conceptos con historias o emociones",
            "Crea mapas mentales coloridos",
            "Graba audios explicándote a ti mismo"
        ]
        tip = random.choice(tips)
        await query.message.reply_text(
            f"*📚 Consejo de Estudio de Itsuki:*\n\n{tip}\n\n"
            "Recuerda: ¡Un pequeño snack de recompensa ayuda! 🍙",
            parse_mode='Markdown'
        )
    elif data == "study_motivation":
        motivations = [
            "Cada página leída es un paso hacia tu sueño",
            "Los grandes profesores fueron primero grandes estudiantes",
            "El conocimiento es el único peso que al llevarlo te hace más ligero",
            "Hoy estudias para ser la inspiración de mañana",
            "Tu futuro yo te agradecerá este esfuerzo"
        ]
        motivation = random.choice(motivations)
        await query.message.reply_text(
            f"*🍎 Motivación de Itsuki:*\n\n✨ *{motivation}* ✨\n\n"
            "¡Tú puedes! Y después... ¡comemos algo rico! 🍜",
            parse_mode='Markdown'
        )
  
async def play_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para descargar música de YouTube"""
    await music_handler.play_command(update, context)
    
                  
                                
# Codigo que hace posible la descarga desde YT
try:
    from .music import music_handler
    
    async def play_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /play completo"""
        await music_handler.play_command(update, context)
    
    print("✅ Módulo de música cargado correctamente")
    
except ImportError as e:
    print(f"❌ Error cargando módulo de música: {e}")
    
    async def play_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Función de respaldo"""
        await update.message.reply_text(
            "🎵 *Sistema de música no disponible*\n\n"
            "🍙 *Instala dependencias:*\n"
            "```bash\n"
            "pip install aiohttp yt-dlp\n"
            "```",
            parse_mode='Markdown'
        )