import os
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def main():
    """
    Este script abre un navegador para que inicies sesión manualmente 
    en tus cuentas (Google/Gemini e Instagram) evadiendo la detección de bot.
    """
    profile_path = os.path.join(os.getcwd(), 'browser_profile')
    
    print("="*50)
    print("Iniciando Modo de Configuración de Sesiones (Con Escudo Antibot)")
    print("="*50)
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            channel="chrome", # <--- Truco: Usa tu Chrome Real para engañar a Google
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            no_viewport=True
        )
        
        # Obtenemos la primera pestaña abierta automáticamente y le aplicamos stealth
        page = context.pages[0] if context.pages else context.new_page()
        stealth_sync(page)
        
        # 1. Google Account (Login genérico suele pasar el filtro mejor que ir directo a Gemini)
        print("\n--- PASO 1 ---")
        print("Ve al navegador abierto. Por favor, inicia sesión en tu cuenta de Google.")
        print("💡 TIP: Si vuelve a fallar, intenta iniciar sesión en 'youtube.com' o 'stackoverflow.com' para engañarlo.")
        page.goto("https://accounts.google.com/")
        
        input("👉 Presiona ENTER aquí en la consola cuando hayas iniciado sesión... ")
        
        # 2. Instagram
        print("\n--- PASO 2 ---")
        print("Ahora inicia sesión en Instagram.")
        page.goto("https://www.instagram.com/")
        input("👉 Presiona ENTER aquí en la consola cuando estés logueado en Instagram y veas tu Feed... ")
        
        print("\n✅ Excelente. Las credenciales se han guardado de forma permanente en la carpeta 'browser_profile'.")
        context.close()

if __name__ == "__main__":
    main()
