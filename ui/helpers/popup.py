from core.config import Toplevel, ctk, tk, root
from ui import layout
from ui.popup_layout import build_choice_popup

def show_choice_popup(normalized: str) -> str:
    result_holder = {"choice": "Skipped"}
    parent = layout.main_container.winfo_toplevel()

    def on_choice(result):
        result_holder["choice"] = result

    # Create the modal popup
    build_choice_popup(parent, normalized, on_choice)
    
    return result_holder["choice"]