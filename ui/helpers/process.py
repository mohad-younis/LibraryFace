from core.config import root, ACCENT_COLOR, SUCCESS_COLOR
import core.config as config
from ui import layout

def on_process_complete():
    config.is_processing = False
    layout.start_btn.configure(state="normal", text="▶ Start Process", fg_color=ACCENT_COLOR)
    config.paused_event.set()
    layout.progress_value.set(100)
    layout.progress_bar.configure(progress_color=SUCCESS_COLOR)
    layout.progress_text.configure(text="Complete!")
    layout.stop_btn.pack_forget()
    config.stop_requested = False
    root.after(2000, lambda: layout.progress_bar.configure(progress_color=ACCENT_COLOR))

def check_pause():
    if config.stop_requested:
        raise StopIteration
    config.paused_event.wait()
