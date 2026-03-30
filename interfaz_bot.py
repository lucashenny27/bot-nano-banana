import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import scrolledtext
from threading import Thread
import os
import sys
import subprocess
import shutil
import json

# Redirigir la consola a un widget de texto
class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget
    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)
    def flush(self):
        pass

class BotDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Community Manager Bot - Futura Dashboard")
        self.root.geometry("750x650")
        self.root.configure(bg="#1E1E2E")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 11, 'bold'), padding=10)
        self.style.configure('TLabel', background="#1E1E2E", foreground="white", font=('Segoe UI', 10))
        
        # Título
        ttk.Label(root, text="🚀 Panel de Publicación Automática", font=('Segoe UI', 16, 'bold')).pack(pady=15)
        
        # Selección de archivo
        frame_file = tk.Frame(root, bg="#1E1E2E")
        frame_file.pack(fill='x', padx=40, pady=5)
        
        ttk.Label(frame_file, text="Foto a Procesar:").pack(side=tk.LEFT)
        self.file_path_var = tk.StringVar(value="No se seleccionó foto...")
        ttk.Label(frame_file, textvariable=self.file_path_var, foreground="#A6E3A1", font=('Segoe UI', 9, 'italic')).pack(side=tk.LEFT, padx=10)
        
        btn_browse = ttk.Button(frame_file, text="Seleccionar Foto 👀", command=self.browse_file)
        btn_browse.pack(side=tk.RIGHT)
        
        # Tema del Video
        frame_tema = tk.Frame(root, bg="#1E1E2E")
        frame_tema.pack(fill='x', padx=40, pady=5)
        ttk.Label(frame_tema, text="¿De qué trata este Post?:").pack(side=tk.LEFT)
        self.tema_var = tk.StringVar(value="nuestro impresionante trabajo corporativo")
        tk.Entry(frame_tema, textvariable=self.tema_var, width=35, font=('Segoe UI', 10)).pack(side=tk.RIGHT)
        
        # Acciones
        frame_actions = tk.Frame(root, bg="#1E1E2E")
        frame_actions.pack(pady=20)
        
        self.btn_run = ttk.Button(frame_actions, text="🔥 INICIAR PUBLICACIÓN", command=self.start_bot)
        self.btn_run.pack(side=tk.LEFT, padx=5)
        
        self.btn_config = ttk.Button(frame_actions, text="⚙️ Datos de Empresa", command=self.open_config)
        self.btn_config.pack(side=tk.LEFT, padx=5)
        
        self.btn_login = ttk.Button(frame_actions, text="🔐 Asegurar Logins", command=self.run_setup)
        self.btn_login.pack(side=tk.LEFT, padx=5)

        self.btn_kill = ttk.Button(frame_actions, text="🧹 Limpiar Navegador", command=self.kill_chrome)
        self.btn_kill.pack(side=tk.LEFT, padx=5)
        
        # Consola Visual
        ttk.Label(root, text="[Logs del Agente en Tiempo Real]").pack(anchor='w', padx=40)
        self.console = scrolledtext.ScrolledText(root, width=85, height=20, bg="#11111B", fg="#CBA6F7", font=('Consolas', 10))
        self.console.pack(padx=40, pady=5)
        
        # Redirigir el print de Python a la interfaz
        sys.stdout = TextRedirector(self.console)
        
        self.selected_file = None

    def browse_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if filepath:
            self.selected_file = filepath
            self.file_path_var.set(os.path.basename(filepath))
            
            # Reemplazar la foto maestra para el bot guardándola como test_image.jpg temporal
            target = os.path.join(os.getcwd(), 'test_image.jpg')
            import shutil
            shutil.copy(self.selected_file, target)
            print(f"✅ Foto fijada como objetivo maestro: {os.path.basename(target)}")

    def open_config(self):
        import json
        config_win = tk.Toplevel(self.root)
        config_win.title("⚙️ Datos de Tu Empresa")
        config_win.geometry("450x450")
        config_win.configure(bg="#1E1E2E")
        
        ttk.Label(config_win, text="Identidad e Información Corporativa", font=('Segoe UI', 13, 'bold')).pack(pady=10)
        
        try:
            with open("empresa_config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
        except:
            config = {
                "nombre_empresa": "Mi Empresa S.A.", "rubro": "Tecnología",
                "hashtags_fijos": "#Empresa #Tecnologia #VideoCorporativo",
                "datos_contacto": "Visita www.miempresa.com", "tono": "Profesional y corporativo."
            }
            
        entries = {}
        fields = [("Nombre Empresa:", "nombre_empresa"), ("Rubro / Sector:", "rubro"),
                  ("Hashtags Fijos:", "hashtags_fijos"), ("Datos de Contacto:", "datos_contacto"),
                  ("Tono de la IA:", "tono")]
        
        for label, key in fields:
            ttk.Label(config_win, text=label).pack(anchor='w', padx=30, pady=(5,0))
            ent = tk.Entry(config_win, width=50, font=('Segoe UI', 10))
            ent.insert(0, config.get(key, ""))
            ent.pack(padx=30, pady=2)
            entries[key] = ent
            
        def save_config():
            new_config = {k: e.get() for k, e in entries.items()}
            with open("empresa_config.json", "w", encoding="utf-8") as f:
                json.dump(new_config, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("¡Guardado!", "¡La Identidad de la Empresa se ha actualizado!")
            config_win.destroy()
            
        ttk.Button(config_win, text="💾 Guardar Todo", command=save_config).pack(pady=15)

    def run_setup(self):
        print("💡 Abriendo Navegador del Bot para comprobar Logins de Google e Instagram...")
        print("💡 Recuerda presionar ENTER en tu terminal cuando hayas iniciado sesión.")
        subprocess.run([sys.executable, "setup_sessions.py"])
        print("✅ Navegador de seguridad cerrado.")

    def kill_chrome(self):
        print("🧹 Intentando cerrar procesos de Chrome bloqueados...")
        try:
            # En Windows matamos todos los chrome.exe que estén usando el perfil del bot. 
            # Agregamos >NUL 2>&1 para que no muestre error si no hay ninguno abierto.
            os.system('taskkill /F /IM chrome.exe /T >NUL 2>&1')
            print("✅ Limpieza completada. Intenta iniciar la publicación ahora.")
            messagebox.showinfo("Limpieza", "Se han cerrado todos los procesos de Chrome. Ya puedes iniciar.")
        except Exception as e:
            print(f"❌ No se pudo completar la limpieza: {e}")

    def start_bot(self):
        if not self.selected_file and not os.path.exists('test_image.jpg'):
            messagebox.showwarning("Falta Foto", "Por favor, selecciona una foto arriba antes de lanzar el Bot.")
            return
            
        self.btn_run.config(state="disabled")
        print("==========================================")
        print("🔥 ACTIVANDO CEREBRO Y NAVEGADOR DEL AGENTE")
        print("==========================================")
        
        # Ejecutar en hilo separado para no congelar la UI pero en un proceso distinto
        def task():
            try:
                # Forzar UTF-8 para emojis en Windows
                env_utf8 = os.environ.copy()
                env_utf8["PYTHONIOENCODING"] = "utf-8"
                
                # Pasamos el tema del video como argumento a main.py
                process = subprocess.Popen(
                    [sys.executable, "main.py", self.tema_var.get()], 
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                    text=True, encoding='utf-8', env=env_utf8
                )
                for line in iter(process.stdout.readline, ''):
                    print(line, end="")
                process.wait()
            except Exception as e:
                print(f"\n❌ Error catastrófico en la consola: {e}")
            finally:
                self.root.after(0, lambda: self.btn_run.config(state="normal"))
                
        Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = BotDashboard(root)
    root.mainloop()
