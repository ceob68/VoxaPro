import subprocess
import os
import uuid
import shutil

# © 2026 ceob68 / Vaultly. All rights reserved.
# Unauthorized copying, distribution or modification is prohibited.

class AudioProcessor:
    @staticmethod
    def is_ffmpeg_installed():
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def compress_to_audio(input_path: str, output_dir: str) -> str:
        """
        Comprime cualquier video o audio a 16kHz mono WAV usando FFmpeg.
        Retorna la ruta al archivo de audio comprimido temporal.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        filename = f"audio_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(output_dir, filename)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-loglevel", "error",
            output_path
        ]
        
        try:
            # En Windows se usa CREATE_NO_WINDOW para evitar flashes de consola
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            subprocess.run(
                cmd, 
                check=True, 
                capture_output=True, 
                text=True,
                startupinfo=startupinfo
            )
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg compression failed: {e.stderr}")
