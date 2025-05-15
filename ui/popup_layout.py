from core.config import (
    DISABLED_COLOR, ctk, tk, root,
    Main_BACKGROUND, TEXT_PRIMARY, TEXT_SECONDARY, PANNELS, ACCENT_COLOR, HOVER_COLOR
)
from ui import state

def build_choice_popup(parent, normalized, on_choice):
    popup = tk.Toplevel(parent)
    popup.withdraw()  # Hide initially to avoid flickering
    popup.overrideredirect(True)  # Remove title bar
    parent.attributes('-topmost', True)
    popup.attributes('-topmost', True)  # Keep on top
    popup.attributes("-toolwindow", False)

    popup.after(200, lambda: parent.attributes('-topmost', False))
    popup.after(200, lambda: popup.attributes('-topmost', False))

    # Add slight transparency like the menu
    try:
        # For Windows
        popup.attributes('-alpha', 1)  # Slight transparency
    except:
        pass
    
    # Determine appropriate size for poster display
    width = 382  # Width suitable for showing posters side by side
    height = 270  # Height to fit posters and labels
    
    # Center on parent
    parent.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
    y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
    popup.geometry(f"{width}x{height}+{x}+{y}")

    # Get appearance mode index (0 for light, 1 for dark)
    appearance_mode = 0 if ctk.get_appearance_mode() == "Light" else 1
    
    border_color = PANNELS[appearance_mode]  # Use panel color based on theme
    
    # Configure the popup window background
    popup.configure(bg=border_color)
    
    # Main frame with slight padding for border effect
    menu_frame = tk.Frame(popup, bg=border_color)
    menu_frame.pack(fill="both", expand=True, padx=1, pady=1)
    
    # Inner frame with content
    inner_frame = ctk.CTkFrame(menu_frame, fg_color=Main_BACKGROUND)
    inner_frame.pack(fill="both", expand=True, padx=0, pady=0)

    label_fram = ctk.CTkFrame(inner_frame, fg_color="transparent")
    label_fram.pack(padx=20, pady=(20, 10), fill="x")

    label = ctk.CTkLabel(
        label_fram,
        text="Unrecognized Folder Title",
        font=("Segoe UI", 18, "bold"),
        text_color=TEXT_PRIMARY
    )
    label.pack(pady=(0, 0))
    
    choice_fram = ctk.CTkFrame(inner_frame, fg_color=PANNELS, corner_radius=10)
    choice_fram.pack(padx=20, pady=(10, 10), fill="x")

    sub_label_row = ctk.CTkFrame(choice_fram, fg_color="transparent")
    sub_label_row.pack(padx=10, pady=(10, 10), fill="x")

    sub_label = ctk.CTkLabel(
        sub_label_row,
        text=("Couldn’t determine the type of:"),
        font=("Segoe UI", 13),
        justify="center",
        text_color=TEXT_PRIMARY
    )
    sub_label.pack(padx=10)

    title_label_row = ctk.CTkFrame(choice_fram, fg_color=Main_BACKGROUND, corner_radius=8)
    title_label_row.pack(padx=10, pady=(0, 10), fill="x")

    title_label = ctk.CTkLabel(
        title_label_row,
        text=(normalized),
        font=("Segoe UI", 13),
        justify="center",
        text_color=TEXT_SECONDARY
    )
    title_label.pack(anchor="center", pady=5)

    button_row = ctk.CTkFrame(choice_fram, fg_color="transparent")
    button_row.pack(padx=5, pady=(0, 10), fill="x")
 
    def on_click(label):  # lock the label value
        choice_data = {
            "label": label,
            "apply_all": state.apply_all_var.get()
        }
        on_choice(choice_data)
        popup.destroy()

    for index, (label, emoji) in enumerate([("Anime", "🎌"), ("TV Show", "📺"), ("Movies", "🎬")]):
        ctk.CTkButton(
            button_row,
            text=f"{emoji} {label}",
            command=lambda l=label: on_click(l),
            font=("Segoe UI", 12),
            fg_color=ACCENT_COLOR,
            text_color=TEXT_PRIMARY,
            hover_color=HOVER_COLOR,
            corner_radius=8,
            width=100,
            height=32
        ).pack(side="left", padx=5)

    skip_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
    skip_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 20))
    
    skip_btn = ctk.CTkButton(
        skip_frame,
        text="⏭️ Skip",
        command=lambda: on_click("Skipped"),
        font=("Segoe UI", 12),
        fg_color="transparent",
        hover_color=DISABLED_COLOR,
        text_color=ACCENT_COLOR,
        border_width=1,
        border_color=ACCENT_COLOR,
        corner_radius=8,
        width=110,
        height=30
    )
    skip_btn.pack(side="right")

    apply_all_checkbox = ctk.CTkCheckBox(
        skip_frame,
        text="Apply to all remaining folders",
        variable=state.apply_all_var,
        font=("Segoe UI", 11), 
        text_color=TEXT_SECONDARY,
        checkbox_width=14,
        checkbox_height=14,
        corner_radius=3,
        border_color=DISABLED_COLOR,
        checkmark_color=Main_BACKGROUND,
        fg_color=DISABLED_COLOR,
        hover_color=DISABLED_COLOR
    )
    apply_all_checkbox.pack(side="left")


    def update_popup_position(event):
        if not popup.winfo_exists():
            return
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
        try:
            popup.geometry(f"{width}x{height}+{x}+{y}")
        except tk.TclError:
            pass

    # Bind the main window's movement to update the popup's position
    parent.bind("<Configure>", update_popup_position)

    def keep_popup_on_top(event):
        if not popup.winfo_exists():
            return
        try:
            popup.lift()
            parent.lift()
        except tk.TclError:
            pass


    # Bind focus events to keep the popup and main window on top
    parent.bind("<FocusIn>", keep_popup_on_top)

    def on_popup_close():
        # Unbind the focus event when the popup is closed
        parent.unbind("<FocusIn>")
        parent.unbind("<Configure>")
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_popup_close)


    popup.deiconify()
    popup.grab_set()  
    popup.focus_set()
    popup.wait_window()
