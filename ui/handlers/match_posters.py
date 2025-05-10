from PIL import Image
from io import BytesIO
import requests
from customtkinter import CTkImage

def fetch_image_preview(url, size=(100, 140)):
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        img_data = Image.open(BytesIO(response.content)).convert("RGBA")
        img_data = img_data.resize(size)
        return CTkImage(light_image=img_data, dark_image=img_data, size=size)
    except Exception as e:
        print(f"Failed to load image from {url}: {e}")
        return None
