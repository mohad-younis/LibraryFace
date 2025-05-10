from core.config import( 
    time, os, subprocess, Image, 
    CREATE_NO_WINDOW
)

from ui.helpers.logs import add_log

def set_folder_icon(folder, jpg, ico):
    if not os.path.exists(ico):
        return False

    try:
        Image.open(ico).verify()
    except:
        add_log(f"Removing broken ICO: {ico}")
        try:
            os.remove(ico)
        except:
            pass
        return False

    ini_path = os.path.join(folder, "desktop.ini")
    icon_filename = os.path.basename(ico)
    thumbs = os.path.join(folder, "Thumbs.db")

    try:
        try_apply(folder, ini_path, icon_filename, thumbs)
    except PermissionError:
        add_log(f"Permission denied: trying to take ownership of '{folder}'...")
        override_permission(folder)
        time.sleep(1)
        try_apply(folder, ini_path, icon_filename, thumbs)
    except:
        add_log(f"Couldn't apply icon")
        return False

    for file in [jpg, ico]:
        hide_file(file)
            
    return True

def override_permission(folder):
    try:
        subprocess.run(f'takeown /f "{folder}" /r /d y', shell=True, creationflags=CREATE_NO_WINDOW)
        subprocess.run(f'icacls "{folder}" /grant "%username%:F" /t', shell=True, creationflags=CREATE_NO_WINDOW)
        return
    except Exception as final_e:
        return

def try_apply(folder, ini_path, icon_filename, thumbs):
    if os.path.exists(ini_path):
        os.chmod(ini_path, 0o666)
        os.remove(ini_path)

    with open(ini_path, "w", encoding="utf-8") as f:
        f.write(f"[.ShellClassInfo]\nIconResource={icon_filename},0\n")

    subprocess.run(f'attrib +h +s "{ini_path}"', shell=True, creationflags=CREATE_NO_WINDOW)
    subprocess.run(f'attrib -r -s -h "{folder}"', shell=True, creationflags=CREATE_NO_WINDOW)
    time.sleep(0.1)
    subprocess.run(f'attrib +r "{folder}"', shell=True, creationflags=CREATE_NO_WINDOW)

    if os.path.exists(thumbs):
        os.remove(thumbs)

    add_log("📁 Applied folder icon")

def hide_file(path):
    if os.path.exists(path):
        subprocess.run(f'attrib +h "{path}"', shell=True, creationflags=CREATE_NO_WINDOW)

    