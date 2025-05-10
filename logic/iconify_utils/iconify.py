from core.config import time, os, messagebox, Path
from customtkinter import StringVar, BooleanVar
import core.config as config

from .manual_selection import handle_manual_selection_queue
from .process import process

from logic.general_utils.connection import check_internet_conection
from logic.general_utils.file_system import clear_icon_cache, get_all_subfolders

from ui import state
from ui.helpers.logs import add_log, update_progress
from ui.handlers.preview import load_preview_list


debug = False
def iconify(folder=None):
    # Ensure all collections are properly initialized before clearing
    if state.undo_map is None:
        state.undo_map = {}
    else:
        state.undo_map.clear()
        
    if state.preview_posters is None:
        state.preview_posters = []
    else:
        state.preview_posters.clear()
    
    # Fix: Initialize the manual_selection_queue if it doesn't exist or is None
    if config.manual_selection_queue is None:
        config.manual_selection_queue = []
    else:
        config.manual_selection_queue.clear()
        
    target = folder or state.path_var.get()

    if not check_internet_conection():
        messagebox.showerror("Connection Error", "Internet connection lost. Cannot start the process.")
        config.is_processing = False
        return

    if not target or not os.path.isdir(target):
        messagebox.showerror("Error", "Please select a valid folder")
        config.is_processing = False
        return

    folders = [target] if not state.apply_to_subfolders.get() else get_all_subfolders(target)
    if not folders:
        add_log("No subfolders found to process.")
        config.is_processing = False
        return

    add_log("Checking for uniconified folders...")
    to_process = [f for f in folders if not is_iconified(f)]
    add_log(f"Folders to iconify: {len(to_process)}")

    if not to_process:
        messagebox.showinfo("Info", "All folders are already iconified.")
        config.is_processing = False
        return

    for i, folder in enumerate(to_process):
        add_log(f"Iconifying: {os.path.basename(folder)}")
        try:
            foder_path = Path(folder)
            if foder_path.is_dir():
                final_folder, selected, clean_title, anime_poster, tv_poster, movie_poster = process(folder, manual=False)
                update_progress(i + 1, len(to_process))
        except OSError as e:
            add_log(f"⚠️ Skipping folder '{folder}' due to access error: {e}")

        jpg_path = os.path.join(final_folder, os.path.basename(final_folder) + ".jpg")
        folder_path_str = str(folder)
        preview_name = state.undo_map.get(folder_path_str, Path(folder).name)

        if os.path.exists(jpg_path):
            state.preview_posters.append({
                "folder_path": folder,
                "jpg_path": jpg_path,
                "old_title": preview_name,
                "clean_title": clean_title,
                "content_type": selected,
                "title_var": StringVar(value=clean_title),
                "undo_var": BooleanVar(value=False),
                "anime_poster" : anime_poster, 
                "tv_poster" : tv_poster, 
                "movie_poster" : movie_poster
            })

    time.sleep(1)

    handle_manual_selection_queue()
    clear_icon_cache()
    add_log("Done iconifying all folders.")
    load_preview_list()

    return state.preview_posters

def is_iconified(folder_path):
    folder = Path(folder_path)
    files = [f.name.lower() for f in folder.iterdir() if f.is_file()]
    return "desktop.ini" in files and any(f.endswith(".ico") for f in files)
