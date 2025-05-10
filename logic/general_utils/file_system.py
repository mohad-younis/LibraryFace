from core.config import( 
    time, os, ctypes, subprocess, Path, 
    CREATE_NO_WINDOW
)

from ui import state
from ui.helpers.logs import add_log

def clear_icon_cache():
    try:
        # Step 1: refresh each folder manually (if it has icon + ini)
        folders = [state.path_var.get()] if not state.apply_to_subfolders.get() else get_all_subfolders(state.path_var.get())
        updated = 0

        for folder in folders:
            folder_refresh(folder)
            updated += 1
        add_log(f"Refreshing {updated} folder(s)")

        # Step 2: system-wide cache clear (fallback)
        ie4uinit_path = os.path.join(os.environ.get("WINDIR", ""), "System32", "ie4uinit.exe")
        if os.path.exists(ie4uinit_path):
            subprocess.run([ie4uinit_path, "-ClearIconCache"], check=True, creationflags=CREATE_NO_WINDOW)
            add_log("icon cache cleared")
        else:
            print("[!] ie4uinit.exe not found. Skipping global cache clear.")

    except Exception as e:
        print(f"[!] Failed to clear icon cache")

def folder_refresh(folder):
    path = Path(folder)
    files = [f.name.lower() for f in path.iterdir() if f.is_file()]
    if any(f.endswith(".ico") for f in files) and "desktop.ini" in files:
        try:
            ctypes.windll.kernel32.SetFileAttributesW(str(path), 0x04 | 0x01)
            path.touch()
        except Exception as e:
            add_log(f"[!] Failed to refresh: {path.name}")

def get_all_subfolders(parent):
    folders = []
    for root, dirs, files in os.walk(parent):
        for dir in dirs:
            folders.append(os.path.join(root, dir))
    return folders

