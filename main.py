from src.core.assistant import VoiceAssistant
import sys

def main():
    try:
        app = VoiceAssistant()
        app.run()
    except KeyboardInterrupt:
        print("\nApagando asistente...")
        sys.exit(0)

if __name__ == "__main__":
    main()