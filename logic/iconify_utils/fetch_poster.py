from core.config import os, requests, Image, time

from logic.general_utils.connection import wait_for_internet
from logic.search_utils.search import search_poster

from ui.helpers.logs import add_log
from ui.helpers.process import check_pause
from ui.handlers.preview import preview_poster

def fetch_and_download_poster(selected, query, jpg, poster_url, preview_name,name, matched_title):
    wait_for_internet()
    check_pause()
    url = search_poster(selected, query, poster_url)
    if url:
        wait_for_internet()
        check_pause()
        if download_image(url, jpg, matched_title) and os.path.exists(jpg):
            wait_for_internet()
            check_pause()
            if  is_valid_poster(jpg):
                wait_for_internet()
                check_pause()
                preview_poster(jpg, preview_name, name, selected)   
                return True
            else:
                try:
                    os.remove(jpg)
                except Exception as e:
                    print(f"Error removing invalid poster: {e}")
                return False
        else:
            return False
    else:
        return False

def download_image(url, save_path, matched_title, retries=2):
    for attempt in range(retries + 1):
        try:
            wait_for_internet()
            check_pause()
            res = requests.get(url, stream=True, timeout=20)

            if res.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(res.content)
                wait_for_internet()
                check_pause()
                if matched_title:
                    add_log(f"Downloading Poster: {matched_title}")
                else:
                    add_log("Downloading Poster")
                return True
            else:
                add_log(f"⚠️ Failed to download poster")
        except requests.exceptions.RequestException as e:
            add_log(f"⚠️ Attempt {attempt + 1} failed")
            time.sleep(2)

    add_log(f"❌ Could not download poster after {retries + 1} attempts")
    return False

def is_valid_poster(jpg_path):
    try:
        with Image.open(jpg_path) as img:
            width, height = img.size
            if width < height:
                return True

    except Exception:
        return False
