import pyautogui


def scroll(distance, direction):
    try:
        distance = int(distance)
        direction = int(direction)
    except ValueError:
        return "Invalid distance or direction"
    if direction == 0:
        # Vertical scroll
        pyautogui.scroll(distance)
    elif direction == 1:
        # Horizontal scroll
        pyautogui.hscroll(distance)
    else:
        raise ValueError("Invalid direction. Use 0 for vertical and 1 for horizontal scroll.")

