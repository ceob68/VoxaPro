from PySide6.QtCore import QThread, Signal
from core.whisper_service import WhisperService
import os

# © 2026 ceob68 / Vaultly. All rights reserved.

class TranscriptionWorker(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, audio_path, language=None):
        super().__init__()
        self.audio_path = audio_path
        self.language = language

    def run(self):
        try:
            service = WhisperService()
            
            def callback(percent, text):
                self.progress_updated.emit(percent, text)
                
            result = service.transcribe(
                self.audio_path, 
                language=self.language, 
                progress_callback=callback
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
