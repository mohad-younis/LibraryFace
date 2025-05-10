import pandas as pd
import re
import os
# =========== File setup ============
imported_csv = "anime_dataset+.csv"
saved_csv = "anime_dataset.csv"
content_type = "Anime"
# ============ Utilities ============
ROMAN_NUMERALS = {
    "ii": "2", "iii": "3", "iv": "4", "v": "5", "vi": "6", "vii": "7",
    "viii": "8", "ix": "9", "x": "10"
}

NUMBER_WORDS = {
    "first": "1", "second": "2", "third": "3", "fourth": "4", "fifth": "5",
    "sixth": "6", "seventh": "7", "eighth": "8", "ninth": "9", "tenth": "10"
}

def normalize_title_season_format(title):
    original_title = title
    title = title.lower()

    # Step 1: Replace roman numerals
    for roman, num in ROMAN_NUMERALS.items():
        title = re.sub(rf'\bseason {roman}\b', f'season {num}', title)
        title = re.sub(rf'\bpart {roman}\b', f'part {num}', title)

    for word, number in NUMBER_WORDS.items():
        title = re.sub(rf'\b{word} season\b', f'season {number}', title)

    # Step 2: Replace '2nd season', '3rd season', etc
    title = re.sub(r'\b(\d{1,2})(st|nd|rd|th)[\s._-]*season\b', r'season \1', title)

    # Step 3: Handle 'number part number' into 'season N part M' first
    title = re.sub(r'\b(\d{1,2})[\s._-]*part[\s._-]*(\d{1,2})\b', r'season \1 part \2', title, flags=re.IGNORECASE)

    # Step 4: One-digit number at end becomes 'season N'
    title = re.sub(r'(?<!season\s)(?<!part\s)(\d)\s*(?=part\b|$)', r' season \1', title, flags=re.IGNORECASE)

    # Step 5: Normalize 'part' cases
    title = re.sub(r'\bseason (\d{1,2}) part (\d{1,2})\b', r'season \1 part \2', title)
    title = re.sub(r'\bpart (\d{1,2})\b', r'part \1', title)

    # Step 6: Handle 'final season'
    final_season = bool(re.search(r"\bfinal[\s._-]+season\b", title, re.IGNORECASE))

    # 🟰 NEW: Copy the "title" edits into a new working version of original_title
    working_title = original_title.lower()

    for word, number in NUMBER_WORDS.items():
        working_title = re.sub(rf'\b{word} season\b', f'season {number}', working_title, flags=re.IGNORECASE)

    for roman, num in ROMAN_NUMERALS.items():
        working_title = re.sub(rf'\bseason {roman}\b', f'season {num}', working_title, flags=re.IGNORECASE)
        working_title = re.sub(rf'\bpart {roman}\b', f'part {num}', working_title, flags=re.IGNORECASE)

    # Now reconstruct clean title
    clean_title = working_title

    season_match = re.search(r'season (\d{1,2})(?: part (\d{1,2}))?', title)
    if season_match:
        season_num = season_match.group(1)
        part_num = season_match.group(2)

        if final_season:
            clean_season = f"Final Season"
        else:
            clean_season = f"Season {season_num}"

        if part_num:
            clean_season += f" Part {part_num}"

        # Replace messy season references inside original title
        clean_title = re.sub(
            r'(\d{1,2}[\s._-]*part[\s._-]*\d{1,2}|'
            r'season[\s._-]*\d{1,2}(?:[\s._-]*part[\s._-]*\d{1,2})?|'
            r'\d{1,2}(st|nd|rd|th)[\s._-]*season|'
            r's\d{1,2}e\d{1,3}|'
            r'\d{1,2}$|'
            r'the[\s._-]*final[\s._-]*season|'
            r'final[\s._-]*season)', 
            clean_season,
            clean_title,
            count=1,
            flags=re.IGNORECASE
        )
    elif final_season:
        clean_title = re.sub(r'(?i)final[\s._-]*season', "Final Season", clean_title, count=1)

    # Final clean: remove double spaces
    clean_title = re.sub(r'\s+', ' ', clean_title).strip()

    return clean_title

