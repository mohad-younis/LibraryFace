from core.config import ctk

# Tkinter UI variables
path_var = ctk.StringVar()
mode_var = ctk.StringVar(value="")
content_type_var = ctk.StringVar(value="Auto")
apply_to_subfolders = ctk.BooleanVar(value=True)
jpg_var = ctk.BooleanVar(value=True)
ico_var = ctk.BooleanVar(value=True)
visibility_var = ctk.StringVar(value="hidden")
rename_folders_var = ctk.BooleanVar(value=False)
view_mode = ctk.StringVar(value="Panel")
select_all_undo_var = ctk.BooleanVar(value=False)
apply_all_var = ctk.BooleanVar(value=False)

# UI flags
log_expanded = False
undoing = False
expand_container = None     
show_rename_edit = False
set_content_type = "Auto"

# Preview system state
preview_posters = []
posters = []
current_index = 0
undo_map = {}
to_replace = []