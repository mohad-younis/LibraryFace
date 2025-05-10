# LibraryFace

**LibraryFace** is a smart desktop tool that transforms plain media folders into a beautifully organized library.  
It automatically sets custom folder icons and posters for anime, movies, and TV shows using real metadata from APIs like TMDb, Jikan, and OMDb.

---

## ✨ Features

- 🔍 **Metadata Recognition**: Detect titles, seasons, parts, and more from messy folder names.
- 🖼 **Poster Fetching**: Automatically grab high-quality posters from TMDb, Jikan, or OMDb.
- 🎨 **Folder Icon Generation**: Turn any folder into a visually recognizable media tile.
- 🧠 **Intelligent Title Normalization**: Clean and format folder names using advanced rules.
- 🧰 **Undo & Restore Tools**: Roll back any icon or poster change with one click.
- 🖥 **Custom UI**: Built with `customtkinter`, offering a clean and intuitive interface.

---

## 🗂 Project Structure (Simplified)

| Folder        | Purpose                                         |
|---------------|-------------------------------------------------|
| `assets/`     | Datasets and default icons/images               |
| `core/`       | Core settings and app branding                  |
| `logic/`      | All core logic: iconify, search, undo, metadata |
| `ui/`         | UI components and layouts (Tkinter-based)       |
| `hooks/`      | PyInstaller or packaging-related hooks          |
| `.gitignore`  | Keeps your repo clean from generated files      |

---

## 🚀 Getting Started

1. **Clone the repo**:
   ```bash
   git clone https://github.com/mohad-younis/LibraryFace.git
   cd LibraryFace
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   python main.py
   ```

> You must be connected to the internet for poster downloading to work.

---

## 📦 Requirements

- Python 3.10+
- `requests`, `customtkinter`, `pandas`, `Pillow`, and others (see `requirements.txt`)

---

## 🤝 Contributing

Got an idea or fix?  
Fork the repo → create a branch → submit a pull request — we’d love your help!

---

## 📄 License

All rights reserved.  
This software is proprietary and may not be copied, distributed, reverse-engineered, or modified in any form without explicit written permission from the author.

---

## 🙏 Acknowledgments

- [TMDb](https://www.themoviedb.org/)
- [Jikan API](https://jikan.moe/)
- [OMDb](https://www.omdbapi.com/)

---

> _“Let your folders speak for themselves.”_
