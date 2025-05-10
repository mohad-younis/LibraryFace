from ui import layout
from ui import expand_layout

def hide_expand_window():
    if expand_layout.expand_container:
        expand_layout.expand_container.destroy()
        expand_layout.expand_container = None
    layout.main_container.pack(fill="both", expand=True, padx=0, pady=0)

def refresh_expand_window():
    from ui.expand_layout import build_expand_window
    if expand_layout.expand_container:
        expand_layout.expand_container.destroy()
    build_expand_window()

