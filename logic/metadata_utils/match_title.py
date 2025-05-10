import difflib
from core.config import( 
    pd, 
    ANIME_DATASET, TV_DATASET, MOVIE_DATASET
)

from ui import layout
from ui import state
from ui.helpers.logs import add_log
from ui.helpers.popup import show_choice_popup

debug = False

anime_df = pd.read_csv(ANIME_DATASET)
tv_df = pd.read_csv(TV_DATASET)
movie_df = pd.read_csv(MOVIE_DATASET)

datasets = [("Anime", anime_df), ("TV Show", tv_df), ("Movies", movie_df)]

def find_match(base_title, year="", season="", part="", manual=False):
    best_match = None
    best_title = None
    best_match_anime = None
    best_match_tv = None
    best_match_movies = None
    partial_candidates = []

    if debug:
        add_log(f"Base title: {base_title}")

    if manual:
        selected = show_choice_popup(base_title)
        return "", selected, "", "", "", ""
    else:
        for content_type, df in datasets:
            check_parts = base_title.lower().split()
            if debug:
                add_log(f"Dataset: {content_type}")

            while check_parts:
                current_title = " ".join(check_parts)
                if debug:
                    add_log(f"Checking title: {current_title}")
                matches = df[df["title"].str.lower() == current_title]
                
                for _, row in matches.iterrows():
                    season_matched, part_matched, year_matched, poster_matched = get_best_match(row, year, season, part)

                    score = matching_score(year_matched, season_matched, part_matched, current_title)

                    if content_type == "Anime" and (best_match_anime is None or score > best_match_anime["score"]):
                        best_match_anime = {
                            "type": content_type,
                            "poster": poster_matched,
                            "score": score,
                            "title": base_title,
                            "matched_title": row["title"]
                        }

                    elif content_type == "TV Show" and (best_match_tv is None or score > best_match_tv["score"]):
                        best_match_tv = {
                            "type": content_type,
                            "poster": poster_matched,
                            "score": score,
                            "title": base_title,
                            "matched_title": row["title"]
                        }

                    elif content_type == "Movies" and (best_match_movies is None or score > best_match_movies["score"]):
                        best_match_movies = {
                            "type": content_type,
                            "poster": poster_matched,
                            "score": score,
                            "title": base_title,
                            "matched_title": row["title"]
                        }

                if state.set_content_type == "Auto":
                    candidates = [
                        bm for bm in [best_match_anime, best_match_tv, best_match_movies]
                        if bm is not None and len(bm["matched_title"].split()) == len(bm["title"].split())
                    ]
                    priority = {"Anime": 3, "TV Show": 2, "Movies": 1}
                    best_match = max(candidates, key=lambda x: (x["score"], priority.get(x["type"], 0)), default=None)
                elif state.set_content_type == "Anime":
                    candidates = [
                        bm for bm in [best_match_anime]
                        if bm is not None and len(bm["matched_title"].split()) == len(bm["title"].split())
                    ]
                    best_match = best_match_anime
                elif state.set_content_type == "TV Show":
                    candidates = [
                        bm for bm in [best_match_tv]
                        if bm is not None and len(bm["matched_title"].split()) == len(bm["title"].split())
                    ]
                    best_match = best_match_tv
                elif state.set_content_type == "Movies":
                    candidates = [
                        bm for bm in [best_match_movies]
                        if bm is not None and len(bm["matched_title"].split()) == len(bm["title"].split())
                    ]
                    best_match = best_match_movies

                if not matches.empty:
                    break

                if not best_match:
                    partial_candidates += get_partial_match(current_title, df, content_type)
                    best_title = fuzzy_match(partial_candidates, base_title)

                check_parts.pop()

        if best_match:
            similrity_ratio_m = compare_titles(base_title, best_match["matched_title"])
            if similrity_ratio_m > 85:
                
                if season and best_match["score"][1] != 1 and best_match["type"] == "Anime":
                    return "", best_match["type"], "", "", "", ""
                if part and not best_match["score"][2] != 1 and best_match["type"] == "Anime":
                    return "", best_match["type"], "", "", "", ""
                
                # Get the top score
                if candidates:
                    top_score = max(candidates, key=lambda x: x["score"])["score"]
                else:
                    top_score = 0  # or handle this case another way

                # Build posters only for those with the same top score
                anime_poster = best_match_anime["poster"] if best_match_anime and best_match_anime["score"] == top_score else ""
                tv_poster = best_match_tv["poster"] if best_match_tv and best_match_tv["score"] == top_score else ""
                movie_poster = best_match_movies["poster"] if best_match_movies and best_match_movies["score"] == top_score else ""
                return best_match["matched_title"], best_match["type"], best_match["poster"], anime_poster, tv_poster, movie_poster
            else:
                return "", best_match["type"], "", "", "", ""

        elif best_title:
            similrity_ratio = compare_titles(base_title, best_title)
            if similrity_ratio > 85:
                new_base_title = best_title
                if debug:
                    add_log(f"✨ Fuzzy match found: '{new_base_title}' — restarting search")
                return find_match(new_base_title, year=year, season=season, part=part, manual=manual)
            else:
                if state.set_content_type != "Auto":
                    fallback_type = state.set_content_type
                    return "", fallback_type, "", "", "", ""
                else:
                    return "", "Unknown", "", "", "", ""
        elif not best_match and not best_title:
            if state.set_content_type != "Auto":
                fallback_type = state.set_content_type
                return "", fallback_type, "", "", "", ""
            else:
                if debug:
                    add_log("❌ No match found.")
                return "", "Unknown", "", "", "", ""
        else:
            return "", "Unknown", "", "", "", ""

