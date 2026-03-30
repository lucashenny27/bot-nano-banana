import os
import requests
import tempfile
from dotenv import load_dotenv
from instagrapi import Client

load_dotenv()

# Credenciales desde .env
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

def download_image_to_temp(image_url):
    """Descarga la imagen de la URL a un archivo temporal."""
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        
        # Crear archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
        temp_file.close()
        return temp_file.name
    except Exception as e:
        print(f"❌ Error descargando imagen: {e}")
        return None

def publish_instagram_post(image_url, caption, schedule_time=None):
    """
    Publica un post en Instagram usando Instagrapi (Usuario/Contraseña).
    """
    print(f"🚀 Iniciando publicación en Instagram para: {USERNAME}")
    
    if not USERNAME or not PASSWORD:
        print("❌ Error: Faltan credenciales INSTAGRAM_USERNAME o INSTAGRAM_PASSWORD en .env")
        return None

    client = Client()
    
    try:
        # 1. Login
        print("🔐 Iniciando sesión en Instagram...")
        client.login(USERNAME, PASSWORD)
        print("✅ Login exitoso")
        
        # 2. Descargar imagen
        print(f"⬇️ Descargando imagen: {image_url}...")
        image_path = download_image_to_temp(image_url)
        
        if not image_path:
            return None
            
        # 3. Publicar (Upload)
        print("⬆️ Subiendo foto...")
        media = client.photo_upload(
            path=image_path,
            caption=caption
        )
        
        # 4. Limpieza
        if os.path.exists(image_path):
            os.remove(image_path)
            
        print(f"✅ Publicado exitosamente! Media PK: {media.pk}")
        
        return {
            "id": media.pk,
            "url": f"https://www.instagram.com/p/{media.code}/",
            "media_type": "image"
        }
        
    except Exception as e:
        print(f"❌ Error crítico publicando en Instagram: {e}")
        # Si falla login por challenge, instagrapi suele tirar ChallengeRequired
        return None

if __name__ == "__main__":
    # Test rápido si se ejecuta directo
    test_url = "https://pollinations.ai/p/cyberpunk%20city?width=1080&height=1080&seed=42&model=flux"
    test_caption = "Test post from Community Concept App 🤖 #ai #testing"
    publish_instagram_post(test_url, test_caption)
