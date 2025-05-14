import re

ROMAN_NUMERALS = {
    "ii": "2", "iii": "3", "iv": "4", "v": "5", "vi": "6", "vii": "7",
    "viii": "8", "ix": "9", "x": "10"
}

NUMBER_WORDS = {
    "first": "1", "second": "2", "third": "3", "fourth": "4", "fifth": "5",
    "sixth": "6", "seventh": "7", "eighth": "8", "ninth": "9", "tenth": "10"
}

def extract_season(raw_title: str):
    season_str = ""
    raw_title = raw_title.lower()

    for word, number in NUMBER_WORDS.items():
        raw_title = re.sub(rf'\b{word} season\b', f'season {number}', raw_title, flags=re.IGNORECASE)
    raw_title = re.sub(r'\b(\d{1,2})(st|nd|rd|th)[\s._-]*season\b', r'season \1', raw_title)

    final_season = bool(re.search(r"\b(?:the[\s._-]+)?final[\s._-]+season\b", raw_title, flags=re.IGNORECASE))
    season_match = re.search(r'\b(s(?:eason)?[\s._-]?)(\d{1,2})\b', raw_title, flags=re.IGNORECASE)
    if not season_match:
        season_match = re.search(r'[Ss](\d{1,2})[Ee](\d{1,3})', raw_title)  # S02E24
    if season_match:
        season_num_raw = season_match.group(2) if season_match.lastindex >= 2 else season_match.group(1)
        season_num = int(season_num_raw)
        if season_num != 1 and not final_season:
            season_str = f"Season {season_num}"
    elif final_season:
        season_str = "Final Season"
    else:
        season_str = ""
    return season_str

def extract_part(raw_title: str):
    part_str = ""
    raw_title = raw_title.lower()

    for roman, num in ROMAN_NUMERALS.items():
        raw_title = re.sub(rf'\b{roman}\b', num, raw_title)

    part_match = re.search(r'(?<!\w)(part|p)[\s._-]?(\d{1,2})(?!\w)', raw_title, flags=re.IGNORECASE)
    if not part_match:
        is_final_part = bool(re.search(r"\bfinal(?:[\s._-]+)?part\b", raw_title, flags=re.IGNORECASE))
        if is_final_part:
            part_str = "Final Part"
        else:
            part_str = ""
    else:
        part_num = int(part_match.group(2))
        if part_num:
            part_str = f"Part {part_num}".strip()
        else:
            part_str = ""
    return part_str

def extract_year(raw_title: str):
    year_str = ""
    raw_title = raw_title.lower()
    
    year_match = re.search(r'(?<!\d)(?:[\(\[\{_\-\.\s]*)?(19|20)\d{2}(?:[\)\]\}_\-\.\s]*)?(?!\d)', raw_title)
    if year_match:
        inner_match = re.search(r'(19|20)\d{2}', year_match.group(0))
        if inner_match:
            raw = inner_match.group(0)
            year_str = f"{raw}"
        else:
            year_str = ""
    else:
        year_str = ""
    
    return year_str

