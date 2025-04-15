import pyautogui

def hotkey(*keys):
    """
    Function to execute a hotkey combination using pyautogui.
    
    :param keys: The keys to be pressed together as a hotkey combination.
    """
    pyautogui.hotkey(*keys)

# Example usage:
# execute_hotkey('ctrl', 'c')  # This will simulate pressing Ctrl+C