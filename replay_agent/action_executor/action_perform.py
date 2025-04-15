import re
import importlib

class ActionExecutor:
    def __init__(self):
        self.actions = {}
        self.load_actions('scroll_action')
        self.load_actions('click_action')
        self.load_actions('type_action')
        self.load_actions('hotkey_action')
        self.load_actions('screenshot')

    def load_actions(self, module_name):
        module = importlib.import_module(f'replay_agent.action_executor.{module_name}')
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr):
                self.actions[attr_name.lower()] = attr

    def execute_action(self, action_description: str):
        if not action_description:
            raise ValueError("Action description cannot be None or empty")
        if '(' not in action_description or ')' not in action_description:
            raise ValueError(f"Invalid action description '{action_description}'. Must be in the format 'action_name(arg1, arg2, ...)'")
        action_name = action_description.split('(')[0].lower()
        action = self.actions.get(action_name)
        if action is None:
            raise ValueError(f"Action '{action_name}' not found")
        print(f"Executing action '{action_name}' with args '{action_description}'")
        args = re.search(r'\((.*?)\)', action_description).group(1)
        if not args:
            return action()
        else:
            return action(*args.split(','))        
