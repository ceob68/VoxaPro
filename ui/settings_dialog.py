from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt

# © 2026 ceob68 / Vaultly. All rights reserved.

class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración")
        self.resize(400, 300)
        self.config_manager = config_manager
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1A1A2E;
                color: white;
            }
            QLabel {
                color: #E0E0E0;
                font-family: 'Segoe UI', Arial;
                font-size: 14px;
            }
            QComboBox {
                background-color: rgba(0, 0, 0, 0.4);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Model Size
        model_layout = QHBoxLayout()
        model_label = QLabel("Tamaño del Modelo (IA):")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large-v3"])
        self.model_combo.setCurrentText(self.config_manager.get("model_size"))
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)

        # Device
        device_layout = QHBoxLayout()
        device_label = QLabel("Dispositivo:")
        self.device_combo = QComboBox()
        self.device_combo.addItems(["cpu", "cuda", "auto"])
        self.device_combo.setCurrentText(self.config_manager.get("device"))
        device_layout.addWidget(device_label)
        device_layout.addWidget(self.device_combo)
        layout.addLayout(device_layout)
        
        # Compute Type
        compute_layout = QHBoxLayout()
        compute_label = QLabel("Tipo de Precisión:")
        self.compute_combo = QComboBox()
        self.compute_combo.addItems(["int8", "float16", "float32"])
        self.compute_combo.setCurrentText(self.config_manager.get("compute_type"))
        compute_layout.addWidget(compute_label)
        compute_layout.addWidget(self.compute_combo)
        layout.addLayout(compute_layout)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_and_close)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("background: transparent; border: 1px solid rgba(255,255,255,0.3);")
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def save_and_close(self):
        new_config = {
            "model_size": self.model_combo.currentText(),
            "device": self.device_combo.currentText(),
            "compute_type": self.compute_combo.currentText()
        }
        self.config_manager.save_config(new_config)
        self.accept()
