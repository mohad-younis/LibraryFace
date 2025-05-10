from core.config import Image

def convert_to_ico(jpg_path, ico_path):
    try:
        img = Image.open(jpg_path).convert("RGBA")
        max_side = max(img.size)
        canvas = Image.new("RGBA", (max_side, max_side), (0, 0, 0, 0))
        canvas.paste(img, ((max_side - img.width) // 2, (max_side - img.height) // 2))
        canvas.save(ico_path, format="ICO", sizes=[(256, 256)])
        return True
    except Exception as e:
        print(f"[ICO ERROR] {e}")
        return False