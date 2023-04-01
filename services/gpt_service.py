import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = str(os.getenv('OPENAI_API_KEY'))
openai.Model.list()

class GPTService :
    def __init__(self) -> None:
        self.urls = 'https://api.openai.com/v1/'

    def chat_completion(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
        return response
    
    def image_generation(self, image_prompt):
        response = openai.Image.create(
            prompt= image_prompt,
            n=1,
            size="1024x1024"
        )
        return response