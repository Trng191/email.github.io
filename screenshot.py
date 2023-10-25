import pyautogui
from io import BytesIO


def screen_shot():
    myScreenshot = pyautogui.screenshot()
    # myScreenshot.save(r'screenshot.png')
    # myScreenshot.show()
    buffer = BytesIO()
    myScreenshot.save(buffer, format="PNG")
    return buffer.getvalue()
