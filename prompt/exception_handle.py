IDENTIFY_EXCEPTION = """
I am a RPA robot. My current action step description is:
 {description}

 But it encountered an exception.
 Can you help identify the exception and provide solution(actions).
 
 The screen resolution is {screen_size}.  

1.If you can find out the solution, please provide the action to solve the exception.
Below are the four available actions and their parameters:
- Click(x,y) # x and y are the pixel coordinates of the screen, left upper point's coordinate is (0,0).
- Type("text") 
- Scroll(distance, direction) #distance: represents the amount of scrolling, it should be a pixel value that can be converted to an integer. direction: 0 for vertical scroll, 1 for horizontal scroll; when distance is positive, scroll up or left, when distance is negative, scroll down or right
- PressHotkey('ctrl', 'c') # Press hotkey combination

2.If you can not find out the solution, you are allowed to perform only Click and Scroll actions to explore the screen. For example, you can click on the dropdown buttom to find available values, or scroll down to find more information.
Don't do the repetitive explorations(actions).
Explore History:
{explore_history}

{response_format}

"""


ASK_FOR_HELP = """
I am a RPA robot. I have performed an action step, but the action failed:
 {step_description}
And next action step is:
 {next_step_description}
Can you give me some suggestions to fix the problem so that I can continue to perform next action step?
{response_format}

"""


PLAN_FOR_EXCEPTION = """
I am a RPA robot. I have performed an action step, but the action failed:
 {step_description}
And next action step is:
 {next_step_description}
Can you give me some suggestions to fix the problem so that I can continue to perform next action step?
Action MUST be limited to the following types: KEY_PRESS, LEFT_CLICK, RIGHT_CLICK, DOUBLE_CLICK, SCROLL, HOTKEY.
Action example:
<No>: <ACTION>-<Description of action>
1: LEFT_CLICK - Left click the G15 cell in Sheet2.
2: KEY_PRESS - Enter '2' in cell G15 from keyboard.
3: HOTKEY - Save the excel file, enter ctrl+s from keyboard.

{response_format}

"""