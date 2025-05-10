from core.config import Image, CTkImage

from ui import layout
from ui import expand_layout
from ui import state
from ui.helpers.logs import add_log

def preview_poster(jpg_path, old_title, clean_title, content_type):
    try:
        img = Image.open(jpg_path)
        
        target_width = 120
        target_height = 180
        
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        img_ctk = CTkImage(light_image=img, size=(target_width, target_height))
        layout.poster_preview.configure(image=img_ctk, text="")
        try:
            layout.counter_label.configure(text=f"{state.current_index + 1} / {len(state.preview_posters)}")
        except:
            pass

        # Update extra labels (only if data available)
        try:
            layout.folder_name_label.configure(text=f'Folder Name:  {old_title}')
            layout.clean_title_label.configure(text=f'Clean Title:  {clean_title}')
            layout.type_label.configure(text=f'Content Type:  {content_type}')
        except:
            pass
        layout.poster_preview.image = img_ctk  # type: ignore[attr-defined]
    except Exception as e:
        print(f"[Preview Error] {e}")

def load_preview_list():
    state.current_index = 0
    if state.preview_posters:
        poster = state.preview_posters[0]
        preview_poster(
            poster["jpg_path"],
            poster["old_title"],
            poster["clean_title"],
            poster["content_type"]
        )
        layout.undo_btn.grid(row=0, column=0, padx=(0, 45))
        layout.prev_btn.grid(row=0, column=1, padx=(0, 5))
        layout.counter_label.grid(row=0, column=2, padx=(0, 5))
        layout.next_btn.grid(row=0, column=3, padx=(0, 45))
        layout.expand_btn.grid(row=0, column=4, padx=0)

def show_next_poster():
    if state.preview_posters and 0 <= state.current_index < len(state.preview_posters) - 1:
        state.current_index += 1
        poster = state.preview_posters[state.current_index]
        preview_poster(
            poster["jpg_path"],
            poster["old_title"],
            poster["clean_title"],
            poster["content_type"]
        )
    else:
        state.current_index = 0
        poster = state.preview_posters[0]
        preview_poster(
            poster["jpg_path"],
            poster["old_title"],
            poster["clean_title"],
            poster["content_type"]
        )

def show_prev_poster():
    if state.preview_posters and 0 < state.current_index < len(state.preview_posters):
        state.current_index -= 1
        poster = state.preview_posters[state.current_index]
        preview_poster(
            poster["jpg_path"],
            poster["old_title"],
            poster["clean_title"],
            poster["content_type"]
        )
    else:
        state.current_index = len(state.preview_posters) - 1
        poster = state.preview_posters[-1]
        preview_poster(
            poster["jpg_path"],
            poster["old_title"],
            poster["clean_title"],
            poster["content_type"]
        )

        
def go_back():
    if expand_layout.expand_container:
        expand_layout.expand_container.destroy()
        expand_layout.expand_container = None
    layout.main_container.pack(fill="both", expand=True, padx=0, pady=0)

def refresh_current_poster():
    """Refreshes the display for the current poster without changing the index"""
    if state.preview_posters and 0 <= state.current_index < len(state.preview_posters):
        poster = state.preview_posters[state.current_index]
        preview_poster(
            poster["jpg_path"],
            poster["old_title"],
            poster["clean_title"],
            poster["content_type"]
        )
    else:
        # Handle empty state or invalid index
        layout.poster_preview.configure(image=None, text="No posters")
        layout.counter_label.configure(text="0 / 0")