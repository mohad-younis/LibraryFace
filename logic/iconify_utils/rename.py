from core.config import os

from ui import state
from ui.helpers.logs import add_log


def rename_folder(folder, original_name, final_folder_name):
    if state.show_rename_edit and final_folder_name and final_folder_name != original_name:
        parent_dir = os.path.dirname(folder)
        new_path = os.path.join(parent_dir, final_folder_name)
        try:
            if not os.path.exists(new_path):
                os.rename(folder, new_path)
                add_log(f"Renaming folder: {final_folder_name}")
                state.undo_map[new_path] = original_name
                folder = new_path
            else:
                add_log(f"! Folder '{final_folder_name}' already exists")
        except Exception:
            add_log(f"Renaming failed: {original_name}")
    return folder

def move_existing_icons(folder, name):
    jpg = os.path.join(folder, f"{name}.jpg")
    ico = os.path.join(folder, f"{name}.ico")
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if file.lower().endswith(('.jpg', '.jpeg')) and file != f"{name}.jpg":
            if os.path.exists(jpg):
                os.remove(jpg)
            os.rename(file_path, jpg)
        elif file.lower().endswith('.ico') and file != f"{name}.ico":
            if os.path.exists(ico):
                os.remove(ico)
            os.rename(file_path, ico)
    return jpg, ico
