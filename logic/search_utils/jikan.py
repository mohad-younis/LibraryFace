from core.config import( 
    time, requests, 
    JIKAN_URL
)
from ui.helpers.logs import add_log

debug = False

def search_jikan(folder_name):
    if debug:
        add_log(f"🔎 Searching (Anime): {folder_name}")
    try:
        if debug:
            add_log(f"🔎 Searching Jikan for: {folder_name}")
        res = requests.get(
            JIKAN_URL,
            params={"q": folder_name, "limit": 5},
            timeout=20
        )
        if debug:
            add_log(f"🔎 Jikan response: {folder_name}")
        res.raise_for_status()
        data = res.json()
        if debug:
            add_log(f"🔎 Jikan data: {folder_name}")
        if not data.get("data"):
            if debug:        
                add_log("❌ No results found")
            return None
        if debug:
            add_log(f"🔎 Jikan data2: {folder_name}")
        first_result = data["data"][0]
        poster = first_result.get("images", {}).get("jpg", {}).get("large_image_url")
        title = first_result.get("title")
        if debug:
            add_log(f"🔎 Jikan title: {title}")
        if poster:
            if debug:
                add_log(f"🔎 Jikan poster: {title}")
            return poster
        else:
            if debug:            
                add_log("❌ No results found")
            return None
    except requests.RequestException as e:
        if debug:
            add_log(f"❌ Error fetching data from Jikan: {e}")
        return None