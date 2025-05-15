from core.config import messagebox, Path
import core.config as config

from logic.undo_utils.replace_poster import replace_changes
from ui import layout
from ui import state
from logic.undo_utils.undo_iconify import undo_iconify, rename_changes, undo_changes
from ui.helpers.expand_helper import hide_expand_window, refresh_expand_window
from ui.helpers.logs import add_log
from ui.handlers.preview import show_next_poster, show_prev_poster, refresh_current_poster

def on_undo_click():
    if not state.preview_posters or state.current_index >= len(state.preview_posters):
        add_log("⚠️ Nothing to undo. Run iconify first.")
        return

    try:
        current_poster = state.preview_posters[state.current_index]
        jpg_path = current_poster["jpg_path"]
        # Fix: Use consistent key naming with fallbacks
        preview_name = current_poster.get("old_title", current_poster.get("preview_name", "Unknown"))
        # Fix: Use content_type as primary key with selected_type as fallback
        selected_type = current_poster.get("content_type", current_poster.get("selected_type", "Unknown"))

        confirm = messagebox.askyesno(
            "Confirm Undo",
            f"Are you sure you want to undo changes applied on:\n\n{preview_name}?"
        )
        if not confirm:
            add_log("Undo cancelled.")
            setattr(config, "undoing", False)
            return

        undo_iconify(current_poster)

        state.preview_posters.pop(state.current_index)
        
        # Adjust current_index if needed to stay in bounds
        if state.preview_posters:
            if state.current_index >= len(state.preview_posters):
                state.current_index = len(state.preview_posters) - 1
            
            # Just refresh the current poster without trying to navigate
            refresh_current_poster()
        else:
            layout.preview_buttons_frame.pack_forget()
            layout.folder_name_label.configure(text=f'Folder Name:')
            layout.clean_title_label.configure(text=f'Clean Title:')
            layout.type_label.configure(text=f'Content Type:')

    except Exception as e:
        add_log(f"⚠️ Error while undoing changes: {str(e)}")
        setattr(config, "undoing", False)

def on_apply_changes():
    to_undo = []
    to_rename = []

    confirm = messagebox.askyesno(
        "Apply Changes",
        f"Are you sure you want to proceed with these changes?"
    )
    if confirm:
        for poster in state.preview_posters:
            jpg_path = poster["jpg_path"]
            preview_name = poster["old_title"]
            clean_title = poster["clean_title"]
            content = poster["content_type"]
            title_var = poster["title_var"]
            undo_var = poster["undo_var"]

            folder_path = str(Path(jpg_path).parent)
            current_title = title_var.get().strip()

            if undo_var.get():
                to_undo.append(poster)

            elif current_title != clean_title:
                to_rename.append({
                    "jpg_path": jpg_path,
                    "old_name": preview_name,
                    "new_title": current_title
                })

        replace_changes(state.to_replace)

        undo_changes(to_undo)

        state.preview_posters = [
            p for p in state.preview_posters
            if not p["undo_var"].get()
        ]

        rename_changes(to_rename)

        # Clear the list after applying
        state.to_replace.clear()

        state.select_all_undo_var.set(False)
        
        if not state.preview_posters:
            hide_expand_window()
            layout.preview_buttons_frame.pack_forget()
            layout.folder_name_label.configure(text=f'Folder Name:')
            layout.clean_title_label.configure(text=f'Clean Title:')
            layout.type_label.configure(text=f'Content Type:')
        else:
            refresh_expand_window()
            # Adjust current_index if needed to stay in bounds
            if state.current_index >= len(state.preview_posters):
                state.current_index = len(state.preview_posters) - 1
            # Just refresh the current poster without trying to navigate
            refresh_current_poster()
    else:
        return
