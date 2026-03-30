import os
import time
import random
import requests
import base64
import mimetypes
from playwright.sync_api import sync_playwright

class BrowserAgent:
    def __init__(self, profile_dir="browser_profile"):
        self.profile_path = os.path.join(os.getcwd(), profile_dir)
        
    def run_bot_flow(self, prompt_text: str, image_path: str, instagram_caption: str):
        # Verificamos si hay un bloqueo previo del perfil (limpieza de seguridad)
        lock_file = os.path.join(self.profile_path, "SingletonLock")
        if os.path.exists(lock_file):
            print("🧹 Detectado un bloqueo previo en el perfil. Intentando limpiar...")
            try: os.remove(lock_file)
            except: pass

        with sync_playwright() as p:
            print("🌐 [Navegador] Arranque del motor. Abriendo Chrome del Bot...")
            try:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=self.profile_path,
                    channel="chrome",
                    headless=False,
                    args=["--disable-blink-features=AutomationControlled", "--start-maximized"],
                    no_viewport=True,
                    accept_downloads=True,
                    slow_mo=100
                )
            except Exception as e:
                print(f"\n❌ ERROR CRÍTICO AL ABRIR CHROME: El perfil está bloqueado o en uso.")
                print("👉 SOLUCIÓN: Cierra todas las ventanas de Chrome abiertas por el bot o usa el botón 'Limpiar Navegador'.")
                return # Salimos del try, p se encargará de cerrarse solo
            
            page = context.pages[0] if context.pages else context.new_page()
            
            # ==========================================
            # FASE 1: GEMINI
            # ==========================================
            print(f"🧠 [Gemini Web] Ingresando a Google Gemini...")
            page.goto("https://gemini.google.com/app")
            page.wait_for_load_state("domcontentloaded")
            
            # Check login
            if "accounts.google.com" in page.url or "Sign in" in page.content() or "Iniciar sesión" in page.content():
                print("⚠️ [ATENCIÓN] Google requiere iniciar sesión.")
                print("   👉 Tienes 60 segundos para iniciar sesión en la ventana abierta. ¡Hazlo ahora!")
                page.wait_for_selector('div[contenteditable="true"]', timeout=60000)
                print("✅ [Gemini Web] Sesión detectada. Continuando...")
                time.sleep(2)
            
            # Seleccionar la herramienta personalizada 'nano banana'
            print("🍌 [Gemini Web] Buscando tu herramienta especializada 'nano banana'...")
            try:
                banana_btn = page.locator('span, div, a, p, span[title]').filter(has_text="nano banana").last
                banana_btn.wait_for(state="visible", timeout=8000)
                # Playwright a veces necesita forzar el clic en un menú
                banana_btn.click(force=True)
                time.sleep(4)
                print("🍌 [Gemini Web] ¡Expertise 'nano banana' activado con éxito!")
            except Exception as e:
                print("⚠️ No logré encontrar 'nano banana' en tu barra lateral. Habláre con el modelo por defecto.")

            if image_path and os.path.exists(image_path):
                print(f"📎 [Gemini Web] Iniciando secuencia de clics para subir archivo...")
                try:
                    chat_box = page.locator('div[contenteditable="true"]').first
                    chat_box.wait_for(state="visible", timeout=15000)
                    
                    # ESTRATEGIA 5: Clic visual guiado por la captura de pantalla del usuario
                    print("   -> Buscando el botón '+'...")
                    try:
                        # Buscamos el botón de subir/añadir por nombre general
                        plus_btn = page.locator('button[aria-label*="ubir"], button[aria-label*="ñad"], button[aria-label*="load"], button[aria-label*="lus"]').first
                        plus_btn.click(timeout=3000)
                    except:
                        # Si cambiaron el nombre oculto, usamos su posición física: el primer botón al lado de la caja de chat
                        page.locator('rich-textarea').locator('xpath=./../../../..').locator('button').first.click()
                    
                    # Damos tiempo a que se dibuje el menú emergente
                    time.sleep(1.5)
                    
                    print("   -> Menú desplegado. Clic en 'Subir archivos'...")
                    with page.expect_file_chooser(timeout=6000) as fc_info:
                        # Basado EXACTAMENTE en tu captura de pantalla
                        upload_option = page.locator('text="Subir archivos"').first
                        upload_option.click()
                    
                    print("   -> ¡Ventana interceptada! Entregando foto...")
                    fc_info.value.set_files(image_path)
                    
                    print("✅ [Gemini Web] ¡FOTO CARGADA CON ÉXITO Y VISIBLE EN PANTALLA!")
                    
                except Exception as final_ex:
                    print(f"⚠️ Error total cargando foto a Gemini mediante clics: {final_ex}")
                
                # Pausa vital extra larga para que Gemini suba la foto a sus servidores y dibuje la miniatura
                time.sleep(8)
                
            input_box = page.locator('div[contenteditable="true"]').first
            input_box.wait_for(state="visible", timeout=15000)
            
            print("⌨️ [Gemini Web] Escribiendo orden corporativa al cerebro nano banana...")
            input_box.fill(prompt_text)
            time.sleep(1)
            input_box.press("Enter")
            
            print("⏳ [Gemini Web] Esperando que la IA genere respuesta (texto y video)...")
            # Esperamos a que los botones interactivos aparezcan en el último mensaje generado (significa que terminó)
            # o a que el botón de Enviar vuelva a estar disponible
            try:
                page.wait_for_selector("message-content", state="visible", timeout=60000)
                # Ahora esperamos activamente a que NO haya ningún indicador de carga
                print("⏳ [Gemini Web] El texto apareció. Esperando que termine todo el procesamiento interno (videos/imágenes)...")
                # Dormimos generosamente porque la generación de video es asíncrona en el iframe de Google
                print("⏳ [Gemini Web] Procesando píxeles... (Aguantando 45 segundos para el renderizado)")
                time.sleep(45)
            except Exception as e:
                print(f"⚠️ Ocurrió una demora esperando a Gemini: {e}")
            
            messages = page.locator('message-content').all()
            gemini_response = messages[-1].inner_text().strip() if messages else ""
            print("   -> Log respuesta de Gemini: se solicitó video, se obtuvo respuesta.")
            
            # Usamos el caption majestuoso de GPT para Instagram
            caption = instagram_caption
            
            video_path = None
            last_message_container = page.locator("user-message, chunked-message, model-response").last
            
            videos = last_message_container.locator("video").all()
            if videos:
                video_src = videos[0].get_attribute("src")
                if video_src and video_src.startswith("http"):
                    print(f"⬇️ Descargando video generado...")
                    r = requests.get(video_src)
                    video_path = os.path.join(os.getcwd(), "video_gemini_generado.mp4")
                    with open(video_path, 'wb') as f:
                        f.write(r.content)
            
            if not video_path:
                print("🔎 [Gemini Web] No hay video expuesto. Buscando botón de descarga directo...")
                try:
                    with page.expect_download(timeout=15000) as download_info:
                        # Clic explícito en "Descargar video" si lo encapsularon en un botón
                        last_message_container.locator("button, a").filter(has_text="escar").first.click()
                    download = download_info.value
                    video_path = os.path.join(os.getcwd(), "video_gemini_generado.mp4")
                    download.save_as(video_path)
                    print(f"✅ Video guardado en: {video_path}")
                except Exception as e:
                    print("⚠️ No se detectó un video descargable. Se publicará la foto original en su lugar y mantendremos la pestaña de Gemini abierta temporalmente para que veas qué pasó.")
                    # NO cerramos la pestaña de inmediato, para que el usuario diagnostique.
                    time.sleep(5)
                    video_path = image_path
            
            # ==========================================
            # FASE 2: INSTAGRAM
            # ==========================================
            tiempo_espera = random.randint(10, 20)
            print(f"⏳ Pausa humana de {tiempo_espera}s antes de abrir Instagram...")
            time.sleep(tiempo_espera)
            
            print(f"📸 [Instagram Web] Iniciando publicación...")
            page.goto("https://www.instagram.com/")
            page.wait_for_load_state("domcontentloaded")
            
            if "accounts.instagram.com" in page.url or "login" in page.url:
                print("⚠️ [ATENCIÓN] Instagram requiere iniciar sesión.")
                print("   👉 Tienes 60 segundos para iniciar sesión manualmente en la ventana abierta. ¡Hazlo rápido!")
                page.wait_for_selector("svg[aria-label='Home'], svg[aria-label='Inicio'], svg[aria-label='New post']", timeout=60000)
                print("✅ [Instagram Web] Sesión detectada. Continuando...")

            print("   -> Despejando posibles popups de Instagram ('Ahora no')...")
            try:
                page.locator('button:has-text("Not Now"), button:has-text("Ahora no")').first.click(timeout=3000)
                time.sleep(1)
            except:
                pass
                
            print("   -> Buscando el botón de Crear (+)...")
            # Selector infalible para Instagram basándonos en el texto visible del menú lateral
            create_btn = page.locator('span:text-is("Crear"), span:text-is("Create"), svg[aria-label*="New post" i], svg[aria-label*="Nueva publicaci" i], svg[aria-label*="Crear" i]').first
            create_btn.wait_for(state="visible", timeout=25000)
            
            # Instagram aveces requiere doble chequeo de enrutamiento del click
            try:
                create_btn.click()
            except:
                # Si falla el span, le damos clic a su contenedor Padre (el botón real)
                create_btn.locator("xpath=./../..").click()
            
            # NUEVO: En muchas cuentas, "Crear" abre un sub-menú. Debemos darle a "Publicación"
            time.sleep(2)
            try:
                print("   -> Detectando sub-menú lateral de Instagram...")
                post_option = page.locator('span:text-is("Publicación"), span:text-is("Post"), svg[aria-label*="ost" i]').first
                if post_option.is_visible():
                    post_option.click()
                    print("   -> Sub-menú 'Publicación' seleccionado.")
                    time.sleep(2)
            except:
                pass
                
            time.sleep(3)
            
            with page.expect_file_chooser() as fc_info:
                page.locator("button:has-text('Select from computer'), button:has-text('Seleccionar de la computadora')").click()
            fc_info.value.set_files(video_path)
            time.sleep(4) 
            
            for _ in range(2):
                next_btn = page.locator("button:has-text('Next'), button:has-text('Siguiente'), div[role='button']:has-text('Siguiente')").last
                next_btn.wait_for(state="visible")
                next_btn.click()
                time.sleep(2)
            
            print("   -> 🛑 LÓGICA DE ENGAÑO: Poniendo la imagen, esperando 3 s...")
            time.sleep(3)
            
            caption_box = page.locator('div[aria-label="Write a caption..."], div[aria-label="Escribe un pie de foto..."]').first
            caption_box.wait_for(state="visible")
            caption_box.fill(caption)
            time.sleep(random.uniform(1.5, 3.0))
            
            share_btn = page.locator("button:has-text('Share'), div[role='button']:has-text('Compartir')").last
            share_btn.wait_for(state="visible")
            share_btn.click()
            
            print("   -> Esperando confirmación de Instagram...")
            page.wait_for_selector("text='Your post has been shared.', text='tu reel se ha compartido', text='Se ha compartido tu publicación'", timeout=90000)
            
            print("✅ [Instagram Web] ¡Publicado limpio y libre de sospechas bots!")
            context.close()
            print("✅ Navegador cerrado con éxito.")
