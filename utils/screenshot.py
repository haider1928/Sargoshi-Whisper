import pyautogui
import io

def get_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        image_bytes = io.BytesIO()
        screenshot.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        return image_bytes
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None
