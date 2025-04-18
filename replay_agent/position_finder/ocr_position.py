from utils.logger_setup_data_extraction import logger
import os
import json
from prompt.position_finder import CORRECT_COORDINATE

from utils.element_analyzer_easyocr import get_elements

from core.llm_chat import LLMChat
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

class Ocr_position:
    def __init__(self):
        self.chat = LLMChat()


    def correct_click_coordinates(self, action_description, text, init_x, init_y, image_path, output_path):
        elements_in_range = get_elements(image_path, output_path, init_x, init_y, 500)
        if len(elements_in_range) == 0:
            logger.info("No elements found in the specified range.")
            return
        ## Check if the text is present in any of the elements
        if text is not None:
            match_list = []
            for element in elements_in_range:
                if text in element.get("text"):
                    logger.info(f"Found element with text '{text}' in range.")
                    match_list.append(element)
            if len(match_list) == 1:
                Id = match_list[0].get("id")
                coordinate = match_list[0].get("coordinates")
                x = coordinate.get("x")
                y = coordinate.get("y")
                print(f"Correct click coordinates to: ({x}, {y})")
                return x, y
        #if text not in any of the elements or more than one matched elements, then we need to call AI model to correct the coordinates
        logger.info(f"Correcting click coordinates for description: {action_description}")
        response_schemas = [
            ResponseSchema(name="Id", description="Id of rectangle that need to be clicked, Integer")
        ]  
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        response_format = output_parser.get_format_instructions()
        partial_prompt = PromptTemplate(
            template=CORRECT_COORDINATE,
            partial_variables={"response_format": response_format}
        )
        prompt = partial_prompt.format(action_description=action_description, x=init_x, y=init_y)
        logger.info(f"Prompt: {prompt}")
        try:
            # ai_model = GenAIModel()
            # response = ai_model.process_image(output_path, prompt)
            response = self.chat.image_respond(output_path, prompt, os.getenv("DEFAULTM_MODEL"))
        except Exception as e:
            logger.error(f"Error: {e}")
            return
        if response is None or response == "Running Error":
            return
        # logger.info(f"Response: {response}")
        json_response = json.loads(response)
        Id = json_response.get("Id")
        coordinate = elements_in_range[int(Id)].get("coordinates")
        x = coordinate.get("x")
        y = coordinate.get("y")
        print(f"Correct click coordinates to: ({x}, {y})")
        return x, y
        
