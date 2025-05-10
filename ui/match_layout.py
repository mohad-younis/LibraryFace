import customtkinter as ctk
import tkinter as tk
from core.config import os, ACCENT_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, HOVER_COLOR, PANNELS, Main_BACKGROUND, DISABLED_COLOR
from logic.undo_utils.replace_poster import replace_poster
from ui.handlers.match_posters import fetch_image_preview
from ui import state
from ui.handlers.preview import refresh_current_poster
from ui.helpers.expand_helper import refresh_expand_window

def show_match_popup(parent, poster):
    popup = tk.Toplevel(parent)
    popup.withdraw()  # Hide initially to avoid flickering
    popup.overrideredirect(True)  # Remove title bar
    popup.attributes('-topmost', True)  # Keep on top
    
    # Add slight transparency like the menu
    try:
        # For Windows
        popup.attributes('-alpha', 0.95)  # Slight transparency
    except:
        pass
    
    # Set dimensions and position
    # Determine appropriate size for poster display
    width = 380  # Width suitable for showing posters side by side
    height = 250  # Height to fit posters and labels
    
    # Center on parent
    parent.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
    y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
    popup.geometry(f"{width}x{height}+{x}+{y}")
    
    # Get appearance mode index (0 for light, 1 for dark)
    appearance_mode = 0 if ctk.get_appearance_mode() == "Light" else 1
    
    # Use theme-aware colors
    bg_color = Main_BACKGROUND[appearance_mode]  # Use appropriate color based on theme
    border_color = PANNELS[appearance_mode]  # Use panel color based on theme
    
    # Configure the popup window background
    popup.configure(bg=border_color)
    
    # Main frame with slight padding for border effect
    menu_frame = tk.Frame(popup, bg=border_color)
    menu_frame.pack(fill="both", expand=True, padx=1, pady=1)
    
    # Inner frame with content
    inner_frame = tk.Frame(menu_frame, bg=bg_color)
    inner_frame.pack(fill="both", expand=True)
    
    # Content inside the inner frame
    posters_frame = tk.Frame(inner_frame, bg=bg_color)
    posters_frame.pack(pady=(15, 10), padx=10, fill="both", expand=True)
    
    # Track if popup is already destroyed to prevent errors
    is_destroyed = False
    
    # Store initial parent position for movement detection
    initial_parent_pos = (parent.winfo_rootx(), parent.winfo_rooty())
    
    # Add event handlers for closing
    def close_popup(event=None):
        nonlocal is_destroyed
        if not is_destroyed:
            is_destroyed = True
            parent.unbind("<Button-1>", click_binding)
            # Get root window for unbinding
            root = parent.winfo_toplevel()
            root.unbind("<Button-1>", root_click_binding)
            parent.unbind("<Configure>", configure_binding)
            popup.destroy()
    
    # Close on focus out with cleanup
    def handle_focus_out(event):
        if event.widget != popup and not is_destroyed:
            close_popup()
    
    # Only check for clicks outside if popup still exists
    def on_root_click(event):
        if is_destroyed:
            return
        
        try:
            # Get popup position and dimensions
            popup_x = popup.winfo_rootx()
            popup_y = popup.winfo_rooty()
            popup_width = popup.winfo_width()
            popup_height = popup.winfo_height()
            
            # Check if click was outside popup
            x, y = event.x_root, event.y_root
            if not (popup_x <= x <= popup_x + popup_width and 
                    popup_y <= y <= popup_y + popup_height):
                close_popup()
        except tk.TclError:
            # If the popup was destroyed in another thread/callback
            pass
    
    # Close popup when parent window moves or resizes
    def on_parent_configure(event):
        if is_destroyed:
            return
            
        try:
            # Get current position
            current_x = parent.winfo_rootx()
            current_y = parent.winfo_rooty()
            
            # Compare with initial position
            initial_x, initial_y = initial_parent_pos
            
            # If window has moved significantly, close popup
            if abs(current_x - initial_x) > 5 or abs(current_y - initial_y) > 5:
                close_popup()
        except tk.TclError:
            pass
    
    # Bind focus out and click events
    popup.bind("<FocusOut>", handle_focus_out)
    
    # Bind to parent window clicks
    click_binding = parent.bind("<Button-1>", on_root_click, add="+")
    
    # Also bind to the root window to catch clicks outside the main window
    root = parent.winfo_toplevel()
    root_click_binding = root.bind("<Button-1>", on_root_click, add="+")
    
    configure_binding = parent.bind("<Configure>", on_parent_configure, add="+")
    
    # Clean up binding when popup is closed
    popup.protocol("WM_DELETE_WINDOW", close_popup)
    
    # Title label at the top
    title_label = tk.Label(
        posters_frame,
        text="Select a Poster",
        font=("Segoe UI", 11, "bold"),
        bg=bg_color,
        fg=TEXT_PRIMARY[appearance_mode]
    )
    title_label.pack(pady=(0, 10))

    # Container for posters

    poster_sources = [
        ("Anime", poster.get("anime_poster")),
        ("TV Show", poster.get("tv_poster")),
        ("Movie", poster.get("movie_poster"))
    ]

    poster_container = tk.Frame(posters_frame, bg=bg_color)
    poster_container.pack(fill="both", expand=True)

    for widget in poster_container.winfo_children():
        widget.destroy()

    active_posters = [(name, url) for name, url in poster_sources if url]
    total = len(active_posters)

    for index, (name, url) in enumerate(active_posters):
        if url:
            def on_click(u, n):  # use default argument to lock value
                close_popup()  # Use our safe close function
                poster["content_type"] = n
                poster["new_poster_url"] = u

                image_preview  = fetch_image_preview(u)
                if image_preview :
                    poster["label_widget"].configure(image=image_preview )
                    poster["label_widget"].image = image_preview 
                state.to_replace.append(poster)

            image = fetch_image_preview(url)
            if image:
                # Create vertical frame for each poster + label
                poster_frame = tk.Frame(poster_container, bg=bg_color)
                poster_frame.grid(row=0, column=index, padx=10)

                # Poster image
                img_label = ctk.CTkLabel(poster_frame, image=image, text="")
                img_label.bind("<Button-1>", lambda e, u=url, n=name: on_click(u, n))
                img_label.pack()

                # Poster type label
                type_label = tk.Label(
                    poster_frame,
                    text=name,
                    font=("Segoe UI", 10),
                    bg=bg_color,
                    fg=TEXT_SECONDARY[appearance_mode]
                )
                type_label.pack(pady=(4, 0))

                # Add hover effect for each poster frame
                def on_enter(e, frame=poster_frame, label=type_label):
                    frame.config(bg=DISABLED_COLOR[appearance_mode])
                    label.config(bg=DISABLED_COLOR[appearance_mode])
                
                def on_leave(e, frame=poster_frame, label=type_label):
                    frame.config(bg=bg_color)
                    label.config(bg=bg_color)
                
                poster_frame.bind("<Enter>", on_enter)
                poster_frame.bind("<Leave>", on_leave)
                type_label.bind("<Enter>", on_enter)
                type_label.bind("<Leave>", on_leave)
                img_label.bind("<Enter>", on_enter)
                img_label.bind("<Leave>", on_leave)

    poster_container.grid_columnconfigure(tuple(range(total)), weight=1)

    def check_focus_loop():
        if is_destroyed:
            return  # popup already closed
        try:
            # If nothing in the popup has focus, close it
            if not popup.focus_displayof():
                close_popup()
            else:
                popup.after(200, check_focus_loop)  # Check again after 200ms
        except tk.TclError:
            pass  # popup might already be destroyed

    # Show the popup now that it's configured
    check_focus_loop()
    popup.deiconify()
    popup.focus_set()

