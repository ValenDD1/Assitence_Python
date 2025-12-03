from src.services.llm_service import GeminiService
from src.services.stt_service import SpeechToTextService
from src.services.tts_service import TextToSpeechService
from colorama import Fore

class VoiceAssistant:
    def __init__(self):
        print(f"{Fore.GREEN}Iniciando asistente...{Fore.RESET}")
        self.llm = GeminiService()
        self.stt = SpeechToTextService()
        self.tts = TextToSpeechService()

    def listen(self):
        """Solo escucha una vez y retorna el texto"""
        print(f"{Fore.YELLOW}Escuchando...{Fore.RESET}")
        return self.stt.listen()

    def think(self, text):
        """Solo piensa y retorna la respuesta"""
        print(f"{Fore.CYAN}Procesando texto...{Fore.RESET}")
        return self.llm.get_response(text)

    def speak(self, text):
        """Solo habla el texto entregado"""
        print(f"{Fore.MAGENTA}Generando voz...{Fore.RESET}")
        self.tts.speak(text)