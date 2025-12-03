import speech_recognition as sr
from colorama import Fore

class SpeechToTextService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        """Escucha el micrófono y devuelve texto."""
        with self.microphone as source:
            print(f"{Fore.YELLOW}Escuchando...{Fore.RESET}")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print(f"{Fore.CYAN}Procesando audio...{Fore.RESET}")
                text = self.recognizer.recognize_google(audio, language="es-ES")
                print(f"Usuario dijo: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("No entendí el audio.")
                return None
            except sr.RequestError:
                print("Error de conexión con el servicio de voz.")
                return None