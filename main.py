import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

# © 2026 ceob68 / Vaultly. All rights reserved.
# Unauthorized copying, distribution or modification is prohibited.

def main():
    app = QApplication(sys.argv)
    
    # Load stylesheet
    try:
        qss_path = os.path.join(os.path.dirname(__file__), 'ui', 'styles', 'theme.qss')
        with open(qss_path, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Warning: Could not load stylesheet - {e}")

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
