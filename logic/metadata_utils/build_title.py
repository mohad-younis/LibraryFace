from .normalize_title import extract_base, extract_part, extract_season, extract_year
from .match_title import find_match

from ui.helpers.logs import add_log

debug = False

def build_final_name(content_type, base_title, season_str="", part_str="", year_str=""):
    if content_type == "Anime":
        return " ".join(x for x in [base_title, season_str, part_str] if x).strip()
    elif content_type == "TV Show":
        return " ".join(x for x in [base_title, season_str, part_str] if x).strip()
    elif content_type == "Movies":
        year = f"({year_str})" if year_str else ""
        return " ".join(x for x in [base_title, part_str, year] if x).strip()
    return " ".join(
    x for x in [base_title, season_str, part_str, f"({year_str})" if year_str else ""] 
    if x
    ).strip()

def build_titles(raw_title:str, manual=False):
    base_title = extract_base(raw_title)
    season_str = extract_season(raw_title)
    part_str = extract_part(raw_title)
    year_str = extract_year(raw_title)

    matched_title, content_type, poster_url, anime_poster, tv_poster, movie_poster = find_match(base_title, year_str, season_str, part_str, manual=manual)

    anime_title = ""
    tv_title = ""
    movie_title = ""
    final_folder_name = build_final_name(content_type, base_title, season_str, part_str, year_str)

    if content_type == "Anime":
        anime_title = " ".join(x for x in [base_title, season_str, part_str] if x).strip()
    elif content_type == "TV Show":
        tv_title = base_title
    elif content_type == "Movies": 
        movie_title = " ".join(x for x in [base_title, part_str] if x).strip()
    
    if debug:
        add_log(f"🧪 base_title='{base_title}' | season_str='{season_str}' | part_str='{part_str}' | year_str='{year_str}'")
        add_log(f"📦 final_name='{final_folder_name}'")
    return anime_title.strip(), tv_title.strip(), movie_title.strip(), content_type, final_folder_name.strip(), poster_url, anime_poster, tv_poster, movie_poster, matched_title
