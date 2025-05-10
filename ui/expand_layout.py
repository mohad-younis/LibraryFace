import io
from core.config import io, os, requests, UnidentifiedImageError, HOVER_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, ctk, Image, CTkImage, header_image, Main_BACKGROUND, ACCENT_COLOR, PANNELS, Path, DISABLED_COLOR
import core.config as config

from ui.handlers.undo import on_apply_changes

from ui import layout
from ui import state
from ui.handlers.preview import go_back
from ui.match_layout import show_match_popup


def toggle_select_all_undo():
    value = state.select_all_undo_var.get()
    for poster in state.preview_posters:
        poster["undo_var"].set(value)

def check_if_all_undo_selected():
    # If any poster undo_var is False, uncheck the Select All box
    if all(poster["undo_var"].get() for poster in state.preview_posters):
        state.select_all_undo_var.set(True)
    else:
        state.select_all_undo_var.set(False)

def apply_hover_bold(widget, normal_btn_font, bold_btn_font):
    widget.bind("<Enter>", lambda e: widget.configure(
        font=bold_btn_font,
         text_color=TEXT_PRIMARY  # ✅ when hovering: bold + white text
    ))
    widget.bind("<Leave>", lambda e: widget.configure(
        font=normal_btn_font,
        text_color=TEXT_SECONDARY  # ✅ when not hovering: normal + gray text
    ))

