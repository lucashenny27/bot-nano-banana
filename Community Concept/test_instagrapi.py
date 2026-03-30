from instagrapi import Client
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

print("="*60)
print("📸 TEST DE CONEXIÓN INSTAGRAPI")
print("="*60)

if not USERNAME or not PASSWORD or "tu_usuario" in USERNAME:
    print("❌ ERROR: Debes configurar INSTAGRAM_USERNAME y INSTAGRAM_PASSWORD en el archivo .env")
    print("   Edita el archivo .env y pon tus credenciales reales.")
    exit()

print(f"👤 Usuario: {USERNAME}")
print("🔐 Intentando login...")

try:
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    print("\n✅ ¡LOGIN EXITOSO!")
    print("   Instagrapi se ha conectado correctamente a tu cuenta.")
    print("   Información de cuenta:", cl.user_id)
    
except Exception as e:
    print("\n❌ FALLÓ EL LOGIN")
    print(f"   Error: {e}")
    print("\n⚠️  Posibles causas:")
    print("   1. Contraseña incorrecta")
    print("   2. Instagram pidió verificación (Challenge) -> Revisa tu email/SMS")
    print("   3. Bloqueo temporal por uso de bot")

print("="*60)
