import tkinter as tk
from core.config import ctk, DISABLED_COLOR, TEXT_PRIMARY, Main_BACKGROUND, PANNELS
from ui.about_app_layout import show_about_screen
from ui.settings_layout import show_settings_screen

class AppMenu:
    def __init__(self):
        self.menu = None
        self.menu_open = False
        self.root = None
        self.click_count = 0  # Store click count in the class instead of on the Toplevel
        
    def show_menu(self, button, x_offset=0, y_offset=0):
        """Show the menu at the specified position"""
        if self.menu_open:
            self.close_menu()
            return
        
        # Store reference to the root window
        self.root = button.winfo_toplevel()
        
        # Get button position - modified to position to the left of the button
        button_x = button.winfo_rootx() + x_offset
        button_y = button.winfo_rooty() + y_offset
        
        # Create menu window
        self.menu = tk.Toplevel(self.root)
        self.menu.withdraw()  # Hide initially to avoid flickering
        self.menu.overrideredirect(True)
        self.menu.attributes('-topmost', True)
        
        # Add drop shadow effect (use attributes where available)
        try:
            # For Windows
            self.menu.attributes('-alpha', 0.97)  # Slight transparency
        except:
            pass
            
        # Position the menu properly (to the left of the button)
        menu_width = 145
        menu_height = 68
        
        # Calculate position to the left of the button
        menu_x = button_x - menu_width
        
        # Align top of menu with the top dot of three dots button (approximately)
        # This positions the top border of the menu at the same height as the top dot
        menu_y = button_y + 10
        
        self.menu.geometry(f"{menu_width}x{menu_height}+{menu_x}+{menu_y}")
        
        # Get appearance mode index (0 for light, 1 for dark)
        appearance_mode = 0 if ctk.get_appearance_mode() == "Light" else 1
        
        # Use theme-aware colors
        bg_color = Main_BACKGROUND[appearance_mode]  # Use appropriate color based on theme
        border_color = PANNELS[appearance_mode]  # Use panel color based on theme
        
        # Configure the root window background
        self.menu.configure(bg=border_color)
        
        # Main frame with slight padding for border effect
        menu_frame = tk.Frame(self.menu, bg=border_color)
        menu_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Inner frame with content
        inner_frame = tk.Frame(menu_frame, bg=bg_color)
        inner_frame.pack(fill="both", expand=True)
        
        # Add menu items
        self._add_menu_item(inner_frame, "ℹ  About LibraryFace", self._on_about_click)
        self._add_menu_item(inner_frame, "⚙️  Settings", self. _on_settings_click)
        
        # Setup event handlers
        self.menu.bind("<FocusOut>", self._on_focus_out)
        self.root.bind("<Configure>", self._on_window_configure)
        self.root.bind("<Button-1>", self._on_root_click, add="+")
        self.menu.bind("<Button-1>", self._on_menu_click, add="+")
        
        # Reset click counter
        self.click_count = 0
        
        # Show the menu now that it's configured
        self.menu.deiconify()
        self.menu.focus_set()
        self.menu_open = True
    
    def close_menu(self):
        """Close the menu"""
        if not self.menu_open:
            return
            
        # Clean up bindings
        if self.root:
            try:
                self.root.unbind("<Configure>")
                self.root.unbind("<Button-1>")
            except:
                pass
                
        # Destroy menu
        if self.menu:
            try:
                self.menu.destroy()
            except:
                pass
            self.menu = None
            
        self.menu_open = False
    
    def _on_window_configure(self, event):
        """Called when the main window changes (moves/resizes)"""
        # Close menu when window is moved or resized
        if self.menu_open:
            self.close_menu()
    
    def _on_focus_out(self, event):
        """Handle menu losing focus"""
        # Give a tiny delay to allow click events to process first
        if self.menu:
            self.menu.after(100, self._check_focus)
    
    def _check_focus(self):
        """Check if we should close the menu after focus out"""
        if self.menu and self.menu_open and self.menu != self.menu.focus_get():
            self.close_menu()
    
    def _on_root_click(self, event):
        """Handle clicks on the root window"""
        if self.menu_open:
            # Get menu position and dimensions
            if not self.menu:
                return
                
            menu_x = self.menu.winfo_rootx()
            menu_y = self.menu.winfo_rooty()
            menu_width = self.menu.winfo_width()
            menu_height = self.menu.winfo_height()
                
            # Check if click was outside menu
            x, y = event.x_root, event.y_root
            if not (menu_x <= x <= menu_x + menu_width and 
                    menu_y <= y <= menu_y + menu_height):
                self.close_menu()
    
    def _on_menu_click(self, event):
        """Handle clicks inside the menu"""
        # Track clicks inside menu to prevent immediate closure
        self.click_count += 1  # Increment click count in the class
    
    def _add_menu_item(self, parent, text, command):
        """Add a menu item to the menu with Discord/Chrome-like styling"""
        frame = tk.Frame(parent, bg=parent["background"])
        frame.pack(fill="x")
        
        # Get appearance mode index (0 for light, 1 for dark)
        appearance_mode = 0 if ctk.get_appearance_mode() == "Light" else 1
        
        label = tk.Label(
            frame,
            text=text,
            font=("Segoe UI", 10),
            bg=parent["background"],
            fg=TEXT_PRIMARY[appearance_mode],  # Use appropriate text color based on theme
            anchor="w",
            padx=10,
            pady=6,
            cursor="hand2"  # Hand cursor on hover
        )
        label.pack(fill="x")
        
        # Bind events for hover effect and click
        def on_enter(e):
            frame.config(bg=DISABLED_COLOR[appearance_mode])  # Use hover color based on theme
            label.config(bg=DISABLED_COLOR[appearance_mode])
            
        def on_leave(e):
            frame.config(bg=parent["background"])
            label.config(bg=parent["background"])
            
        def on_click(e):
            # Execute command first, then close the menu
            command()
            # Now close the menu after command has been executed
            self.close_menu()
            
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        frame.bind("<Button-1>", on_click)
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
        label.bind("<Button-1>", on_click)

    
    def _on_about_click(self):
        """Handle about click"""
        # Use root directly from config instead of self.root
        from core.config import root
        # Show the about screen using the main root window
        show_about_screen(root)

    def _on_settings_click(self):
        """Handle about click"""
        # Use root directly from config instead of self.root
        from core.config import root
        # Show the about screen using the main root window
        show_settings_screen(root)

        
# Create a singleton instance
app_menu = AppMenu()