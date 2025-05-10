from core.config import root

from logic.deiconify_utils.deiconify import deiconify
from logic.iconify_utils.iconify import iconify

from ui import layout
from ui import state
from ui.helpers.process import on_process_complete 
from ui.handlers.preview import load_preview_list

def run_iconify():
    try:
        layout.toggle_log_btn.pack(side="right", padx=0)
        layout.content_frame.pack(padx=20, pady=(10, 20), fill="both", expand=True)
        root.update_idletasks()
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

        state.preview_posters = iconify()
        if state.preview_posters:
            load_preview_list() 

    except StopIteration:
        pass
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        root.after(0, on_process_complete)

def run_deiconify():
    try:
        layout.toggle_log_btn.pack_forget()
        layout.content_frame.pack_forget()
        root.update_idletasks()
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight() +15}")
        deiconify()
    except StopIteration:
        pass
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        root.after(0, on_process_complete)