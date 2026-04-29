import os
from faster_whisper import WhisperModel
from .config_manager import ConfigManager

# © 2026 ceob68 / Vaultly. All rights reserved.
# Unauthorized copying, distribution or modification is prohibited.

class WhisperService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WhisperService, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.config_manager = ConfigManager()
        return cls._instance

    def load_model(self, force_reload=False):
        cfg = self.config_manager.config
        if self.model is None or force_reload:
            try:
                models_dir = os.path.join(os.path.expanduser("~"), ".voxapro", "models")
                os.makedirs(models_dir, exist_ok=True)
                
                self.model = WhisperModel(
                    model_size_or_path=cfg["model_size"],
                    device=cfg["device"],
                    compute_type=cfg["compute_type"],
                    download_root=models_dir
                )
            except Exception as e:
                raise RuntimeError(f"Failed to load Whisper model: {e}")

    def transcribe(self, audio_path: str, language=None, progress_callback=None):
        if self.model is None:
            self.load_model()
            
        cfg = self.config_manager.config
        lang = language if language else cfg.get("language")
        
        segments, info = self.model.transcribe(
            audio_path,
            language=lang,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
        results = []
        total_duration = info.duration
        
        for segment in segments:
            results.append({
                "id": segment.id,
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
            
            if progress_callback and total_duration > 0:
                percent = min(100, int((segment.end / total_duration) * 100))
                progress_callback(percent, segment.text.strip())
                
        return {
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "segments": results
        }
