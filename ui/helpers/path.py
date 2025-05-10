from core.config import (
    filedialog, Path, 
    ACCENT_COLOR, TEXT_SECONDARY
)
from ui import layout
from ui import state

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        # Set full path
        state.path_var.set(folder)

        # Format shortened display path
        short_path = str(Path(folder).expanduser())
        if len(short_path) > 50:
            short_path = "..." + short_path[-47:]
        layout.path_display.configure(text=short_path, text_color=ACCENT_COLOR)


def update_path_display_hint(*_):
    if not state.path_var.get():
        if state.apply_to_subfolders.get():
            layout.path_display.configure(
                text="Changes will be applied to all subfolders in the selected folder",
                text_color=TEXT_SECONDARY
            )
        else:
            layout.path_display.configure(
                text="Changes will be applied only to the selected folder",
                text_color=TEXT_SECONDARY
            )
