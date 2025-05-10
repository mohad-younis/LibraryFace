from core.config import  os, Path, Tuple
import core.config as config

from .rename import move_existing_icons, rename_folder
from .convert import convert_to_ico
from .fetch_poster import fetch_and_download_poster, is_valid_poster

from logic.general_utils.icon import set_folder_icon
from logic.general_utils.file_system import folder_refresh
from logic.general_utils.connection import wait_for_internet
from logic.metadata_utils.build_title import build_titles

from ui import state
from ui.helpers.logs import add_log
from ui.helpers.process import check_pause

debug = False

def process(folder, manual=False) -> Tuple[str, str, str, str, str, str]:
    try:
        wait_for_internet()
        check_pause()
    
        original_name = os.path.basename(folder)
        check_pause()
        
        anime_title, tv_title, movie_title, content_type, final_folder_name, poster_url, anime_poster, tv_poster, movie_poster, matched_title = build_titles(original_name, manual=manual)
        final_folder_name = final_folder_name.title()

        check_pause()

        name = final_folder_name

        if content_type == "Skipped":
            skip_name = original_name or "Unknown"
            add_log(f"⏭ Skipping: {skip_name}")
            return folder, "Skipped", "", "", "", ""
        if content_type == "Unknown":
            add_log(f"? Unknown content: {original_name} (queued for manual selection)")
            config.manual_selection_queue.append((folder, original_name))
            return folder, "Unknown", name, "", "", ""
        elif content_type != "Unknown":
            folder = rename_folder(folder, original_name, final_folder_name)
            name = os.path.basename(folder)
        else:
            name = final_folder_name

        check_pause() 

        # Move existing icons
        jpg, ico = move_existing_icons(folder, name)

        wait_for_internet()
        check_pause()

        # Fetch poster
        valid_jpg = os.path.exists(jpg) and is_valid_poster(jpg)
        if not valid_jpg and not os.path.exists(ico):
            if content_type == "Anime":
                query = anime_title
            elif content_type == "TV Show":
                query = tv_title
            elif content_type == "Movies":
                query = movie_title
            else:
                query = final_folder_name
            folder_path_str = str(folder)
            preview_name = state.undo_map.get(folder_path_str, Path(folder).name)
            if fetch_and_download_poster(content_type, query, jpg, poster_url, preview_name, name, matched_title):
                check_pause()    
            else:
                folder = rename_folder(folder, final_folder_name, original_name)
                name = os.path.basename(folder)
                
        valid_jpg = os.path.exists(jpg) and is_valid_poster(jpg)
        if valid_jpg and not os.path.exists(ico):
            if not convert_to_ico(jpg, ico):
                add_log(f"Removing broken JPG: {jpg}")
                try:
                    os.remove(jpg)
                except:
                    pass
                return folder, content_type, name, anime_poster, tv_poster, movie_poster

        check_pause()

        # Apply icon
        success = set_folder_icon(folder, jpg, ico)
        if not success:
            return folder, content_type, name, anime_poster, tv_poster, movie_poster
        
        folder_refresh(folder)
        
        check_pause()
        return folder, content_type, name, anime_poster, tv_poster, movie_poster

    except StopIteration:
        raise
