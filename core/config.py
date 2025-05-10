# ================
# 📦 Imports & Constants
import ctypes
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Label, Button, ttk, simpledialog, StringVar
import threading
import subprocess
from subprocess import CREATE_NO_WINDOW
import re
import time
import requests
from PIL import Image, ImageTk, UnidentifiedImageError
from customtkinter import CTkImage
from pathlib import Path
import sys
import os
import ctypes
import pandas as pd
import json
import traceback
from typing import Tuple
import io
# ==============
# 🔑 API Keys & Config
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("my.libraryface.app")

TMDB_API_KEY = "c241a0a07224595c16f6e3d07adc6cdd"
OMDB_API_KEY = "9f0e5b5e"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/original"
TMDB_MOVIES_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_TV_SHOW_URL = "https://api.themoviedb.org/3/search/tv"
OMDB_URL = "https://www.omdbapi.com/"
JIKAN_URL = "https://api.jikan.moe/v4/anime"
tmdb_unreachable = False

Main_BACKGROUND = ("#FFFFFF", "#19222D")
PANNELS = ("#EAEDF0", "#232E3C")
TEXT_PRIMARY = ("#000000", "#ffffff")
TEXT_SECONDARY = ("#64727f", "#cbcdd7")
ACCENT_COLOR = ("#3B7EDD", "#2972da")
HOVER_COLOR = ("#395f96", "#395f96")
SUCCESS_COLOR = ("#2cd370", "#2cd370")
DISABLED_COLOR = ("#B2C5E2", "#525D69")
STOP_COLOR = ("#d24252", "#d24252")
STOP_HOVER = ("#bf2d3d", "#bf2d3d")


root = tk.Tk()
tmdb_fail_count = 0 
is_processing = False
paused = False
paused_event = threading.Event()
paused_event.set()
stop_requested = False
manual_type_cache = {} 
manual_selection_queue = []
poster_states = []

root.configure(bg="#1e1e1e")
root.title("LibraryFace")
root.geometry("")

root.overrideredirect(False) 
root.attributes("-toolwindow", False)
root.attributes("-topmost", False)
root.attributes("-alpha", 1.0)

root.update_idletasks()
root.minsize(720, 300)
root.maxsize(720, 660)
root.resizable(False, False) 

def get_asset_path(filename):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, "assets", filename)

icon_path = get_asset_path("LibraryFace.ico")
root.iconbitmap(icon_path)

image_path = get_asset_path("LibraryFace.png")
image = Image.open(image_path)
image = image.resize((30, 30))
header_image = CTkImage(light_image=image, size=(30, 30))

ANIME_DATASET = get_asset_path("anime_dataset.csv")
TV_DATASET = get_asset_path("tv_show_dataset.csv")
MOVIE_DATASET = get_asset_path("movie_dataset.csv")
