from core.config import os, Path
from customtkinter import StringVar, BooleanVar
import core.config as config

from .process import process

from ui import state
from ui.helpers.logs import add_log
from ui.helpers.process import check_pause

def handle_manual_selection_queue():
    # Fix: Check if manual_selection_queue is None and initialize it if needed
    if config.manual_selection_queue is None:
        config.manual_selection_queue = []
        add_log("Fixed missing queue - no folders need manual selection.")
        return
        
    if not config.manual_selection_queue:
        return
    add_log("Resolving unknown folders...")
    for folder_path, raw_title in config.manual_selection_queue:
        try:
            check_pause()

            final_folder, content_type, clean_title, anime_poster, tv_poster, movie_poster = process(folder_path, manual=True)
                
            jpg_path = os.path.join(final_folder, os.path.basename(final_folder) + ".jpg")
            folder_path_str = str(final_folder)
            preview_name = state.undo_map.get(folder_path_str, Path(final_folder).name)

            if os.path.exists(jpg_path):
                state.preview_posters.append({
                    "folder_path": folder_path,
                    "jpg_path": jpg_path,
                    "old_title": preview_name,
                    "clean_title": clean_title,
                    "content_type": content_type,
                    "title_var": StringVar(value=clean_title),
                    "undo_var": BooleanVar(value=False),
                    "anime_poster" : anime_poster, 
                    "tv_poster" : tv_poster, 
                    "movie_poster" : movie_poster
                })

        except StopIteration:
            add_log("Process terminated early by user.")
            return
        except Exception as e:
            add_log(f"⚠️ Failed during manual folder handling: {e}")
