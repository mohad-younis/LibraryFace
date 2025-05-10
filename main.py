# main
import customtkinter as ctk
from ui.layout import build_ui
from core.config import root
import json
import os

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".libraryface_settings.json")
def load_theme_from_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            settings = json.load(f)
            theme = settings.get("theme", "System")
            ctk.set_appearance_mode(theme)
    except Exception:
        ctk.set_appearance_mode("System")

load_theme_from_config()

def main():
    ctk.set_default_color_theme("blue")

    build_ui()

    root.mainloop()

if __name__ == "__main__":
    main()