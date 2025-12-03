
import asyncio
import edge_tts
import pygame
import os


class TextToSpeechService:
    def __init__(self):
        self.voice = "es-PE-CamilaNeural" 
        self.output_file = "response.mp3"
        pygame.mixer.init()

    async def _generate_audio(self, text):
        """Genera el archivo de audio usando Edge TTS (async interno)."""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(self.output_file)

    def speak(self, text: str):
        """Convierte texto a voz natural y lo reproduce."""
        if not text:
            return

        print("🔊 Generando voz...")
        
        try:
            asyncio.run(self._generate_audio(text))
        except Exception as e:
            print(f"Error generando audio: {e}")
            return
        try:
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"Error reproduciendo audio: {e}")