# === Step 6: Extract season and part info ===
def extract_season_part(row):
    title = row["title"]
    season = row["season"]
    part = row["part"]

    if pd.isna(title):
        return pd.Series([season, part, title])

    final_season_pattern = re.compile(r'\bthe[\s._-]+final[\s._-]+season\b', flags=re.IGNORECASE)
    if final_season_pattern.search(title) and not season:
        season = "Final Season"
        title = final_season_pattern.sub('', title)

    final_season_pattern_ = re.compile(r'\bfinal[\s._-]+season\b', flags=re.IGNORECASE)
    if final_season_pattern_.search(title) and not season:
        season = "Final Season"
        title = final_season_pattern_.sub('', title)

    # Extract "Season X" (only if season is still empty)
    season_pattern = re.compile(r'\bseason[\s._-]*(\d{1,2})\b', flags=re.IGNORECASE)
    season_match = season_pattern.search(title)
    if season_match and not season:
        season = f"Season {season_match.group(1)}"
        title = season_pattern.sub('', title)

    # Extract "Part X" (only if part is still empty)
    part_pattern = re.compile(r'\bpart[\s._-]*(\d{1,2})\b', flags=re.IGNORECASE)
    part_match = part_pattern.search(title)
    if part_match and not part:
        part = f"Part {part_match.group(1)}"
        title = part_pattern.sub('', title)

    # Clean extra spaces
    title_cleaned = re.sub(r'\s+', ' ', title).strip()

    return pd.Series([season, part, title_cleaned])

def extract_year_from_title(row):
    title = row['title']
    year = row.get('year', '')  # Keep existing year if already there

    if pd.isna(title):
        return pd.Series([year, title])

    # Search for a 4-digit year starting with 19 or 20
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', title)
    if year_match:
        found_year = year_match.group(1)
        # Only overwrite year if it was empty before
        if not year:
            year = found_year
        # Remove year from title
        title = re.sub(r'\b(19\d{2}|20\d{2})\b', '', title)

    # Final clean: remove double spaces
    title = re.sub(r'\s+', ' ', title).strip()

    return pd.Series([year, title])

def is_bad_title(title):
    if pd.isna(title):
        return True

    title = str(title).strip()

    # Too short
    if len(title) < 3:
        return True

    # No alphabet letters
    if not re.search(r'[a-zA-Z]', title):
        return True

    # Too many symbols compared to letters
    letters = re.findall(r'[a-zA-Z]', title)
    symbols = re.findall(r'[^a-zA-Z0-9 ]', title)
    if len(symbols) > len(letters):
        return True

    return False
    
