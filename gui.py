import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                            QWidget, QPushButton, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QUrl
from PyQt6.QtGui import QFont, QColor

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

from src.core.assistant import VoiceAssistant

class AssistantThread(QThread):
    listening_signal = pyqtSignal()
    thinking_signal = pyqtSignal()
    speaking_signal = pyqtSignal(str) 
    finished_speaking_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self.is_running = True

    def run(self):
        """Ciclo de vida del asistente en segundo plano"""
        while self.is_running:
            self.listening_signal.emit()
            user_text = self.assistant.listen()

            if user_text:
                if "salir" in user_text.lower() or "adiós" in user_text.lower():
                    break
                
                self.thinking_signal.emit()
                ai_response = self.assistant.think(user_text)

                self.speaking_signal.emit(ai_response) 
                self.assistant.speak(ai_response)
                self.finished_speaking_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Avatar Interface - Python Pro (Video MP4)")
        self.setGeometry(100, 100, 500, 700)
        self.setStyleSheet("background-color: #1e1e2e;")

        self.idle_video_path = os.path.abspath("src/assets/Albert_idle.mp4")
        self.talking_video_path = os.path.abspath("src/assets/Albert_talking.mp4")

        self.assistant = VoiceAssistant()
        
        self.worker = AssistantThread(self.assistant) 

        self.init_ui()
        self.setup_media_player() 
        
        self.play_video("idle")

        self.setup_connections() 
        self.worker.start() 

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(460, 400)
        self.video_widget.setStyleSheet("background-color: #000; border: 2px solid #4e4e6e;")
        layout.addWidget(self.video_widget)

        self.status_label = QLabel("Iniciando...", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setStyleSheet("color: #89b4fa;")
        layout.addWidget(self.status_label)

        self.subtitle_label = QLabel("", self)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setFont(QFont("Segoe UI", 12))
        self.subtitle_label.setStyleSheet("background-color: #313244; color: #cdd6f4; padding: 15px; border-radius: 10px;")
        layout.addWidget(self.subtitle_label)

        self.btn_exit = QPushButton("Cerrar Asistente")
        self.btn_exit.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; border-radius: 10px; padding: 10px; font-weight: bold; } QPushButton:hover { background-color: #d20f39; }")
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit)

    def setup_media_player(self):
        """Configuración OPTIMIZADA para evitar conflictos de audio"""
        self.media_player = QMediaPlayer()
        
        self.media_player.setVideoOutput(self.video_widget)
        
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite)

    def play_video(self, mode):
        if mode == "idle":
            url = QUrl.fromLocalFile(self.idle_video_path)
        else:
            url = QUrl.fromLocalFile(self.talking_video_path)
            
        if self.media_player.source() != url:
            self.media_player.setSource(url)
            self.media_player.play()

    def setup_connections(self):
        self.worker.listening_signal.connect(self.on_listening)
        self.worker.thinking_signal.connect(self.on_thinking)
        self.worker.speaking_signal.connect(self.on_speaking)
        self.worker.finished_speaking_signal.connect(self.on_finished_speaking)

    def on_listening(self):
        self.status_label.setText("🎤 Escuchando...")
        self.status_label.setStyleSheet("color: #a6e3a1;")

    def on_thinking(self):
        self.status_label.setText("🧠 Pensando...")
        self.status_label.setStyleSheet("color: #fab387;")

    def on_speaking(self, text):
        self.status_label.setText("🗣️ Hablando...")
        self.status_label.setStyleSheet("color: #89b4fa;")
        self.subtitle_label.setText(text)
        self.play_video("talking")

    def on_finished_speaking(self):
        self.play_video("idle")

    def closeEvent(self, event):
        self.media_player.stop()
        if hasattr(self, 'worker'):
            self.worker.is_running = False
            self.worker.quit()
            self.worker.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())