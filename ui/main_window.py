import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
    QPushButton, QFileDialog, QProgressBar, QTextEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QDropEvent, QDragEnterEvent

from core.audio_processor import AudioProcessor
from ui.workers import TranscriptionWorker
from core.config_manager import ConfigManager

# © 2026 ceob68 / Vaultly. All rights reserved.

class DropZone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Arrastra tu archivo de audio/video aquí\no haz clic para buscar")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Segoe UI", 14))
        self.label.setStyleSheet("color: rgba(255,255,255,0.7);")
        
        self.layout.addWidget(self.label)
        self.setStyleSheet("""
            QWidget {
                border: 2px dashed rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                background-color: rgba(0, 0, 0, 0.2);
            }
            QWidget:hover {
                border: 2px dashed #8E2DE2;
                background-color: rgba(142, 45, 226, 0.1);
            }
        """)
        self.setMinimumHeight(200)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.window().process_file(file_path)

    def mousePressEvent(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Archivo", "", 
            "Media Files (*.mp4 *.mkv *.avi *.mp3 *.wav *.m4a *.flac);;All Files (*.*)"
        )
        if file_path:
            self.window().process_file(file_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voxa Pro - Transcripción Élite")
        self.resize(900, 650)
        self.config = ConfigManager()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setObjectName("mainContainer")

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        self.title_label = QLabel("VOXA PRO")
        self.title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        # Simulated gradient text in Qt using inline styling since rich text doesn't support complex gradients
        self.title_label.setStyleSheet("color: #00c6ff;")
        
        self.settings_btn = QPushButton("⚙️ Configuración")
        self.settings_btn.setFixedWidth(150)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_btn)
        
        self.main_layout.addLayout(header_layout)

        # Drop Zone
        self.drop_zone = DropZone(self)
        self.main_layout.addWidget(self.drop_zone)

        # Progress Area
        self.progress_container = QWidget()
        self.progress_layout = QVBoxLayout(self.progress_container)
        self.progress_layout.setContentsMargins(0,0,0,0)
        
        self.status_label = QLabel("Listo para transcribir.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.hide()
        
        self.progress_layout.addWidget(self.status_label)
        self.progress_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.progress_container)

        # Results Area
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("La transcripción aparecerá aquí...")
        self.main_layout.addWidget(self.result_text)
        
        # Action Buttons
        self.btn_layout = QHBoxLayout()
        self.save_txt_btn = QPushButton("💾 Guardar TXT")
        self.save_srt_btn = QPushButton("🎬 Guardar SRT")
        self.save_txt_btn.hide()
        self.save_srt_btn.hide()
        
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.save_txt_btn)
        self.btn_layout.addWidget(self.save_srt_btn)
        self.main_layout.addLayout(self.btn_layout)

        self.current_result = None

    def process_file(self, file_path):
        self.status_label.setText(f"Procesando: {os.path.basename(file_path)}")
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.result_text.clear()
        self.drop_zone.setEnabled(False)
        self.save_txt_btn.hide()
        self.save_srt_btn.hide()

        # Execute extraction after short delay to let UI update
        QTimer.singleShot(100, lambda: self._start_transcription(file_path))

    def _start_transcription(self, file_path):
        self.status_label.setText("Extrayendo audio optimizado...")
        QApplication.processEvents() # Force UI update
        
        output_dir = os.path.join(os.path.expanduser("~"), ".voxapro", "temp")
        
        try:
            audio_path = AudioProcessor.compress_to_audio(file_path, output_dir)
        except Exception as e:
            self.status_label.setText("Error en la extracción de audio.")
            self.result_text.setText(str(e))
            self.drop_zone.setEnabled(True)
            self.progress_bar.hide()
            return

        self.status_label.setText("Transcribiendo mediante IA local...")
        
        self.worker = TranscriptionWorker(audio_path)
        self.worker.progress_updated.connect(self._update_progress)
        self.worker.finished.connect(self._on_transcription_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _update_progress(self, percent, text):
        self.progress_bar.setValue(percent)
        self.status_label.setText(f"Transcribiendo... {text[:50]}...")

    def _on_transcription_finished(self, result):
        self.current_result = result
        self.progress_bar.setValue(100)
        self.status_label.setText(f"Completado en {result['duration']:.2f}s | Idioma detectado: {result['language']}")
        self.drop_zone.setEnabled(True)
        
        full_text = "\n".join([seg["text"] for seg in result["segments"]])
        self.result_text.setText(full_text)
        
        self.save_txt_btn.show()
        self.save_srt_btn.show()

    def _on_error(self, error_msg):
        self.status_label.setText("Error durante la transcripción")
        self.result_text.setText(error_msg)
        self.drop_zone.setEnabled(True)
        self.progress_bar.hide()
