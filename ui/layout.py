# ui.layout
from core.config import (
    STOP_HOVER,
    ctk, 
    root,  header_image,
    Main_BACKGROUND, ACCENT_COLOR, PANNELS, TEXT_PRIMARY, TEXT_SECONDARY, HOVER_COLOR, DISABLED_COLOR , STOP_COLOR
) 

from ui import state
from .helpers.expand import show_expand_window
from .helpers.menu import app_menu
from .handlers.general import on_stop, toggle_log, on_start
from .handlers.preview import show_prev_poster, show_next_poster
from .handlers.options import toggle_options, update_mode_description
from .handlers.undo import on_undo_click
from .helpers.path import browse_folder, update_path_display_hint

# ================
# 🧱 UI Build & App Start 

def apply_hover_bold(widget, normal_btn_font, bold_btn_font):
    widget.bind("<Enter>", lambda e: widget.configure(
        font=bold_btn_font,
        text_color=TEXT_PRIMARY  # ✅ when hovering: bold + white text
    ))
    widget.bind("<Leave>", lambda e: widget.configure(
        font=normal_btn_font,
        text_color=TEXT_SECONDARY  # ✅ when not hovering: normal + gray text
    ))

def build_ui():
    global app
    app = ctk.CTkFrame(root)
    app.pack(expand=True, fill="both")

    global main_container
    main_container = ctk.CTkFrame(app, fg_color=Main_BACKGROUND)
    main_container.pack(fill="both", expand=True, padx=0, pady=0)

    # === Header ===
    top_spacer = ctk.CTkFrame(main_container, fg_color="transparent", height=10)
    top_spacer.pack(fill="x")

    header_row = ctk.CTkFrame(main_container, fg_color="transparent")
    header_row.pack(fill="x", padx=20, pady=(10, 20))

    image_label = ctk.CTkLabel(header_row, image=header_image, text="")
    image_label.pack(side="left", padx=(0, 5))

    ctk.CTkLabel(header_row, text="LibraryFace", font=("Segoe UI", 18, "bold"), text_color=ACCENT_COLOR).pack(side="left")
    
    # Three-dot menu button with improved styling
    menu_button = ctk.CTkButton(
        header_row,
        text="⋮",  # Three vertical dots symbol
        font=("Segoe UI", 20),
        width=30, 
        height=30,
        fg_color="transparent",
        text_color=TEXT_SECONDARY,
        hover_color=Main_BACKGROUND,
        corner_radius=8,
        command=lambda: app_menu.show_menu(menu_button)
    )
    menu_button.pack(side="right")

    # === Path Input ===
    path_frame = ctk.CTkFrame(main_container, fg_color=PANNELS, corner_radius=10)
    path_frame.pack(padx=20, pady=(0, 10), fill="x")

    path_content = ctk.CTkFrame(path_frame, fg_color="transparent")
    path_content.pack(padx=15, pady=15, fill="x")

    folder_icon = ctk.CTkLabel(path_content, text="📁", font=("Segoe UI", 16))
    folder_icon.grid(row=0, column=0, padx=(0, 5))

    path_label = ctk.CTkLabel(path_content, text="Target Folder:", text_color=TEXT_PRIMARY, font=("Segoe UI", 14, "bold"))
    path_label.grid(row=0, column=1, padx=(0, 10), sticky="w")

    global path_display
    path_display = ctk.CTkLabel(path_content, text="No folder selected", font=("Segoe UI", 12), text_color=TEXT_PRIMARY)
    path_display.grid(row=0, column=2, sticky="w", padx=(0, 10))

    browse_btn = ctk.CTkButton(path_content,  text="Browse", command=browse_folder, font=("Segoe UI", 12, "bold"), width=120, height=32, text_color="white", fg_color=ACCENT_COLOR, hover_color=HOVER_COLOR)
    browse_btn.grid(row=0, column=3, padx=0)

    apply_checkbox = ctk.CTkCheckBox(
        path_content, 
        text="Apply to all subfolders", 
        variable=state.apply_to_subfolders, 
        font=("Segoe UI", 11), 
        checkbox_width=14,
        checkbox_height=14,
        corner_radius=3,
        border_color=DISABLED_COLOR,
        checkmark_color=Main_BACKGROUND,
        fg_color=DISABLED_COLOR,
        hover_color=DISABLED_COLOR
    )
    apply_checkbox.grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 0))

    state.apply_to_subfolders.trace_add("write", update_path_display_hint)

    path_content.grid_columnconfigure(2, weight=1)

    update_path_display_hint()

    # === Control Panel ===
    global control_panel
    control_panel = ctk.CTkFrame(main_container, fg_color=PANNELS, corner_radius=10)
    control_panel.pack(padx=20, pady=(0,0), fill="x")

    control_content = ctk.CTkFrame(control_panel, fg_color="transparent")
    control_content.pack(padx=15, pady=(15,15), fill="x")

    # === Mode Selector ===
    mode_label = ctk.CTkLabel(control_content, text="Mode:", text_color=TEXT_PRIMARY, font=("Segoe UI", 14, "bold"))
    mode_label.grid(row=0, column=0, padx=(0, 15), pady=0, sticky="w")

    global mode_selector
    mode_selector = ctk.CTkSegmentedButton(
        control_content,
        values=["  Iconify  ", " Deiconify "],
        variable=state.mode_var,
        font=("Segoe UI", 12),
        fg_color=PANNELS,                     # background for the segmented button area
        selected_color=ACCENT_COLOR,             # active segment
        selected_hover_color=HOVER_COLOR,        # hover on selected
        unselected_color=Main_BACKGROUND,         # non-active segments
        unselected_hover_color=DISABLED_COLOR,   # hover on non-active
        text_color=TEXT_PRIMARY,                 # text color for segments
        corner_radius=8,
        height=32,
        command=update_mode_description
    )
    mode_selector.grid(row=0, column=1, sticky="ew", padx=(0, 10))


    global mode_desc
    mode_desc = ctk.CTkLabel(
        control_content, 
        text="Hi !  Please select a target folder and choose a mode to start the process...", 
        text_color=TEXT_SECONDARY, 
        font=("Segoe UI", 12), 
        anchor="w"
    )
    mode_desc.grid(row=0, column=2, sticky="w", padx=(10, 0))

    control_content.grid_columnconfigure(1, weight=0)
    control_content.grid_columnconfigure(2, weight=1)

    # === Options Panel ===
    global options_frame
    options_frame = ctk.CTkFrame(control_panel, fg_color=Main_BACKGROUND , corner_radius=5)
    options_frame.pack(padx=15, pady=(0, 0), fill="x")
    options_frame.pack_forget()

    options_content = ctk.CTkFrame(options_frame, fg_color="transparent")
    options_content.pack(padx=10, pady=0, fill="x")

    global content_type_container
    content_type_container = ctk.CTkFrame(options_content, fg_color="transparent")
    content_type_container.grid(row=0, column=1, columnspan=3, sticky="w", padx=(0, 20), pady=15)
    content_type_container.grid_remove() 

    options_label = ctk.CTkLabel(
        options_content, 
        text="Options:", 
        font=("Segoe UI", 12, "bold")
    )
    options_label.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="w")

    global jpg_chk
    jpg_chk = ctk.CTkCheckBox(
        options_content, 
        text="Delete JPG", 
        variable=state.jpg_var, 
        font=("Segoe UI", 12),
        checkbox_width=16,
        checkbox_height=16,
        corner_radius=3,
        border_color=DISABLED_COLOR,
        checkmark_color=Main_BACKGROUND,
        fg_color=DISABLED_COLOR,
        hover_color=DISABLED_COLOR
    )
    jpg_chk.grid(row=0, column=1, padx=(0, 20), pady=5, sticky="w")

    global ico_chk
    ico_chk = ctk.CTkCheckBox(
        options_content, 
        text="Delete ICO", 
        variable=state.ico_var, 
        font=("Segoe UI", 12),
        checkbox_width=16,
        checkbox_height=16,
        corner_radius=3,
        border_color=DISABLED_COLOR,
        checkmark_color=Main_BACKGROUND,
        fg_color=DISABLED_COLOR,
        hover_color=DISABLED_COLOR
    )
    ico_chk.grid(row=0, column=2, padx=(0, 20), pady=5, sticky="w")

    global vis_label
    vis_label = ctk.CTkLabel(
        options_content, 
        text="JPG Visibility:", 
        font=("Segoe UI", 12)
    )
    vis_label.grid(row=0, column=3, padx=(0, 20), pady=5, sticky="w")

    global vis_menu
    vis_menu = ctk.CTkOptionMenu(
        options_content, 
        variable=state.visibility_var, 
        values=["hidden", "visible", "skip"], 
        font=("Segoe UI", 12),
        width=130, 
        height=32,
        dropdown_font=("Segoe UI", 12),
        fg_color=ACCENT_COLOR,
        button_color=ACCENT_COLOR,
        button_hover_color=HOVER_COLOR
    )
    vis_menu.grid(row=0, column=4, sticky="w")

    global rename_chk
    rename_chk = ctk.CTkCheckBox(
        content_type_container, 
        text="Clean title", 
        variable=state.rename_folders_var,
        font=("Segoe UI", 12),
        checkbox_width=16,
        checkbox_height=16,
        corner_radius=3,
        border_color=DISABLED_COLOR,
        checkmark_color=Main_BACKGROUND,
        fg_color=DISABLED_COLOR,
        hover_color=DISABLED_COLOR
    )
    rename_chk.grid(row=0, column=0, padx=(0, 20), pady=5, sticky="w")

    content_type_label = ctk.CTkLabel(
        content_type_container, 
        text="Content Type:", 
        font=("Segoe UI", 12)
        )
    content_type_label.grid(row=0, column=1, padx=(0, 10))

    content_type_menu = ctk.CTkOptionMenu(
        content_type_container,
        variable=state.content_type_var,
        values=["Anime", "Movies", "TV Show", "Auto"],
        font=("Segoe UI", 12),
        width=130,
        height=32,
        dropdown_font=("Segoe UI", 12),
        fg_color=ACCENT_COLOR,
        button_color=ACCENT_COLOR,
        button_hover_color=HOVER_COLOR
    )
    content_type_menu.grid(row=0, column=3)


    # === Start & Log Box Buttons ===
    action_frame = ctk.CTkFrame(main_container, fg_color="transparent")
    action_frame.pack(pady=(10, 0), fill="x", padx=20)
    
    global start_btn
    start_btn = ctk.CTkButton(
        action_frame, 
        text="▶ Start Process",
        command=on_start,
        font=("Segoe UI", 14, "bold"),
        fg_color=ACCENT_COLOR,
        hover_color=HOVER_COLOR,
        text_color="white",
        corner_radius=8,
        height=32,
        width=130
    )
    start_btn.pack(side="left", padx=0)

    global stop_btn
    stop_btn = ctk.CTkButton(
        action_frame,
        text="■ Stop",
        command=on_stop,
        font=("Segoe UI", 14, "bold"),
        fg_color=STOP_COLOR,
        hover_color=STOP_HOVER,
        text_color="white",
        corner_radius=8,
        height=32,
        width=65
    )
    stop_btn.pack(side="left", padx=(10, 0))
    stop_btn.pack_forget()

    global toggle_log_btn
    toggle_log_btn = ctk.CTkButton(
        action_frame, 
        text="Show Details ▼",
        command=toggle_log,
        font=("Segoe UI", 14),
        fg_color="transparent",
        hover_color=DISABLED_COLOR,
        text_color=ACCENT_COLOR,
        corner_radius=8,
        height=32,
        width=130,
        border_width=1,
        border_color=ACCENT_COLOR
    )
    toggle_log_btn.pack_forget()

    # === Progress Bar ===
    global progress_value
    progress_value = ctk.DoubleVar(value=0)
    global progress_frame
    progress_frame = ctk.CTkFrame(main_container, fg_color="transparent")

    global progress_bar
    progress_bar = ctk.CTkProgressBar(
        progress_frame, 
        variable=progress_value,
        width=680,
        height=15,
        corner_radius=7,
        progress_color=ACCENT_COLOR,
        fg_color=("gray85", "gray25")
    )
    progress_bar.pack(fill="x", pady=(0, 5))

    global progress_text
    progress_text = ctk.CTkLabel(progress_frame, text="0% (0/0)", font=("Segoe UI", 11))
    progress_text.pack(anchor="e", padx=5)

    progress_frame.pack_forget()

    # === Details ===
    global content_frame
    content_frame = ctk.CTkFrame(main_container, fg_color=PANNELS, corner_radius=10, height=220)
    content_frame.pack_forget()
    content_frame.pack_propagate(False)

    preview_frame = ctk.CTkFrame(content_frame, fg_color=Main_BACKGROUND, corner_radius=6, height=200)
    preview_frame.pack(side="left", padx=10, pady=10)
    content_frame.pack_propagate(False)
    # Preview poster
    poster_frame = ctk.CTkFrame(preview_frame, fg_color=PANNELS, width=120, height=180)
    poster_frame.pack(side="left",pady=10, padx=10)
    poster_frame.pack_propagate(False)

    global poster_preview
    poster_preview = ctk.CTkLabel(poster_frame, text="No preview", width=120, height=180)
    poster_preview.pack(side="left")

    # Poster info
    info_frame = ctk.CTkFrame(preview_frame, fg_color="transparent", corner_radius=6, width=260, height=200)
    info_frame.pack(side="left", padx=10)
    info_frame.pack_propagate(False)

    titles_frame = ctk.CTkFrame(info_frame, fg_color="transparent", corner_radius=6, width=260, height=150)
    titles_frame.pack(fill="x")
    titles_frame.pack_propagate(False)

    poster_info = ctk.CTkLabel(titles_frame, text="Poster Info...", font=("Segoe UI", 13, "bold"))
    poster_info.pack(anchor="w", pady=(0, 5))

    global folder_name_label
    folder_name_label = ctk.CTkLabel(titles_frame, text="Folder Name: ", font=("Segoe UI", 11, "bold"), wraplength=250, text_color=TEXT_PRIMARY, justify="left")
    folder_name_label.pack(anchor="w", pady=(0, 5))

    global clean_title_label
    clean_title_label = ctk.CTkLabel(titles_frame, text="Clean Title: ", font=("Segoe UI", 11), wraplength=250, text_color=TEXT_PRIMARY, justify="left")
    clean_title_label.pack(anchor="w", pady=(0, 5))

    global type_label
    type_label = ctk.CTkLabel(titles_frame, text="Type: ", font=("Segoe UI", 11), wraplength=250, text_color=TEXT_PRIMARY, justify="left")
    type_label.pack(anchor="w", pady=(0, 20))

    preview_buttons_frame = ctk.CTkFrame(info_frame, fg_color="transparent", corner_radius=6, width=260, height=50)
    preview_buttons_frame.pack(fill="x")
    preview_buttons_frame.pack_propagate(False)

    # Undo Button
    global undo_btn
    undo_btn = ctk.CTkButton(
        preview_buttons_frame,
        text="↩",
        font=("Segoe UI", 15),
        width=32,
        fg_color="transparent",
        text_color=TEXT_SECONDARY,
        hover_color=Main_BACKGROUND,
        command=on_undo_click
    )
    normal_undo_btn = ("Segoe UI", 15)
    bold_undo_btn = ("Segoe UI", 16, "bold")
    apply_hover_bold(undo_btn, normal_undo_btn, bold_undo_btn)
    undo_btn.grid_forget()

    # Previous Button
    global prev_btn
    prev_btn = ctk.CTkButton(
        preview_buttons_frame,
        text="◀",
        font=("Segoe UI", 15),
        width=32,
        fg_color="transparent",
        text_color=TEXT_SECONDARY,
        hover_color=Main_BACKGROUND,
        command=show_prev_poster
    )
    normal = ("Segoe UI", 15)
    bold = ("Segoe UI", 16, "bold")
    apply_hover_bold(prev_btn, normal, bold)
    prev_btn.grid_forget()

    # Counter Label (no hover styling needed)
    global counter_label
    counter_label = ctk.CTkLabel(preview_buttons_frame, text="0 / 0", font=("Segoe UI", 12), text_color=TEXT_PRIMARY)
    counter_label.grid_forget()

    # Next Button
    global next_btn
    next_btn = ctk.CTkButton(
        preview_buttons_frame,
        text="▶",
        font=("Segoe UI", 15),
        width=32,
        fg_color="transparent",
        text_color=TEXT_SECONDARY,
        hover_color=Main_BACKGROUND,
        command=show_next_poster
    )
    apply_hover_bold(next_btn, normal, bold)
    next_btn.grid_forget()

    # Expand Button
    global expand_btn
    expand_btn = ctk.CTkButton(
        preview_buttons_frame,
        text="⌞ ⌝ ",
        font=("Segoe UI", 15),
        width=32,
        fg_color="transparent",
        text_color=TEXT_SECONDARY,
        hover_color=Main_BACKGROUND,
        command=show_expand_window
    )
    normal_expand_btn = ("Segoe UI", 15)
    bold_expand_btn = ("Segoe UI", 16, "bold")
    apply_hover_bold(expand_btn, normal_expand_btn, bold_expand_btn)
    expand_btn.grid_forget()

   # 📝 Left Side - Log Box
    log_frame = ctk.CTkFrame(content_frame, fg_color="transparent", width=250)
    log_frame.pack(side="right", expand=True, padx=(0, 10))
    log_frame.pack_propagate(False)

    operation_log = ctk.CTkLabel(log_frame, text="Operation Log", font=("Segoe UI", 13, "bold"))
    operation_log.pack(anchor="w", pady=(0, 2))

    global log_box
    log_box = ctk.CTkTextbox(
        log_frame, 
        height=250, 
        wrap="word", 
        font=("Cascadia Mono", 11),
        corner_radius=6,
        border_width=1,
        border_color=DISABLED_COLOR,
        fg_color=Main_BACKGROUND
    )
    log_box.pack(fill="both", expand=True)
    log_box.configure(state="disabled")



    state.mode_var.trace_add("write", toggle_options)
    state.jpg_var.trace_add("write", toggle_options)
