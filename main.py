# main.py
import os
from brain import BrainGPT
from browser_agent import BrowserAgent
from dotenv import load_dotenv

import sys

load_dotenv()

def main():
    print("🚀 Iniciando el Agente Community Manager Evolucionado")
    
    media_file_1 = os.path.join(os.getcwd(), "test_image.jpg")
    media_file_2 = os.path.join(os.getcwd(), "Community Concept", "test_debug_image.jpg")
    
    if os.path.exists(media_file_1):
        input_photo = media_file_1
    elif os.path.exists(media_file_2):
        input_photo = media_file_2
    else:
        print("❌ ERROR: No se encontró una foto de prueba ('test_image.jpg').")
        return
        
    # Obtiene el tema del post desde la interfaz (argumento 1), o usa un predeterminado
    tema_post = sys.argv[1] if len(sys.argv) > 1 else "nuestro impresionante trabajo corporativo"
    
    # 1. El Cerebro (GPT)
    print("\n--- FASE 1: PENSAMIENTO Y REDACCIÓN (CEREBRO) ---")
    brain = BrainGPT()
    
    caption_instagram = brain.generate_instagram_post(tema_post)
    print(f"\n   [POST MAESTRO CREADO POR GPT PARA INSTAGRAM]:\n{caption_instagram}\n")
    
    # 2. Interacción Web Unificada
    print("--- FASE 2: NAVEGACIÓN WEB AUTOMATIZADA ---")
    prompt_for_gemini = f"Quiero que uses tu motor interno de IA para animar la foto adjunta sobre '{tema_post}'. NO me des ideas ni guiones. Necesito que exportes un archivo de video real (.mp4) de esta imagen."
    agent = BrowserAgent()
    agent.run_bot_flow(prompt_text=prompt_for_gemini, image_path=input_photo, instagram_caption=caption_instagram)
    
    print(f"\n🎉 ¡Flujo Completo! Tokens gastados en razonamiento: {brain.total_tokens_used}")

if __name__ == "__main__":
    main()
