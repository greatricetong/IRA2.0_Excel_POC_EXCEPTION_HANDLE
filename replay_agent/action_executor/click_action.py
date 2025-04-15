import pyautogui

def click(x, y):
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        return "Invalid coordinates"
    pyautogui.click(x,y)

def double_click( x, y):
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        return "Invalid coordinates"
    pyautogui.doubleClick(x,y)

def right_click(x, y):
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        return "Invalid coordinates"
    pyautogui.rightClick(x,y)

def get_screen_size():
    size = pyautogui.size()
    return str(size.width) + '*' + str(size.height)
