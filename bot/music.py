"""
Sistema de música completo para Itsuki Nakano Bot
Adaptado del código original de WhatsApp para Telegram
"""
import os
import re
import json
import asyncio
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import yt_dlp
import aiohttp

class MusicHandler:
    """Sistema de música completo con múltiples APIs de respaldo"""
    
    def __init__(self):
        self.temp_dir = "data/temp_music"
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Configurar yt-dlp con FFmpeg si está disponible
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': os.path.join(self.temp_dir, '%(id)s.%(ext)s'),
            'postprocessors': [],
            'extract_flat': False,
            'noplaylist': True,
        }
        
        # Intentar usar FFmpeg si existe
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=False)
            self.ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            self.has_ffmpeg = True
        except:
            self.has_ffmpeg = False
    
    async def play_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /play - Versión completa como el original"""
        if not context.args:
            await update.message.reply_text(
                "🎵 *COMANDO /play*\n\n"
                "Uso: `/play <nombre de canción o URL de YouTube>`\n\n"
                "*Ejemplos:*\n"
                "• `/play Stay With Me`\n"
                "• `/play https://youtu.be/abc123`\n"
                "• `/play anime opening 2024`\n\n"
                "🍙 *Itsuki buscará en YouTube y descargará el audio*",
                parse_mode='Markdown'
            )
            return
        
        query = " ".join(context.args)
        
        # Mensaje de estado inicial
        status_msg = await update.message.reply_text(
            f"🎵 *Itsuki está procesando tu solicitud...*\n\n"
            f"🔍 *Búsqueda:* `{query}`\n"
            "⏳ *Por favor espera...* 🍙",
            parse_mode='Markdown'
        )
        
        try:
            # PASO 1: Detectar si es URL o búsqueda
            youtube_url = ''
            video_title = 'Audio de YouTube'
            video_id = ''
            
            # Verificar si es URL de YouTube
            is_youtube_url = self._is_youtube_url(query)
            
            if is_youtube_url:
                video_id = self._extract_youtube_id(query)
                if video_id:
                    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                    # Obtener título
                    try:
                        video_info = await self._get_video_info_api(youtube_url)
                        video_title = video_info.get('titulo', 'Audio YouTube')
                    except:
                        video_title = 'Audio YouTube'
                else:
                    await status_msg.edit_text(
                        "❌ *URL de YouTube no válida*\n\n"
                        "🍙 *Por favor usa una URL válida de YouTube*",
                        parse_mode='Markdown'
                    )
                    return
            else:
                # Búsqueda por texto
                await status_msg.edit_text(
                    f"🔍 *Buscando en YouTube:*\n`{query}`\n\n"
                    "🎵 *Itsuki está buscando la mejor opción...* 🍙",
                    parse_mode='Markdown'
                )
                
                search_result = await self._search_youtube_ultra_fast(query)
                if not search_result:
                    await status_msg.edit_text(
                        "❌ *No se encontraron resultados*\n\n"
                        "🍙 *Intenta con otro nombre o artista*",
                        parse_mode='Markdown'
                    )
                    return
                
                youtube_url = f"https://www.youtube.com/watch?v={search_result['id']}"
                video_title = search_result['title']
                video_id = search_result['id']
            
            # PASO 2: Obtener información del video
            await status_msg.edit_text(
                f"✅ *¡Encontrado!*\n\n"
                f"🎵 *{video_title}*\n\n"
                "📥 *Obteniendo información completa...* 🍙",
                parse_mode='Markdown'
            )
            
            video_info = await self._get_video_info_api(youtube_url)
            if video_info and video_info.get('titulo'):
                video_title = video_info['titulo']
            
            # PASO 3: Mostrar información
            info_text = self._format_info_message(video_info, video_title, youtube_url)
            
            # PASO 4: Descargar audio (método automático)
            await status_msg.edit_text(
                f"{info_text}\n\n"
                "⬇️ *Itsuki está descargando el audio...*\n"
                "⏳ *Esto puede tomar unos segundos* 🍙",
                parse_mode='Markdown'
            )
            
            # Intentar diferentes métodos de descarga
            audio_file = None
            
            # Método 1: API May (Prioridad 1)
            try:
                audio_file = await self._download_audio_may_api(youtube_url)
            except Exception as e:
                print(f"API May falló: {e}")
            
            # Método 2: API Neeveloop (Prioridad 2)
            if not audio_file:
                try:
                    audio_file = await self._download_audio_api(youtube_url)
                except Exception as e:
                    print(f"API Neeveloop falló: {e}")
            
            # Método 3: yt-dlp (Último recurso)
            if not audio_file:
                try:
                    audio_file = await self._download_audio_ytdlp(youtube_url)
                except Exception as e:
                    print(f"yt-dlp falló: {e}")
            
            if not audio_file:
                raise Exception("No se pudo descargar el audio con ningún método")
            
            # PASO 5: Enviar audio
            await status_msg.edit_text(
                f"✅ *Audio descargado!*\n\n"
                f"🎵 *Enviando:* `{video_title[:50]}...`\n"
                "🍙 *Un momento por favor...*",
                parse_mode='Markdown'
            )
            
            # Enviar archivo de audio
            with open(audio_file, 'rb') as audio_data:
                await update.message.reply_audio(
                    audio=audio_data,
                    title=video_title[:64],
                    performer=video_info.get('canal', 'YouTube')[:32] if video_info else 'YouTube',
                    caption=f"🎵 *{video_title}*\n\n⬇️ Descargado por Itsuki Nakano 🍙",
                    parse_mode='Markdown'
                )
            
            # Eliminar mensaje de estado
            await status_msg.delete()
            
            # Limpiar archivo temporal
            await asyncio.sleep(5)
            try:
                os.remove(audio_file)
            except:
                pass
            
        except Exception as e:
            error_msg = str(e)
            await status_msg.edit_text(
                f"❌ *Error al procesar:*\n\n`{error_msg[:100]}`\n\n"
                "🍙 *Itsuki lo siente mucho...*\n"
                "Intenta con otra canción o URL.",
                parse_mode='Markdown'
            )
    
    # ==================== MÉTODOS DE BÚSQUEDA ====================
    
    def _is_youtube_url(self, url):
        """Verifica si es una URL de YouTube"""
        return bool(re.search(r'youtu\.?be', url, re.IGNORECASE))
    
    def _extract_youtube_id(self, url):
        """Extrae ID de video de URL de YouTube"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    async def _search_youtube_ultra_fast(self, query):
        """Búsqueda rápida en YouTube (como en tu código original)"""
        try:
            search_url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=5)
            html = response.text
            
            # Buscar el primer video en resultados
            pattern = r'"videoId":"([a-zA-Z0-9_-]{11})".*?"title":\{"runs":\[\{"text":"([^"]+?)"'
            match = re.search(pattern, html)
            
            if match:
                return {
                    'id': match.group(1),
                    'title': match.group(2).replace('\\u0026', '&')[:60]
                }
            
            return None
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return None
    
    # ==================== MÉTODOS DE DESCARGA ====================
    
    async def _download_audio_may_api(self, url):
        """API May - Prioridad 1"""
        try:
            print("🔧 Intentando con API May...")
            api_url = f"https://mayapi.ooguy.com/ytdl?apikey=may-f53d1d49&url={requests.utils.quote(url)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, timeout=15) as response:
                    data = await response.json()
            
            # Buscar URL de audio en la respuesta
            audio_url = None
            
            # Diferentes estructuras posibles
            if data.get('result') and data['result'].get('url'):
                audio_url = data['result']['url']
            elif data.get('audio'):
                audio_url = data['audio']
            elif data.get('url'):
                audio_url = data['url']
            else:
                # Búsqueda recursiva
                def find_audio_url(obj):
                    for key, value in obj.items():
                        if isinstance(value, str) and value.endswith('.mp3'):
                            return value
                        elif isinstance(value, dict):
                            result = find_audio_url(value)
                            if result:
                                return result
                        elif isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict):
                                    result = find_audio_url(item)
                                    if result:
                                        return result
                    return None
                
                audio_url = find_audio_url(data)
            
            if not audio_url:
                raise Exception('No se encontró URL de audio')
            
            print(f"✅ API May proporcionó URL: {audio_url[:50]}...")
            
            # Descargar el audio
            temp_file = os.path.join(self.temp_dir, f"may_{hash(url)}.mp3")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url, timeout=30) as response:
                    with open(temp_file, 'wb') as f:
                        while True:
                            chunk = await response.content.read(8192)
                            if not chunk:
                                break
                            f.write(chunk)
            
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1024:
                return temp_file
            
            return None
            
        except Exception as e:
            print(f"❌ API May falló: {e}")
            return None
    
    async def _download_audio_api(self, url):
        """API Neeveloop - Prioridad 2"""
        try:
            print("🔧 Intentando con API Neeveloop...")
            key = "7FlPnpuUbnbrZIhZ"
            audio_url = f"https://api-nv.ultraplus.click/api/dl/yt-direct?url={requests.utils.quote(url)}&type=audio&key={key}"
            
            temp_file = os.path.join(self.temp_dir, f"api_{hash(url)}.mp3")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url, timeout=60) as response:
                    with open(temp_file, 'wb') as f:
                        while True:
                            chunk = await response.content.read(8192)
                            if not chunk:
                                break
                            f.write(chunk)
            
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1024:
                return temp_file
            
            return None
            
        except Exception as e:
            print(f"❌ API Neeveloop falló: {e}")
            return None
    
    async def _download_audio_ytdlp(self, url):
        """yt-dlp - Último recurso"""
        try:
            print("🔧 Intentando con yt-dlp...")
            import subprocess
            import tempfile
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False, dir=self.temp_dir) as tmp:
                temp_file = tmp.name
            
            # Comando yt-dlp
            cmd = [
                'yt-dlp',
                '-x',  # Extraer audio
                '--audio-format', 'mp3',
                '--audio-quality', '5',  # Calidad media
                '--no-playlist',
                '-o', temp_file,
                url
            ]
            
            # Ejecutar
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                # Verificar que el archivo existe y tiene contenido
                if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1024:
                    return temp_file
            
            return None
            
        except Exception as e:
            print(f"❌ yt-dlp falló: {e}")
            return None
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    async def _get_video_info_api(self, url):
        """Obtiene información del video desde API"""
        try:
            key = "7FlPnpuUbnbrZIhZ"
            api_url = f"https://api-nv.ultraplus.click/api/youtube/info?url={requests.utils.quote(url)}&key={key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, timeout=10) as response:
                    data = await response.json()
            
            if data and data.get('Result'):
                return data['Result']
            
            return {
                'titulo': 'Título no disponible',
                'canal': 'Canal no disponible',
                'duracion': 'Duración no disponible'
            }
            
        except Exception:
            return {
                'titulo': 'Título no disponible',
                'canal': 'Canal no disponible',
                'duracion': 'Duración no disponible'
            }
    
    def _format_info_message(self, video_info, video_title, youtube_url):
        """Formatea el mensaje de información"""
        author = video_info.get('canal', 'Desconocido') if video_info else 'Desconocido'
        duration = video_info.get('duracion', 'Desconocida') if video_info else 'Desconocida'
        
        info_message = "`🎵 𝐘𝐨𝐮𝐭𝐮𝐛𝐞 𝐌𝐏𝟑 🎵`\n\n"
        info_message += "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n\n"
        info_message += f"`𖦹` *Título:* `{video_info.get('titulo', video_title) if video_info else video_title}`\n\n"
        info_message += f"`۞` *Autor:* `{author}`\n\n"
        info_message += f"`☆` *Duración:* `{duration}`\n\n"
        info_message += f"`𑁍` *URL:* {youtube_url}\n\n"
        info_message += "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n\n"
        info_message += "» *Itsuki Nakano Bot* 🍙\n\n"
        info_message += "> *By: Itsuki Nakano*\n\n"
        info_message += "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n\n"
        
        return info_message
    
    async def _get_high_quality_thumbnail(self, video_id):
        """Obtiene thumbnail de alta calidad"""
        if not video_id:
            return None
        
        thumbnail_qualities = [
            f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
            f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg",
            f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        ]
        
        for thumbnail_url in thumbnail_qualities:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(thumbnail_url, timeout=3) as response:
                        if response.status == 200:
                            data = await response.read()
                            if len(data) > 5000:
                                return data
            except:
                continue
        
        return None

# Instancia global del manejador de música
music_handler = MusicHandler()

# luego debo de poner thumbnailUrl...