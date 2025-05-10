from core.config import ctk, root, TEXT_PRIMARY

from ui import layout
from ui import state

def update_mode_description(value=None):
    mode = state.mode_var.get()

    if mode == "  Iconify  ":
        layout.mode_desc.configure(text="Create icons for your folders using online databases")
    elif mode == " Deiconify ":
        layout.mode_desc.configure(text="Remove folder icons and optionally delete image files")

    if ctk.get_appearance_mode() == "Light":
        for segment in layout.mode_selector._buttons_dict:
            layout.mode_selector._buttons_dict[segment].configure(
                text_color=TEXT_PRIMARY,
                font=("Segoe UI", 12)
            )
    else:
        for segment in layout.mode_selector._buttons_dict:
            layout.mode_selector._buttons_dict[segment].configure(
                text_color=TEXT_PRIMARY,
                font=("Segoe UI", 12)
            )

def toggle_options(*args):
    mode = state.mode_var.get()
    update_mode_description()
    layout.options_frame.forget()
    layout.control_panel.pack_configure(pady=(0, 0))
    layout.content_type_container.grid_remove()
    layout.jpg_chk.grid_remove()
    layout.ico_chk.grid_remove()
    layout.vis_label.grid_remove()
    layout.vis_menu.grid_remove()

    if mode == "  Iconify  ":
        layout.options_frame.pack(padx=15, pady=(15, 15), fill="x")
        layout.content_type_container.grid(row=0, column=1, columnspan=3, padx=(0, 20), pady=5, sticky="w")
    elif mode == " Deiconify ":
        layout.options_frame.pack(padx=15, pady=(15, 15), fill="x")
        layout.jpg_chk.grid(row=0, column=1, padx=(0, 20), pady=5, sticky="w")
        layout.ico_chk.grid(row=0, column=2, padx=(0, 20), pady=5, sticky="w")
        if not state.jpg_var.get():
            layout.vis_label.grid(row=0, column=3, padx=(0, 20), pady=5, sticky="w")
            layout.vis_menu.grid(row=0, column=4, padx=(0, 20), pady=5, sticky="w")

    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight() +20}")