def clean_title(title):
    if pd.isna(title):
        return ""
    title = str(title).lower()
    cleaned = re.sub(r"[._\-]", " ", title)
    cleaned = re.sub(r"""[?!$#@%^*\-_=+|/;()\[\]{}.,'"\\]""", " ", title)
    cleaned = re.sub(r"\s*&\s*", " and ", cleaned)
    cleaned = re.sub(r"\s*:\s*", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def filter_and_prepare_columns(data_df, content_type):
    # === Step 1: Detect important columns ===
    possible_poster_columns = [
        "poster", "poster_path", "coverImage_extraLarge"
    ]
    found_poster_col = None
    for col in data_df.columns:
        if col in possible_poster_columns:
            found_poster_col = col
            break

    possible_title_columns = ["title", "name"]
    found_title_col = None
    for col in data_df.columns:
        if col in possible_title_columns:
            found_title_col = col
            break 

    possible_year_columns = ["year", "release_date"]
    found_year_col = None
    for col in data_df.columns:
        if col in possible_year_columns:
            found_year_col = col
            break

    possible_english_columns = ["title_english"]
    found_english_col = None
    for col in data_df.columns:
        if col in possible_english_columns:
            found_english_col = col
            break

    possible_romaji_columns = ["title_romaji"]
    found_romaji_col = None
    for col in data_df.columns:
        if col in possible_romaji_columns:
            found_romaji_col = col
            break

    possible_season = ["season"]
    found_season = None
    for col in data_df.columns:
        if col in possible_season:
            found_season = col
            break

    possible_part = ["part"]
    found_part = None
    for col in data_df.columns:
        if col in possible_part:
            found_part = col
            break

    # === Step 2: Rename columns to a standard ===
    if found_poster_col:
        data_df.rename(columns={found_poster_col: "poster"}, inplace=True)
    if found_title_col:
        data_df.rename(columns={found_title_col: "title"}, inplace=True)
    if found_year_col:
        data_df.rename(columns={found_year_col: "year"}, inplace=True)
    if found_english_col:
        data_df.rename(columns={found_english_col: "title_english"}, inplace=True)
    if found_romaji_col:
        data_df.rename(columns={found_romaji_col: "title_romaji"}, inplace=True)

    # === Step 3: Keep only needed columns ===
    columns_to_keep = ["title", "title_romaji", "title_english", "year", "poster"]
    columns_to_keep = [col for col in columns_to_keep if col in data_df.columns]
    data_df = data_df[columns_to_keep]

    # === Step 4: Clean year column ===
    if "season" not in data_df.columns:
        data_df["season"] = ""
    
    if "part" not in data_df.columns:
        data_df["part"] = ""

    if "year" not in data_df.columns:
        data_df["year"] = ""
    else:
        data_df["year"] = data_df["year"].astype(str).str.extract(r"(\d{4})")
        data_df["year"] = data_df["year"].fillna('')

    # === Step 5: Fix poster URLs ===


    # === Step 7: Add content type ===
    data_df["type"] = content_type

    return data_df
# ======== Ask for main process ========
print("Which process would you like to run?")
print("1. Start full cleaning pipeline")
print("2. Arrange anime titles")

main_choice = input("Enter 1 or 2: ").strip()

# ========= Step 1: Load file ==========
if not os.path.exists(imported_csv):
    print(f"- File not found: {imported_csv}")
    exit()

data_df = pd.read_csv(imported_csv)
print(f"- Loaded dataset: {imported_csv}")

# =========== Main process ==========
if main_choice == "1":
    print("- Starting full cleaning pipeline...")

    print("- Filtering the dataset from unwanted columns...")
    data_df = filter_and_prepare_columns(data_df, content_type)
    print("- unwanted columns removed.")

    print("- Removing bad titles...")
    initial_count = len(data_df)
    data_df = data_df[~data_df["title"].apply(is_bad_title)]
    print("- Bad titles removeded.")

    print("- Cleaning special characters...")
    data_df["title"] = data_df["title"].astype(str).apply(clean_title)
    print("- Special characters cleaned.")

    clean_season = input("Do you want to extract year from titles? (y/n)").strip()
    if clean_season.lower() == "y":
        print("- Extracting year from titles...")
        data_df[['year', 'title']] = data_df.apply(extract_year_from_title, axis=1)
        print("- Year extracted.")

    clean_season = input("Do you want to extract clean season & part formate? (y/n)").strip()
    if clean_season.lower() == "y":
        print("- Extracting season & part info...")
        
        data_df['title'] = data_df['title'].apply(normalize_title_season_format)
        # Apply to rows
        data_df[["season", "part", "title"]] = data_df.apply(extract_season_part, axis=1)

    print("- Season & part extracted.")

    data_df.to_csv(saved_csv, index=False)
    print(f"- Saved cleaned file as {saved_csv}")
    
elif main_choice == "2":
    print("- Filtering the dataset from unwanted columns...")
    data_df = filter_and_prepare_columns(data_df, content_type)
    print("- unwanted columns removed.")

    print("- Arranging anime titles")
    data_df["title_romaji"] = data_df["title_romaji"].fillna("").str.strip()
    data_df["title_english"] = data_df["title_english"].fillna("").str.strip()

    romaji_df = data_df.copy()
    romaji_df["title"] = romaji_df["title_romaji"]

    english_df = data_df.copy()
    english_df["title"] = english_df["title_english"]

    final_df = pd.concat([romaji_df, english_df], ignore_index=True)
    final_df.drop(columns=["title_romaji", "title_english"], inplace=True)
    final_df = final_df[final_df["title"] != ""]

    print("- All titles moved to one column")
    final_df.to_csv(saved_csv, index=False)
    print(f"- Saved cleaned file as {saved_csv}")
