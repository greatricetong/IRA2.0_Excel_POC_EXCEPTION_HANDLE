import pyautogui
import time

def take_screenshot(save_path: str):
    """
    Takes a screenshot and saves it to the specified path.

    :param save_path: The path where the screenshot will be saved, including the filename and extension.
    """
    time.sleep(2)
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)

# Example usage:
# take_screenshot('data/input/exception_image/current.png')