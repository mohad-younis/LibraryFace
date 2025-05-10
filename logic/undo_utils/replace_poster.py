import os
from core.config import Path
from annotated_types import T
from logic.general_utils.file_system import clear_icon_cache
from logic.general_utils.icon import set_folder_icon
from logic.iconify_utils.convert import convert_to_ico
from logic.iconify_utils.rename import move_existing_icons
from ui.helpers.logs import add_log
import requests
from ui import state

def replace_poster(folder, url, name):

    jpg_path, ico_path = move_existing_icons(folder, name)

    jpg_delete = True
    ico_delete = True

    # Remove desktop.ini if exists
    ini_path = os.path.join(folder, "desktop.ini")
    if os.path.exists(ini_path):
        try:
            os.chmod(ini_path, 0o666)
            os.remove(ini_path)
            add_log(f"Removing desktop.ini")
        except Exception as e:
            add_log(f"[ERROR] Couldn't remove desktop.ini: {e}")

    # Delete old .jpg/.ico files if needed
    for file in os.listdir(folder):
        full_path = os.path.join(folder, file)

        if jpg_delete and file.lower().endswith((".jpg", ".jpeg")):
            try:
                os.chmod(full_path, 0o666)
                os.remove(full_path)
                add_log(f"🗑 Deleted JPG: {file}")
            except Exception as e:
                add_log(f"[ERROR] Couldn't delete JPG: {e}")

        elif ico_delete and file.lower().endswith(".ico"):
            try:
                os.chmod(full_path, 0o666)
                os.remove(full_path)
                add_log(f"🗑 Deleted ICO: {file}")
            except Exception as e:
                add_log(f"[ERROR] Couldn't delete ICO: {e}")

    # Download new image
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        with open(jpg_path, "wb") as f:
            f.write(response.content)
        add_log("✅ Downloaded new poster")
    except Exception as e:
        add_log(f"[ERROR] Couldn't download image: {e}")
        return

    # Convert and apply
    if convert_to_ico(jpg_path, ico_path):
        set_folder_icon(folder, jpg_path, ico_path)
        clear_icon_cache()
        add_log("🎯 Applied new poster as icon")
    else:
        add_log("[ERROR] Failed to convert image to icon")

def replace_changes(to_replace):
    for poster in to_replace:
        preview_name = poster["old_title"]
        clean_title = poster["clean_title"]
        jpg_path = poster["jpg_path"]
        folder = Path(jpg_path).parent if jpg_path else None
        if state.show_rename_edit:
            name = clean_title
        else:
            name = preview_name
        url = poster.get("new_poster_url")
        if folder and url and name:
            replace_poster(folder, url, name)