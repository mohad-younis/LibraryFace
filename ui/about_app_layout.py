"""
About app layout module for LibraryFace
Shows information about the app with logo when clicking on "About LibraryFace" in the menu
"""

import tkinter as tk
from core.config import TEXT_SECONDARY, HOVER_COLOR, ctk, get_asset_path, Main_BACKGROUND, TEXT_PRIMARY, PANNELS, root
from PIL import Image, ImageTk
import webbrowser
from ui import layout  # Import layout module to access main_container
import sys
import os

class AboutAppLayout:
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
        
        # Get appearance mode index (0 for light, 1 for dark)
        appearance_mode = 0 if ctk.get_appearance_mode() == "Light" else 1
        
        # Create main frame that covers the entire window
        self.frame = tk.Frame(self.parent, bg=Main_BACKGROUND[appearance_mode])
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create top container for back button and title
        top_container = tk.Frame(self.frame, bg=Main_BACKGROUND[appearance_mode])
        top_container.pack(fill="x", padx=20, pady=10)
        
        # Back button using consistent colors from config
        back_btn = ctk.CTkButton(
            top_container,
            text="❮",
            font=("Segoe UI", 20),
            width=32,
            fg_color="transparent",
            text_color=TEXT_SECONDARY[appearance_mode],
            hover_color=HOVER_COLOR[appearance_mode],
            command=self.close
        )
        normal_back_btn = ("Segoe UI", 20)
        bold_back_btn = ("Segoe UI", 20, "bold")
        
        # Apply hover effect with consistent colors
        back_btn.bind("<Enter>", lambda e: back_btn.configure(
            font=bold_back_btn,
            text_color=TEXT_PRIMARY[appearance_mode]
        ))
        back_btn.bind("<Leave>", lambda e: back_btn.configure(
            font=normal_back_btn,
            text_color=TEXT_SECONDARY[appearance_mode]
        ))
        
        back_btn.pack(side="left")
        
        # Title with consistent colors
        title_label = ctk.CTkLabel(
            top_container,
            text="About LibraryFace",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT_PRIMARY[appearance_mode]
        )
        title_label.pack(side="left", padx=10)
        
        # Ensure the frame is on top
        self.frame.lift()
        
        # Add app logo
        try:
            logo_path = get_asset_path("LibraryFace.png")
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((100, 100))  # Resize the logo
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(
                self.frame, 
                image=self.logo_photo, 
                bg=Main_BACKGROUND[appearance_mode]
            )
            logo_label.pack(pady=(120, 20))
        except Exception as e:
            # Create a fallback label if image fails to load
            tk.Label(
                self.frame,
                text="LibraryFace Logo",
                font=("Segoe UI", 16),
                fg=TEXT_PRIMARY[appearance_mode],
                bg=Main_BACKGROUND[appearance_mode]
            ).pack(pady=(60, 10))
        
        # App name
        app_name_label = tk.Label(
            self.frame,
            text="LibraryFace",
            font=("Segoe UI", 18, "bold"),
            fg=TEXT_PRIMARY[appearance_mode],
            bg=Main_BACKGROUND[appearance_mode]
        )
        app_name_label.pack(pady=10)
        
        # Version
        version_label = tk.Label(
            self.frame,
            text="Version 1.0",
            font=("Segoe UI", 10),
            fg=TEXT_PRIMARY[appearance_mode],
            bg=Main_BACKGROUND[appearance_mode]
        )
        version_label.pack(pady=10)
        
        # Description
        description_text = "LibraryFace — Where your media comes to life."
        description_label = tk.Label(
            self.frame,
            text=description_text,
            font=("Segoe UI", 10),
            fg=TEXT_PRIMARY[appearance_mode],
            bg=Main_BACKGROUND[appearance_mode],
            wraplength=500
        )
        description_label.pack(pady=10)
        
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
def show_about_screen(parent, close_callback=None):
    """
    Show the about screen
    
    Args:
        parent: The parent widget
        close_callback: Callback function when closing the about screen
    
    Returns:
        AboutAppLayout: The about app layout instance
    """
    about_screen = AboutAppLayout(parent, close_callback)
    about_screen.show()
    return about_screen