from core.config import root

from ui import layout

def add_log(text):
    layout.log_box.configure(state="normal")
    layout.log_box.insert("end", f"{text}\n")
    layout.log_box.see("end")
    layout.log_box.configure(state="disabled")
    root.update()

def update_progress(current, total):
    fraction = current / total

    def update_ui():
        layout.progress_value.set(fraction)
        layout.progress_text.configure(text=f"{int(fraction * 100)}% ({current}/{total})")
        layout.progress_bar.update_idletasks()

    root.after(0, update_ui)
