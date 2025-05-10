from ui import layout
from ui.expand_layout import build_expand_window

def show_expand_window():
    layout.main_container.pack_forget()
    build_expand_window()
