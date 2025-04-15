import pyautogui
import time

def type(text):
    time.sleep(2)  # Wait for 2 seconds before typing
    pyautogui.typewrite(text)
