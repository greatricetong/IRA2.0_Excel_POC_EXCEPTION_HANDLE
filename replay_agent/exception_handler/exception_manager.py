# from utils.logger_setup_replayer import logger
from utils.logger_setup_data_extraction import logger
from replay_agent.action_executor.action_perform import ActionExecutor
import os
import json
from prompt.exception_handle import IDENTIFY_EXCEPTION
from prompt.exception_handle import ASK_FOR_HELP
from replay_agent.position_finder.ocr_position import Ocr_position
from prompt.exception_handle import PLAN_FOR_EXCEPTION

import tkinter as tk
from tkinter import messagebox
import shutil
import time

from utils.element_analyzer_easyocr import get_elements

from core.llm_chat import LLMChat
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chat_models import init_chat_model
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate


class ExceptionManager:
    def __init__(self):
        self.chat = LLMChat()
        self.executor = ActionExecutor()
        self.exception = None
        self.explore = "No"
        self.explore_history = []
        self.step_count = 0


    def handle(self, description):
        root = tk.Tk()
        root.withdraw()
        global popup
        while True:
            self.identify_exception(description)
            
            # popup = tk.Toplevel()
            # popup.title("Exception Handling")
            # popup.geometry("550x200")
            # prompt_lable = tk.Label(popup, text="Confirming to continue or stop")
            # prompt_lable.grid(row=0, column=0, columnspan=2, pady=30, padx=75)
            # continue_button = tk.Button(popup, text="Continue", command=self.continue_case)
            # continue_button.grid(row=1, column=0, padx=10)
            # stop_button = tk.Button(popup, text="Stop", command=self.stop_case)
            # stop_button.grid(row=1, column=1, padx=10)
            # popup.protocol("WM_DELETE_WINDOW", self.stop_case)
            # popup.mainloop()
            # # return to check if the exception is handled, if not, call ask_for_help
            if self.explore == "No":
                break
        root.destroy()
        return 

    def continue_case(self):
        popup.quit()
        popup.destroy()
        
        
    def stop_case(self):
        self.explore = "No"
        popup.quit()
        popup.destroy()



    def identify_exception(self, mydescription):
        # get screenshot of the screen and save them 
        self.step_count += 1
        image_path = 'data/input/exception_image/current.png'
        self.executor.execute_action(f"take_screenshot({image_path})")
        self.copy_and_rename_file(image_path, 'data/input/exception_image/screenshot_history', f'Image{self.step_count}.png')
        #image_path = 'data/input/exception_image/Image3.png'

        # identify the type of exception and provide actions
        current_screen_size = self.executor.execute_action("get_screen_size()")

        response_schemas = [
            ResponseSchema(name="IsException", description="Indicates if it is an exception (Yes/No)"),
            ResponseSchema(name="IsExplore", description="Need more actions to explore possible solutions to fix the exception (Yes/No)"),
            ResponseSchema(name="Action", description="Next action api to call. if no next action, return NoAction"),
            ResponseSchema(name="ClickElementText", description="If the action is click, return the text of the element to be clicked"),
            ResponseSchema(name="ExceptionType", description="Type of the exception"),
            ResponseSchema(name="ActionDescription", description="Description of the action")
        ]  

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        response_format = output_parser.get_format_instructions()
        partial_prompt = PromptTemplate(
            template=IDENTIFY_EXCEPTION,
            partial_variables={"response_format": response_format}
        )
        prompt = partial_prompt.format(screen_size=current_screen_size, description=mydescription, explore_history=self.explore_history)
        logger.info(f"Prompt: {prompt}")
        try:
            # ai_model = GenAIModel()
            # response = ai_model.process_image(image_path, prompt)
            response = self.chat.image_respond(image_path, prompt, os.getenv("DEFAULTM_MODEL"))
        except Exception as e:
            logger.error(f"Error: {e}")
            return
        if response is None or response == "Running Error":
            return
        # logger.info(f"Response: {response}")
        json_response = json.loads(response)
        action = json_response.get("Action")
        click_element_text = json_response.get("ClickElementText")
        exception_type = json_response.get("ExceptionType")
        self.explore = json_response.get("IsExplore")
        action_description = json_response.get("ActionDescription")
        if self.explore=="Yes":
            self.explore_history.append(action)
        if action != "NoAction":
            if action.lower().startswith("click"):
                try:
                    x, y = action.split("(")[1].split(",")
                    x = int(x)
                    y = int(y.split(")")[0])
                    ocr_position = Ocr_position()
                    c_x, c_y = ocr_position.correct_click_coordinates(action_description, click_element_text, x, y, image_path, f'data/input/exception_image/screenshot_history/Image{self.step_count}_ocr.png')
                    action = f"Click({round(c_x)},{round(c_y)})"
                    self.perform_action(action)
                except Exception as e:
                    logger.error(f"Error: {e}")
            else:
                self.perform_action(action)
       
      

    def perform_action(self, action):
        # Logic to perform action based on exception type
        logger.info(f"Performing action: {action}")
        self.executor.execute_action(action)
        
    def plan_for_exception(self,step_description, next_step_description, image_path):
        if step_description is None or step_description == "":
            logger.error("Step description is None")
            return
        if image_path is None or image_path == "":
            logger.error("Image path is None")
            return
        
        logger.info(f"Plan Actions to Handle Exception: {step_description}")
        response_schemas = [
            ResponseSchema(name="ExceptionDescription", description="Description of the exception"),
            ResponseSchema(name="ActionDescription", description="Description of the action"),
            ResponseSchema(name="ActionSteps", description="Actions to handle the exception", type="string array")
        ]  
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        response_format = output_parser.get_format_instructions()
        partial_prompt = PromptTemplate(
            template=PLAN_FOR_EXCEPTION,
            partial_variables={"response_format": response_format}
        )
        prompt = partial_prompt.format(step_description=step_description, next_step_description=next_step_description)
        logger.info(f"Prompt: {prompt}")
        try:
            # ai_model = GenAIModel()
            # response = ai_model.process_image(output_path, prompt)
            response = self.chat.image_respond(image_path, prompt, os.getenv("DEFAULTM_MODEL"))
        except Exception as e:
            logger.error(f"Error: {e}")
            return
        if response is None or response == "Running Error":
            return
        # logger.info(f"Response: {response}")
        json_response = json.loads(response)
        suggestion = json_response.get("ActionDescription")
        action_steps = json_response.get("ActionSteps")
        # send email to the team to ask for help
        logger.info(f"Sending email for help: {suggestion}")
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Ask for help", f"Suggestion: {suggestion} \nPlease click 'OK' to continue")
        root.destroy()
        return action_steps

    def ask_for_help(self, step_description, next_step_description):
        # Logic to ask for help when exception cannot be handled
        logger.info(f"Ask for help to handle exception: {step_description}")
        self.step_count += 1
        image_path = 'data/input/exception_image/current.png'
        self.executor.execute_action(f"take_screenshot({image_path})")
        self.copy_and_rename_file(image_path, 'data/input/exception_image/screenshot_history', f'Image{self.step_count}.png')
        response_schemas = [
            ResponseSchema(name="ExceptionDescription", description="Description of the exception"),
            ResponseSchema(name="ActionDescription", description="Description of the action"),
            ResponseSchema(name="Suggestion", description="Suggestion to handle the exception")
        ]  
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        response_format = output_parser.get_format_instructions()
        partial_prompt = PromptTemplate(
            template=ASK_FOR_HELP,
            partial_variables={"response_format": response_format}
        )
        prompt = partial_prompt.format(step_description=step_description, next_step_description=next_step_description)
        logger.info(f"Prompt: {prompt}")
        try:
            # ai_model = GenAIModel()
            # response = ai_model.process_image(output_path, prompt)
            response = self.chat.image_respond(image_path, prompt, os.getenv("DEFAULTM_MODEL"))
        except Exception as e:
            logger.error(f"Error: {e}")
            return
        if response is None or response == "Running Error":
            return
        # logger.info(f"Response: {response}")
        json_response = json.loads(response)
        suggestion = json_response.get("Suggestion")
        # send email to the team to ask for help
        logger.info(f"Sending email for help: {suggestion}")
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Ask for help", f"Suggestion: {suggestion} \nPlease click 'OK' to continue")
        root.destroy()


    def copy_and_rename_file(self, source_file, destination_folder, new_name):
        try:
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            destination_file = os.path.join(destination_folder, new_name)
            shutil.copy2(source_file, destination_file)
        except FileNotFoundError:
            print(f"Error: source file {source_file} not found")
        except Exception as e:
            print(f"Unknown exception while copying file: {e}")