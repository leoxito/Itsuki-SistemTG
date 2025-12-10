import json
import os
from datetime import datetime

def ensure_data_dir():
    """Asegura que el directorio data exista"""
    os.makedirs('data', exist_ok=True)

def load_users():
    """Carga los usuarios desde el archivo JSON"""
    ensure_data_dir()
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    """Guarda los usuarios en el archivo JSON"""
    ensure_data_dir()
    with open('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def register_user(user_id, name, username):
    """Registra o actualiza un usuario"""
    users = load_users()
    
    if str(user_id) not in users:
        users[str(user_id)] = {
            'user_id': user_id,
            'name': name,
            'username': username,
            'registered_date': datetime.now().isoformat(),
            'last_interaction': datetime.now().isoformat(),
            'interaction_count': 0,
            'friendship_level': 0
        }
    else:
        users[str(user_id)]['last_interaction'] = datetime.now().isoformat()
        users[str(user_id)]['name'] = name
        users[str(user_id)]['username'] = username
    
    save_users(users)

def get_user(user_id):
    """Obtiene información de un usuario"""
    users = load_users()
    return users.get(str(user_id))

def increment_interaction(user_id):
    """Incrementa el contador de interacciones"""
    users = load_users()
    
    if str(user_id) in users:
        users[str(user_id)]['interaction_count'] += 1
        users[str(user_id)]['last_interaction'] = datetime.now().isoformat()
        
        # Calcular nivel de amistad
        interactions = users[str(user_id)]['interaction_count']
        users[str(user_id)]['friendship_level'] = min(interactions // 10, 10)
        
        save_users(users)

def get_top_users(limit=10):
    """Obtiene los usuarios más activos"""
    users = load_users()
    
    # Filtrar usuarios con interacciones
    active_users = [user for user in users.values() if user['interaction_count'] > 0]
    
    # Ordenar por interacciones
    sorted_users = sorted(active_users, key=lambda x: x['interaction_count'], reverse=True)
    
    return sorted_users[:limit]

# Inicializar datos al importar
ensure_data_dir()