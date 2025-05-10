import re
from turtle import pos
from core import config

from logic.general_utils.connection import wait_for_internet
from logic.search_utils.omdb import search_omdb
from ui.helpers.process import check_pause
from .jikan import search_jikan
from .tmdb import search_tmdb

from ui.helpers.logs import add_log

def search_poster(selected, query, poster_url):
    url = None
    if selected == "Anime":
        add_log(f"Getting poster for (Anime): {query}")
        if poster_url:
            url = poster_url
            return url
        else:
            wait_for_internet()
            check_pause()
            url = search_jikan(query)
            print(f"using jikan for {query}")
            if url:
                return url
            else:
                add_log("Couldn't find a poster")
                return None

    elif selected in ["Movies", "TV Show"]:
        add_log(f"Getting poster for ({selected}): {query}")
        if poster_url:
            url = poster_url
            return url
        else:
            wait_for_internet()
            check_pause()
            url = search_tmdb(query, selected)
            print(f"using TMDB for {query} {selected}")
            if url:
                return url
            else:
                url = search_omdb(query)
                print(f"using OMDB for {query} {selected}")
                if url:
                    return url
                else:
                    add_log("Couldn't find a poster")
                    return None
    else:
        add_log("Couldn't find a poster")
        return None

