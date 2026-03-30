import os
import tiktoken
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class BrainGPT:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("⚠️ No se encontró OPENAI_API_KEY.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
        
        try:
            self.encoder = tiktoken.encoding_for_model("gpt-4o-mini")
        except KeyError:
            self.encoder = tiktoken.get_encoding("cl100k_base")
            
        self.total_tokens_used = 0
        
        # Cargar configuración corporativa
        self.config_path = os.path.join(os.getcwd(), "empresa_config.json")
        self.company_data = self._load_company_config()

    def _load_company_config(self):
        if not os.path.exists(self.config_path):
            print("⚠️ No se encontró 'empresa_config.json'. Creando uno por defecto.")
            default_config = {
                "nombre_empresa": "Mi Empresa S.A.",
                "rubro": "Tecnología",
                "hashtags_fijos": "#Empresa #Tecnologia #VideoCorporativo #Innovacion",
                "datos_contacto": "Visita nuestra web: www.miempresa.com",
                "tono": "Profesional, entusiasta y corporativo."
            }
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            return default_config
            
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def generate_instagram_post(self, context_topic: str) -> str:
        """
        Crea el caption DIRECTAMENTE con GPT.
        """
        system_instruction = (
            "Eres el Community Manager Experto de la empresa.\n"
            f"DATOS DE LA EMPRESA:\n"
            f"- Nombre: {self.company_data.get('nombre_empresa')}\n"
            f"- Contacto: {self.company_data.get('datos_contacto')}\n"
            f"- Hashtags: {self.company_data.get('hashtags_fijos')}\n"
            f"- Tono: {self.company_data.get('tono')}\n\n"
            "MISION: Escribe el texto PERFECTO (Caption) para una publicación en Instagram "
            "sobre el tema que el usuario provea. Incluye llamadas a la acción, emojis, "
            "los hashtags de la empresa y respeta el tono de voz al pie de la letra. No saludes, no uses comillas."
        )
        
        user_message = f"Genera el texto maestro para publicar en Instagram (Caption) sobre el tema: '{context_topic}'."
        
        input_tokens = self.count_tokens(system_instruction + user_message)
        self.total_tokens_used += input_tokens
        
        if not self.client:
            return f"Descubre más sobre {context_topic}. {self.company_data.get('datos_contacto')} {self.company_data.get('hashtags_fijos')}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=400
            )
            
            answer = response.choices[0].message.content.strip()
            self.total_tokens_used += self.count_tokens(answer)
            return answer
            
        except Exception as e:
            print(f"❌ Error en OpenAI: {e}")
            return f"¡Nuevo contenido sobre {context_topic}! {self.company_data.get('hashtags_fijos')}"