def get_best_match(row, year, season, part):
    raw_year = row.get("year", "")
    row_year = str(raw_year).strip().split(".")[0] if pd.notna(raw_year) else ""
    normalized_year_str = str(year).strip().split(".")[0]

    raw_season = row.get("season", "")
    row_season = str(raw_season).strip().split(".")[0] if pd.notna(raw_season) else ""
    normalized_season = str(season.title()).strip().split(".")[0]

    raw_part = row.get("part", "")
    row_part = str(raw_part).strip().split(".")[0] if pd.notna(raw_part) else ""
    normalized_part = str(part.title()).strip().split(".")[0]

    season_matched = (normalized_season and row_season == normalized_season)
    part_matched = (normalized_part and row_part == normalized_part)
    year_matched = (normalized_year_str and row_year == normalized_year_str)
    
    if debug:
        add_log(f"Matched: {row['title']} | Year: {row_year} | Season: {row_season}")

    poster_matched = row.get("poster", "")
    if pd.isna(poster_matched):
        poster_matched = ""
    
    return season_matched, part_matched, year_matched, poster_matched

def matching_score(year_matched, season_matched, part_matched, current_title):
    score = (
        1 if year_matched else 0,
        1 if season_matched else 0,
        1 if part_matched else 0,
        len(current_title.split()),
    )
    if debug:
        add_log(f"Score: Year={score[0]}, season={score[1]}, part={score[2]}, Words={score[3]}")

    return score

def get_partial_match(current_title, df, content_type):
    partial_match = df[df["title"].str.lower().str.contains(current_title, na=False)].head(100)
    partial_candidates = []
    if not partial_match.empty:
        if debug:
            add_log(f"🟡 Partial matches found for: '{current_title}' (showing up to 100)")
        partial_candidates += [
            (row["title"], row.get("poster", "") or "", content_type)
            for _, row in partial_match.iterrows()
        ]
        return partial_candidates
    else:
        return partial_candidates

def fuzzy_match(partial_candidates, base_title):
    if partial_candidates:
        if debug:
            add_log(f"📂 Partial match count: {len(partial_candidates)}")
        titles_only = [t[0] for t in partial_candidates]
        best_title = difflib.get_close_matches(base_title, titles_only, n=1, cutoff=0.90)
        if best_title:
            return best_title[0]
        else:
            return ""
    else:
        return ""

def compare_titles(title1, title2) -> int:
    """
    Compare two titles and return a similarity percentage (0–100).
    """
    clean1 = str(title1).strip().lower()
    clean2 = str(title2).strip().lower()
    ratio = difflib.SequenceMatcher(None, clean1, clean2).ratio()
    if debug:
        add_log(f"Comparing '{clean1}' with '{clean2}' | Similarity: {ratio:.2f}")
    return int(ratio * 100)
