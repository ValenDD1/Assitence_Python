import google.generativeai as genai
from src.config import Config

class GeminiService:
    def __init__(self):
        genai.configure(api_key=Config.API_KEY)
        model_name = 'gemini-2.5-flash'
        try:
            self.model = genai.GenerativeModel(model_name)
            self.chat = self.model.start_chat(history=[])
            print(f"Cerebro conectado usando: {model_name}")
        except Exception as e:
            print(f"Error al conectar modelo {model_name}, intentando con gemini-pro...")
            self.model = genai.GenerativeModel('gemini-pro')
            self.chat = self.model.start_chat(history=[])

    def get_response(self, prompt: str) -> str:
        try:
            full_prompt = f"Responde de forma conversacional, breve y útil: {prompt}"
            response = self.chat.send_message(full_prompt)
            return response.text
        except Exception as e:
            return f"Lo siento, hubo un error con mi cerebro: {e}"