def extract_base(raw_title: str):
    raw_title = raw_title.lower()

    # Remove Year ------------------------------------------------------------------------------------------

    # 1. Remove year like 2012, 1999, etc.
    raw_title = re.sub(r"[\[\(\{<\. _-]?(19|20)\d{2}[\]\)\}>\. _-]?", " ", raw_title)

    # ------------------------------------------------------------------------------------------

    # 2. Remove Roman numeral math like "IV + V"
    raw_title = re.sub(r'(?:\s|^)([IVXLCM]+(?:\s*\+\s*[IVXLCM]+)+)(?=\s|$)', '', raw_title, flags=re.IGNORECASE)
    # 3. Remove Arabic numeral math like "1 + 2"
    raw_title = re.sub(r'(?:\s|^)(\d+(?:\s*\+\s*\d+)+)(?=\s|$)', '', raw_title)

    # Remove Season & Episode ------------------------------------------------------------------------------------------

    # 4. Remove "S01E12"
    raw_title = re.sub(r'[Ss]\d{1,2}[Ee]\d{1,3}', '', raw_title, flags=re.IGNORECASE)
    # 5. Remove episode patterns like "S01E01", "Season 1 Ep12", etc.
    raw_title = re.sub(
        r'(?i)(s(eason)?[\s._-]?\d{1,2}[\s._-]*)?e(p(isode)?)?[\s._-]?\d{1,3}.*',
        lambda m: m.group(0) if m.group(1) is None else m.group(1), raw_title
    )

    # Remove Season ------------------------------------------------------------------------------------------
    
    # 6. If format is "Season 2E10" → keep "Season 2"
    raw_title = re.sub(r"(Season \d{1,2})[Ee](\d{1,3})", r"\1", raw_title, flags=re.IGNORECASE)
    raw_title = re.sub(r"\bthe[\s._-]+final[\s._-]+season\b", "", raw_title, flags=re.IGNORECASE)
    raw_title = re.sub(r"\bfinal[\s._-]+season\b", "", raw_title, flags=re.IGNORECASE)   
    for word, number in NUMBER_WORDS.items():
        raw_title = re.sub(rf'\b{word} season\b', '', raw_title)
    # 7. Replace '2nd season', '3rd season', etc
    raw_title = re.sub(r'\b(\d{1,2})(st|nd|rd|th)[\s._-]*season\b', '', raw_title)
    # 8. Remove patterns like "Season 1" or "s1"
    raw_title = re.sub(r'\b(?:s(?:eason)?[\s._-]?\d{1,2})\b', '', raw_title, flags=re.IGNORECASE)

    # Remove Episode ------------------------------------------------------------------------------------------
    
    # 9. Remove single episode indicators like "E12", "e-05", "e_7"
    raw_title = re.sub(r"\b[Ee][\s._-]?\d{1,3}\b", "", raw_title, flags=re.IGNORECASE)
    # 10. Remove verbose episode indicators like "Ep10", "Episode-10", "Ep_10"
    raw_title = re.sub(r"\b(?:Ep(?:isode)?)[\s._-]*\d{1,3}\b", "", raw_title, flags=re.IGNORECASE)
    # 11. Remove stand-alone "Ep"
    raw_title = re.sub(r"\b[Ee][p]?\b", "", raw_title)
    # 12. Remove episode ranges like "Ep 01-03" or "02~05"
    raw_title = re.sub(r"\b(Ep?\.?|)[\d]{1,3}[\-~to]{1,3}[\d]{1,3}\b", "", raw_title, flags=re.IGNORECASE)
    # 13. Remove episode ranges like "01–03"
    raw_title = re.sub(r"\b\d{1,3}[\-~to]{1,3}\d{1,3}\b", "", raw_title, flags=re.IGNORECASE)

    # Remove Part ------------------------------------------------------------------------------------------

    # 14. Remove "Part 1", "p-2", etc.
    for roman, num in ROMAN_NUMERALS.items():
        raw_title = re.sub(rf'\b{roman}\b', num, raw_title)
    raw_title = re.sub(r"\b(part|p)[\s._-]?\d{1,2}\b", "", raw_title, flags=re.IGNORECASE)
    raw_title = re.sub(r"\bfinal[\s._-]+part\b", "", raw_title, flags=re.IGNORECASE)
    raw_title = re.sub(r"\bthe[\s._-]+final[\s._-]+part\b", "", raw_title, flags=re.IGNORECASE)

    # Remove junk ------------------------------------------------------------------------------------------

    # 15. Replace " & " with " and "
    raw_title = re.sub(r"\s*&\s*", " and ", raw_title)
    # 16. Replace ":" with space
    raw_title = re.sub(r"\s*:\s*", " ", raw_title)
    # 17. Remove brackets and their content
    raw_title = re.sub(r"\[.*?\]|\(.*?\)", "", raw_title)
    # 18. Replace ".", "-", "_" with space
    raw_title = re.sub(r"[._\-]", " ", raw_title)
   
    # Remove Unwanted Words ------------------------------------------------------------------------------------------

    unwanted = [
        "1080p", "720p", "480p", "2160p", "1080", "720", "480", "2160", "4K", "8K", "8bit", "10bit", "BD", "EngDub", "EnglishDub", "EnglishSub", 
        "Erai raws", "Erai", "raw", "HDR", "BDR", "BRR", "HDRip", "BluRay", "BDRip", "BRRip", "WEBRip", "WEB", 
        "WEB-DL", "HDTV", "DVDRip", "DVDScr", "DVD", "TV", "TVRip", "REMASTERED", "DL", "WEB-DL", 
        "CAM", "TS", "R5", "HDCAM", "x264", "x265", "H264", "H265", "AVC", "HEVC", "XviD", "DivX", "Sup", 
        "AAC", "AC3", "DTS", "MP3", "FLAC", "OGG", "TrueHD", "DD5.1", "Atmos", "Dual Audio", "DualLang", 
        "MULTi", "MultiLang", "Multilingual", "English Dub", "English Sub", "EngSub", "Eng Dub", "Dubbed", 
        "Subbed", "Hardsub", "Softsub", "RAW", "Scan", "ESub", "Hindi", "Arabic", "Jap", "JPN", "VOSTFR", 
        "VO", "VF", "NF", "AMZN", "HMAX", "DSNP", "Crunchyroll", "Funimation", "Netflix", "Disney", "HBO", 
        "iTunes", "Remux", "Proper", "Repack", "Uncensored", "Censored", 
        "Sample", "Trailer", "Featurette", "Behind the Scenes", "Extras", "Bonus", "Clip", 
        "Batch", "Mini-Series", "Eng", "Sub", 
        "Ep", "SD", "HD", "FullHD", "UltraHD", "UHD",  
        "YIFY", "RARBG", "PSA", "QxR", "FGT", "Erai-raws", "HorribleSubs", "SubsPlease", "AnimeRG", 
        "Release", "Encode", "Rip", "Scene", "TYBW"
    ]
    unwanted.sort(key=len, reverse=True)
    pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, unwanted)) + r')\b', re.IGNORECASE)
    raw_title = pattern.sub("", raw_title)

    raw_title = re.sub(r"\s+", " ", raw_title).strip()
    base_title = raw_title
    
    return base_title

while True:
    raw_title = input("Enter the title: ").strip()
    if not raw_title:
        print("No title provided.")
        break

    base_title = extract_base(raw_title)
    season_str = extract_season(raw_title)
    part_str = extract_part(raw_title)
    year_str = extract_year(raw_title)
    clean_title = f"({base_title}) ({season_str}) ({part_str}) ({year_str})".strip()
    clean_title = re.sub(r"\s+", " ", clean_title).strip()
    print(clean_title)

