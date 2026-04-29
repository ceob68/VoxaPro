import json
import os
from pathlib import Path

# © 2026 ceob68 / Vaultly. All rights reserved.
# Unauthorized copying, distribution or modification is prohibited.

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".voxapro"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "model_size": "base",
            "device": "cpu",
            "compute_type": "int8",
            "language": None,
            "export_srt": True,
            "export_txt": True
        }
        self.config = self.load_config()

    def load_config(self):
        if not self.config_file.exists():
            self._save(self.default_config)
            return self.default_config.copy()
        
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Merge with defaults
                merged = self.default_config.copy()
                merged.update(data)
                return merged
        except Exception:
            return self.default_config.copy()

    def save_config(self, new_config):
        self.config.update(new_config)
        self._save(self.config)

    def _save(self, data):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.config.get(key)
