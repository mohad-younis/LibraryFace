
from ast import If
from core.config import (
    threading, messagebox, 
    root,
    ACCENT_COLOR, DISABLED_COLOR
)
import core.config as config

from logic.general_utils.file_system import clear_icon_cache

from ui import layout
from ui import state
from ui.handlers.preview import load_preview_list
from ui.helpers.logs import add_log
from ui.handlers.run_modes import run_deiconify, run_iconify


def toggle_log():
    state.log_expanded = not state.log_expanded

    if state.log_expanded:
        layout.content_frame.pack(padx=20, pady=(10, 20), fill="both", expand=True)
        layout.toggle_log_btn.configure(text="Hide Details ▲")
    else:
        layout.content_frame.pack_forget()
        layout.toggle_log_btn.configure(text="Show Details ▼")

    root.update_idletasks()
    if state.log_expanded:
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")
    else:
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight() + 20}")


def on_start():
    if not config.is_processing:
        if state.path_var.get() == "":
            messagebox.showerror("Error", "Please select a target folder")
            return

        mode = state.mode_var.get()
        if mode not in ["  Iconify  ", " Deiconify "]:
            messagebox.showerror("Error", "Please select a mode before starting.")
            return

        config.is_processing = True
        config.paused = False
        config.paused_event.set()
        config.stop_requested = False

        layout.stop_btn.pack(side="left", padx=(10, 0))

        if config.paused:
            config.paused_event.clear()
            layout.start_btn.configure(text="▶ Resume", fg_color=ACCENT_COLOR)
            add_log("⏸ Process paused.")

        layout.start_btn.configure(state="normal", text="⏸ Pause", fg_color=DISABLED_COLOR)
        layout.progress_frame.pack(fill="x", padx=20, pady=(10, 0))
        layout.progress_value.set(0)

        if not state.log_expanded:
            toggle_log()

        state.show_rename_edit = state.rename_folders_var.get()
        
        state.set_content_type = state.content_type_var.get()

        layout.undo_btn.grid_forget()
        layout.prev_btn.grid_forget()
        layout.counter_label.grid_forget()
        layout.next_btn.grid_forget()
        layout.expand_btn.grid_forget()
        layout.folder_name_label.configure(text=f'Folder Name:')
        layout.clean_title_label.configure(text=f'Clean Title:')
        layout.type_label.configure(text=f'Content Type:')

        thread = threading.Thread(target={
            "  Iconify  ": run_iconify,
            " Deiconify ": run_deiconify,
        }[mode])

        if not state.show_rename_edit:
            layout.clean_title_label.pack_forget()
        if state.show_rename_edit:
            layout.folder_name_label.pack_forget()
            layout.clean_title_label.pack_forget()
            layout.type_label.pack_forget()
            layout.folder_name_label.pack(anchor="w", pady=(0, 5))
            layout.clean_title_label.pack(anchor="w", pady=(0, 5))
            layout.type_label.pack(anchor="w", pady=(0, 20))
            
        thread.daemon = True
        thread.start()

    else:
        config.paused = not config.paused
        if config.paused:
            config.paused_event.clear()
            layout.start_btn.configure(text="▶ Resume", fg_color=ACCENT_COLOR)
            add_log("⏸ Process paused.")
        else:
            config.paused_event.set()
            layout.start_btn.configure(text="⏸ Pause", fg_color=DISABLED_COLOR)
            add_log("▶ Resuming...")

def on_stop():
    confirm = messagebox.askyesno(
        "Process Termination",
        f"Are you sure you want to stop the process, some folders might not get iconifyed?"
    )
    if confirm:
        config.stop_requested = True
        config.paused_event.set()  # resume if paused
        config.paused = False
        config.is_processing = False

        layout.start_btn.configure(state="normal", text="▶ Start Process", fg_color=ACCENT_COLOR)
        layout.stop_btn.pack_forget()
        add_log("⏹ Process stopped: some folders might not be iconifyed.")
        clear_icon_cache()
        add_log("Done iconifying all folders.")
        load_preview_list()
    else:
        return
    

