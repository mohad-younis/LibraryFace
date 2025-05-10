from core.config import( 
    requests, 
    TMDB_API_KEY, TMDB_IMAGE_BASE, TMDB_MOVIES_URL, TMDB_TV_SHOW_URL
)
import core.config as config

from . omdb import search_omdb

from ui.helpers.logs import add_log

debug = False

def search_tmdb(folder_name, content_type):
    try:
        endpoint = TMDB_TV_SHOW_URL if content_type.lower() == "tv show" else TMDB_MOVIES_URL
        if debug:
            add_log(f"🔎 Searching ({content_type}): {folder_name}")

        params = {
            "api_key": TMDB_API_KEY,
            "query": folder_name
        }

        res = requests.get(endpoint, params=params, timeout=20)
        res.raise_for_status()
        data = res.json()

        if data.get("results"):
            poster = data["results"][0].get("poster_path")
            if poster:
                config.tmdb_fail_count = 0
                return TMDB_IMAGE_BASE + poster

        if not data.get("data"):
            if debug:
                add_log("❌ No results found")
            return None
        
    except Exception as e:
        config.tmdb_fail_count += 1
        if config.tmdb_fail_count >= 2:
            config.tmdb_unreachable = True
    return None