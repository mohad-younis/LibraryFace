from core.config import( 
    requests, 
    OMDB_API_KEY, OMDB_URL
)

def search_omdb(folder_name: str) -> str:
    try:
        params = {
            "apikey": OMDB_API_KEY,
            "t": folder_name
        }
        res = requests.get(OMDB_URL, params=params, timeout=20)
        res.raise_for_status()
        data = res.json()
        if data.get("Response") == "True" and data.get("Poster") and data.get("Poster") != "N/A":
            print(f"🛟 Fallback OMDb Poster: {data['Poster']}")
            return data["Poster"]
    except Exception as e:
        print(f"[OMDb Fallback Error] ")
    return ""