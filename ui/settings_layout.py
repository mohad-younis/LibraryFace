"""
About app layout module for LibraryFace
Shows information about the app with logo when clicking on "About LibraryFace" in the menu
"""

import tkinter as tk
from core.config import ACCENT_COLOR, TEXT_SECONDARY, HOVER_COLOR, ctk, get_asset_path, Main_BACKGROUND, TEXT_PRIMARY, PANNELS, root
from PIL import Image, ImageTk
import webbrowser
from ui import layout  # Import layout module to access main_container
from ui import state  # Import state module to access theme mode variable
import sys
import os
import json

class SettingsLayout:
    def __init__(self, parent, close_callback=None):
        """
        Initialize the about app layout
        
        Args:
            parent: The parent widget
            close_callback: Callback function when closing the about screen
        """
        self.parent = parent
        self.close_callback = close_callback
        self.frame = None
        # Store original window size
        self.original_geometry = None
        
    def show(self):
        """Show the about app layout"""
        # Store the current geometry before changing it
        self.original_geometry = root.geometry()
        
        # Ensure the window is at maximum size before showing the about screen
        if hasattr(root, 'geometry'):
            # Get the maximum size defined in config
            max_width = 720
            max_height = 660
            
            # Set window to maximum size
            root.geometry(f"{max_width}x{max_height}")
            root.update_idletasks()  # Force update to apply the new size
            
        # Hide the main container if it exists
        if hasattr(layout, 'main_container') and layout.main_container.winfo_ismapped():
            layout.main_container.pack_forget()
        
        
        # Create main frame that covers the entire window
        self.frame = ctk.CTkFrame(self.parent, fg_color=Main_BACKGROUND)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)

        main_container = ctk.CTkFrame(self.frame, fg_color=Main_BACKGROUND)
        main_container.pack(fill="both")
        
        # Create top container for back button and title
        top_container = ctk.CTkFrame(main_container, fg_color=Main_BACKGROUND)
        top_container.pack(fill="x", padx=20, pady=(10, 0))
        
        # Back button using consistent colors from config
        back_btn = ctk.CTkButton(
            top_container,
            text="❮",
            font=("Segoe UI", 20),
            width=32,
            fg_color="transparent",
            text_color=TEXT_SECONDARY,
            hover_color=HOVER_COLOR,
            command=self.close
        )
        normal_back_btn = ("Segoe UI", 20)
        bold_back_btn = ("Segoe UI", 20, "bold")
        
        # Apply hover effect with consistent colors
        back_btn.bind("<Enter>", lambda e: back_btn.configure(
            font=bold_back_btn,
            text_color=TEXT_PRIMARY
        ))
        back_btn.bind("<Leave>", lambda e: back_btn.configure(
            font=normal_back_btn,
            text_color=TEXT_SECONDARY
        ))
        
        back_btn.pack(side="left")
        
        # Title with consistent colors
        title_label = ctk.CTkLabel(
            top_container,
            text="Settings",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT_PRIMARY
        )
        title_label.pack(side="left", padx=10)

        # Settings container
        settings_container = ctk.CTkFrame(main_container, fg_color=Main_BACKGROUND)
        settings_container.pack(fill="both", padx=20, pady=20)

        # Theme mode option
        theme_mode = ctk.CTkFrame(settings_container, fg_color=PANNELS, corner_radius=10)
        theme_mode.pack(fill="both",pady=(0, 10))

        theme_mode_label = ctk.CTkLabel(
            theme_mode,
            text="Theme:",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_PRIMARY
        )
        theme_mode_label.pack(side="left", padx=20, pady=10)
        
        theme_mode_option  = ctk.CTkOptionMenu(
            theme_mode,
            values=["Light", "Dark", "System"],
            font=("Segoe UI", 14),
            width=130,
            height=32,
            dropdown_font=("Segoe UI", 12),
            fg_color=ACCENT_COLOR,
            button_color=ACCENT_COLOR,
            button_hover_color=HOVER_COLOR,
            command=lambda mode: (ctk.set_appearance_mode(mode), save_theme_to_config(mode))
        )
        theme_mode_option.set(ctk.get_appearance_mode())
        theme_mode_option.pack(side="left", padx=10, pady=10)
        
        # Bind escape key to close
        self.parent.bind("<Escape>", lambda e: self.close())
        
    def close(self):
        """Close the about screen"""
        if self.frame:
            self.frame.destroy()
            self.frame = None
            # Unbind the escape key
            self.parent.unbind("<Escape>")
            
        # Restore the main container
        if hasattr(layout, 'main_container'):
            layout.main_container.pack(fill="both", expand=True, padx=0, pady=0)
            
        # Restore the original window size
        if self.original_geometry:
            # Schedule geometry change after a short delay to ensure smooth transition
            root.after(100, lambda: root.geometry(self.original_geometry))
            
        # Call the close callback if provided
        if self.close_callback:
            self.close_callback()

# Helper function to show about screen
def show_settings_screen(parent, close_callback=None):
    """
    Show the about screen
    
    Args:
        parent: The parent widget
        close_callback: Callback function when closing the about screen
    
    Returns:
        AboutAppLayout: The about app layout instance
    """
    about_screen = SettingsLayout(parent, close_callback)
    about_screen.show()
    return about_screen

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".libraryface_settings.json")
def save_theme_to_config(mode):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"theme": mode}, f)