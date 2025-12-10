from telegram.ext import ConversationHandler

# Estados para conversaciones más complejas
class ConversationStates:
    # Para conversaciones sobre comida
    WAITING_FOOD_PREFERENCE = 1
    WAITING_RECIPE_REQUEST = 2
    
    # Para conversaciones sobre estudios
    WAITING_STUDY_HELP = 3
    WAITING_MOTIVATION = 4
    
    # Para personalización
    WAITING_NICKNAME = 5
    WAITING_FAVORITE_THING = 6
    
# Estados de conversación generales
WAITING, CHOOSING, CONFIRMING = range(3)