def build_expand_window():
    global expand_container
    expand_container = ctk.CTkFrame(layout.app, fg_color=Main_BACKGROUND)
    expand_container.pack(fill="both", expand=True, padx=0, pady=0)

    top_spacer = ctk.CTkFrame(expand_container, fg_color="transparent", height=10)
    top_spacer.pack(fill="x")

    header_row = ctk.CTkFrame(expand_container, fg_color="transparent")
    header_row.pack(fill="x", padx=20, pady=(10, 20))

    image_label = ctk.CTkLabel(header_row, image=header_image, text="")
    image_label.pack(side="left", padx=(0, 5))

    ctk.CTkLabel(header_row, text="LibraryFace", font=("Segoe UI", 18, "bold"), text_color=ACCENT_COLOR).pack(side="left")

    main_frame = ctk.CTkFrame(expand_container, fg_color=PANNELS, corner_radius=10)
    main_frame.pack(expand=True, padx=20, pady=(0, 20), fill="both")
    
    # Top container holding everything
    top_container = ctk.CTkFrame(main_frame, fg_color="transparent")
    top_container.pack(fill="x", padx=10, pady=5)

    global back_btn
    back_btn = ctk.CTkButton(
        top_container,
        text="❮",
        font=("Segoe UI", 20),
        width=32,
        fg_color="transparent",
        text_color=TEXT_SECONDARY,
        hover_color=Main_BACKGROUND,
        command=go_back
    )
    normal_back_btn = ("Segoe UI", 20)
    bold_back_btn = ("Segoe UI", 20, "bold")
    apply_hover_bold(back_btn, normal_back_btn, bold_back_btn)
    back_btn.pack(side="left")

    ctk.CTkLabel(
        top_container,
        text="Expanded View",
        font=("Segoe UI", 16, "bold"),
        text_color=TEXT_PRIMARY
    ).pack(side="left", padx=(0, 435))

    ctk.CTkLabel(
        top_container,
        text="Select All",
        font=("Segoe UI", 12),
        text_color=TEXT_PRIMARY
    ).pack(side="left", padx=(0, 5))

    select_all_checkbox = ctk.CTkCheckBox(
        top_container,
        text="",
        variable=state.select_all_undo_var,
        command=toggle_select_all_undo,
        checkbox_width=16,
        checkbox_height=16,
        corner_radius=3,
        border_color=DISABLED_COLOR,
        checkmark_color=Main_BACKGROUND,
        fg_color=DISABLED_COLOR,
        hover_color=DISABLED_COLOR
    )
    select_all_checkbox.pack(side="left")

    
    # 🖼 Scrollable canvas to contain poster panels
    border_fram = ctk.CTkFrame(main_frame, fg_color=Main_BACKGROUND, corner_radius=10, border_color=Main_BACKGROUND, border_width=2)
    border_fram.pack(expand=True, fill="both",padx=10)

    scroll_frame = ctk.CTkScrollableFrame(border_fram,  fg_color="transparent")
    scroll_frame.pack(expand=True, fill="both", padx=5, pady=5)

    tail_frame = ctk.CTkFrame(main_frame, fg_color="transparent",height=30)
    tail_frame.pack(fill="x",padx=10, pady=10)
    tail_frame.pack_propagate(False)

    ctk.CTkLabel(tail_frame, text="⚠️ Note: Some changes may not appear until you restart your device.", font=("Segoe UI", 13)).pack(side="left", padx=(10, 100))

    apply_button = ctk.CTkButton(
        tail_frame,
        text="Apply Changes",
        font=("Segoe UI", 14, "bold"),
        width=100,
        height=30,
        corner_radius=6,
        fg_color=ACCENT_COLOR,
        hover_color=HOVER_COLOR,
        text_color="white",
        command=on_apply_changes
    )
    apply_button.pack(side="left")
    
    for poster in state.preview_posters:
        def create_poster_panel(poster):
            folder_path = poster["folder_path"]
            jpg_path = poster["jpg_path"]
            preview_name = poster["old_title"]
            final_folder_name = poster["clean_title"]
            content = poster["content_type"]
            title_var = poster["title_var"]
            undo_var = poster["undo_var"]
            anime_url = poster["anime_poster"]
            tv_url = poster["tv_poster"]
            movie_url = poster["movie_poster"]
            
            # Poster panel
            poster_panel = ctk.CTkFrame(scroll_frame, fg_color=PANNELS, corner_radius=10)
            poster_panel.pack(fill="x", padx=(0, 10), pady=(0, 10))

            poster_container = ctk.CTkFrame(poster_panel, fg_color="transparent", width=100, height=140)
            poster_container.pack(side="left", padx=10, pady=10)
            poster_container.pack_propagate(False)

            # Image
            if os.path.exists(jpg_path):
                try:
                    with Image.open(jpg_path) as img:
                        image = img.resize((100, 140))
                except UnidentifiedImageError:
                    return
                except Exception as e:
                    return
            else:
                return

            ctk_image = CTkImage(light_image=image, size=(100, 140))
            poster_label = ctk.CTkLabel(poster_container, image=ctk_image, text="")
            poster["label_widget"] = poster_label  # Save the reference to update later
            poster["new_poster_url"] = None
            poster_label.image = ctk_image  # type: ignore # prevent garbage collection
            poster_label.place(relx=0.5, rely=0.5, anchor="center")

            poster_count = sum(bool(url) for url in [anime_url, tv_url, movie_url])
            if poster_count >= 2:
                edit_button = ctk.CTkButton(
                    poster_container,
                    text="✎",
                    width=14,
                    height=10,
                    text_color=TEXT_SECONDARY,
                    font=("Segoe UI", 10),
                    corner_radius=0,
                    border_width=1,
                    border_color=DISABLED_COLOR,
                    fg_color=PANNELS,       # Transparent background
                    hover_color=DISABLED_COLOR,  # Transparent hover effect      
                    command=lambda: show_match_popup(poster_container.winfo_toplevel(), poster)
                )
                edit_button.place(relx=1.0, rely=0.0, anchor="ne", x=-4, y=4)
            
            # Info box
            info_box = ctk.CTkFrame(poster_panel, fg_color="transparent", width=420, height=140)
            info_box.pack(side="left", fill="y", padx=(10, 0), pady=10)
            info_box.pack_propagate(False)

            ctk.CTkLabel(info_box, text=f"Folder Name:  {preview_name}", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))

            if state.show_rename_edit:
                title_wrapper = ctk.CTkFrame(info_box, fg_color="transparent")
                title_wrapper.pack(anchor="w", pady=(0, 5))

                # Add "Clean Title:" label
                title_prefix = ctk.CTkLabel(
                    title_wrapper,
                    text="Clean Title: ",
                    font=("Segoe UI", 11),
                    text_color=TEXT_PRIMARY
                )
                title_prefix.pack(side="left")

                # This frame holds either the label or entry
                title_frame = ctk.CTkFrame(title_wrapper, fg_color="transparent")
                title_frame.pack(side="left")

                # Get current title from poster
                original_title = final_folder_name

                # Default view: label with original clean title (not linked to title_var yet)
                title_label = ctk.CTkLabel(
                    title_frame,
                    text=original_title,
                    font=("Segoe UI", 11),
                    text_color=TEXT_SECONDARY
                )
                title_label.pack(side="left")

                def switch_to_entry():
                    title_label.pack_forget()
                    pin_button.pack_forget()

                    entry = ctk.CTkEntry(
                        title_frame,
                        textvariable=title_var,
                        width=160
                    )
                    entry.pack(side="left")
                    entry.focus()

                    def handle_focus_out(event):
                        if event.widget != entry:
                            finish_edit(entry)

                    entry.bind("<Return>", lambda e: finish_edit(entry))
                    entry.bind("<FocusOut>", handle_focus_out)

                def finish_edit(entry):
                    entry.pack_forget()
                    # Get updated title
                    updated = title_var.get()
                    title_label.configure(text=updated)
                    title_label.pack(side="left")
                    pin_button.pack(side="left", padx=(8, 0))

                pin_button = ctk.CTkButton(
                    title_frame,
                    text="✎",
                    width=14,
                    height=14,
                    text_color=TEXT_SECONDARY,
                    font=("Segoe UI", 14),
                    fg_color="transparent",
                    hover_color=HOVER_COLOR,
                    command=switch_to_entry
                )
                normal_pin_button = ("Segoe UI", 14)
                bold_pin_button = ("Segoe UI", 14, "bold")
                apply_hover_bold(pin_button, normal_pin_button, bold_pin_button)
                pin_button.pack(side="left", padx=(8, 0))

            ctk.CTkLabel(info_box, text=f"Content Type:  {content}", font=("Segoe UI", 11), text_color=TEXT_PRIMARY).pack(anchor="w", pady=(0, 5))
            
            # Undo checkbox
            undo_container = ctk.CTkFrame(poster_panel, fg_color="transparent", width=100, height=24)
            undo_container.pack(side="left", pady=(0, 110))

            ctk.CTkLabel(undo_container, text="Undo", font=("Segoe UI", 12), text_color=TEXT_PRIMARY).pack(side="left", padx=(0, 5))

            undo_box = ctk.CTkCheckBox(
                undo_container,
                text="",
                variable=undo_var,
                command=check_if_all_undo_selected,
                checkbox_width=16,
                checkbox_height=16,
                corner_radius=3,
                border_color=DISABLED_COLOR,
                checkmark_color=Main_BACKGROUND,
                fg_color=DISABLED_COLOR,
                hover_color=DISABLED_COLOR
            )
            undo_box.pack(side="left")

        create_poster_panel(poster)
