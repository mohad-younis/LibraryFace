from core.config import( 
    os, subprocess, messagebox, 
    CREATE_NO_WINDOW
)

from logic.general_utils.file_system import clear_icon_cache, get_all_subfolders

from ui import state
from ui.helpers.logs import add_log, update_progress
from ui.helpers.process import check_pause

def deiconify():
    target_dir = state.path_var.get()
    if not target_dir or not os.path.isdir(target_dir):
        messagebox.showerror("Error", "Please select a valid folder")
        return

    jpg_delete = state.jpg_var.get()
    ico_delete = state.ico_var.get()
    visibility = state.visibility_var.get()

    folders = [target_dir] if not state.apply_to_subfolders.get() else get_all_subfolders(target_dir)
    if not folders:
        add_log("No subfolders found to process.")
        return
    
    add_log(f"Found {len(folders)} folders to process")
    check_pause()
    for i, folder in enumerate(folders):
        folder_name = os.path.basename(folder)
        add_log(f"Deiconifying: {folder_name}")

        check_pause()

        ini_path = os.path.join(folder, "desktop.ini")
        if os.path.exists(ini_path):
            check_pause()
            try:
                os.chmod(ini_path, 0o666)
                os.remove(ini_path)
                add_log(f"Removing desktop.ini")
            except Exception as e:
                add_log(f"[ERROR] Couldn't remove desktop.ini: {e}")

        check_pause()

        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)

            if jpg_delete and file.lower().endswith(('.jpg', '.jpeg')):
                check_pause()
                try:
                    os.chmod(full_path, 0o666)
                    os.remove(full_path)
                    add_log(f"Deleting JPG file")
                except Exception as e:
                    add_log(f"[ERROR] Couldn't delete JPG: {e}")
                check_pause()

            elif ico_delete and file.lower().endswith('.ico'):
                check_pause()
                try:
                    os.chmod(full_path, 0o666)
                    os.remove(full_path)
                    add_log(f"Deleteing ICO file")
                except Exception as e:
                    add_log(f"[ERROR] Couldn't delete ICO: {e}")
                check_pause()

            elif not jpg_delete and file.lower().endswith(('.jpg', '.jpeg')) and visibility != "skip":
                check_pause()
                if visibility == "visible":
                    subprocess.run(f'attrib -h "{full_path}"', shell=True, creationflags=CREATE_NO_WINDOW)
                    add_log(f"Made visible: {file}")
                elif visibility == "hidden":
                    subprocess.run(f'attrib +h "{full_path}"', shell=True, creationflags=CREATE_NO_WINDOW)
                    add_log(f"Made Hidden: {file}")
                check_pause()

        update_progress(i + 1, len(folders))

    clear_icon_cache()
    add_log("Done deiconifying all folders.")
    check_pause()
