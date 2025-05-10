from core.config import os, Path
import core.config as config

from logic.general_utils.file_system import folder_refresh
from logic.iconify_utils.rename import move_existing_icons, rename_folder

from ui import state
from ui.helpers.logs import add_log

debug = False

def undo_iconify(poster):
    jpg_path = poster["jpg_path"]
    # Fix: Use get() method with fallbacks for both keys
    preview_name = poster.get("old_title", poster.get("preview_name", "Unknown"))
    # Fix: Use content_type as primary key with selected_type as fallback
    selected_type = poster.get("content_type", poster.get("selected_type", "Unknown"))

    if debug:
        add_log(f"[DEBUG] Target JPG path: {jpg_path}")

    folder = Path(jpg_path).parent
    if not folder.exists():
        if debug:    
            add_log(f"[DEBUG] Target folder doesn't exist: {folder}")
        return

    # Delete desktop.ini
    ini_file = folder / "desktop.ini"
    if ini_file.exists():
        try:
            os.chmod(ini_file, 0o666)
            ini_file.unlink()
            if debug:
                add_log("🗑️ Removed desktop.ini")
        except Exception as e:
            if debug:
                add_log(f"⚠️ Failed to remove desktop.ini: {e}")
    else:
        if debug:
            add_log(f"⚠️ ini not found: {jpg_path}")

    # Delete .ico file
    found_ico = False
    for file in folder.glob("*.ico"):
        found_ico = True
        try:
            os.chmod(file, 0o666)
            file.unlink()
            if debug:
                add_log(f"🗑️ Removed {file.name}")
        except Exception as e:
            if debug:
                add_log(f"⚠️ Failed to remove {file.name}: {e}")
    if not found_ico:
        if debug:
            add_log(f"⚠️ ico not found: {jpg_path}")

    # Delete .jpg poster
    jpg_path = Path(jpg_path)
    if jpg_path.exists():
        try:
            os.chmod(jpg_path, 0o666)
            jpg_path.unlink()
            if debug:
                add_log("🗑️ Removed poster")
        except Exception as e:
            if debug:
                add_log(f"⚠️ Failed to delete poster: {e}")
    else:
        if debug:
            add_log(f"⚠️ Poster not found: {jpg_path}")

    # Rename folder back if renamed
    if folder.name != preview_name:
        try:
            restored_path = folder.parent / preview_name
            os.rename(folder, restored_path)
            if debug:
                add_log(f"↩️ Renamed back to: {restored_path}")
        except Exception as e:  
            if debug:
                add_log(f"⚠️ Failed to rename folder: {e}")
    else:
        if debug:
            add_log(f"↩️ No rename needed: {preview_name}")

    add_log(f"Changes are undone for: {preview_name}")

def undo_changes(to_undo):
    if not to_undo:
        return
    
    for poster in to_undo:
        to_be_removed = []
        try:
            undo_iconify(poster)

            to_be_removed.append(poster)

        except Exception as e:
            add_log(f"❌ Undo failed: {e}")

    for poster in to_be_removed:
        to_undo.remove(poster)


def rename_changes(to_rename):
    if not to_rename:
        return
    
    for item in to_rename:
        to_be_removed = []
        jpg_path = item["jpg_path"]
        folder = str(Path(jpg_path).parent)
        
        old = item["old_name"]
        new = item.get("new_title", item.get("new_name", old))

        try:
            folder = rename_folder(folder, old, new)
            move_existing_icons(folder, new)

            # ✅ Update the corresponding poster in preview_posters
            for poster in state.preview_posters:
                poster_folder = str(Path(poster["jpg_path"]).parent)
                if poster_folder == str(Path(jpg_path).parent):  # Match the folder before rename
                    # Update fields
                    poster["clean_title"] = new
                    poster["jpg_path"] = os.path.join(
                        str(Path(folder)), new + ".jpg"
                    )


            ini_path = os.path.join(folder, "desktop.ini")
            if os.path.exists(ini_path):
                try:
                    os.system(f'attrib -s -h "{ini_path}"')
                    with open(ini_path, "r") as f:
                        lines = f.readlines()
                    with open(ini_path, "w") as f:
                        for line in lines:
                            if line.lower().startswith("iconresource"):
                                f.write(f"IconResource={new}.ico,0\n")
                            else:
                                f.write(line)
                    os.system(f'attrib +s +h "{ini_path}"')
                except Exception as e:
                    add_log(f"Failed to update desktop.ini: {str(e)}")

            folder_refresh(folder)
            add_log(f"Renamed '{old}' → '{new}'")
            to_be_removed.append(item)
        except Exception as e:
            add_log(f"Rename failed for '{old}': {str(e)}")

    for item in to_be_removed:
        to_rename.remove(item)
