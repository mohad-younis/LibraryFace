from core.config import time, requests, messagebox
import core.config as config

from ui.helpers.logs import add_log

def wait_for_internet():
    first_time = True
    while not check_internet_conection():
        if first_time:
            add_log("⏸ Internet connection lost. Waiting to reconnect...")
            messagebox.showerror("Connection Error", "Internet connection lost. Process will resume when connection is restored.")
            first_time = False

        time.sleep(3)

    config.paused = False
    config.paused_event.set()

def check_internet_conection():
    try:
        requests.get("https://www.google.com", timeout=30)
        return True
    except:
        return False