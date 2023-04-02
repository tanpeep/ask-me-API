import os
import openai
from dotenv import load_dotenv
from models.chat_model import Chat
from models.image_model import Image
from models.edit_model import Edit
load_dotenv()

import time

openai.api_key = str(os.getenv('OPENAI_API_KEY'))
openai.Model.list()

class GPTService :
    def __init__(self) -> None:
        self.urls = 'https://api.openai.com/v1/'

    async def chat_completion(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )

        response_obj = Chat(**response)
        return response_obj
    
    async def image_generation(self, image_prompt):
        response = openai.Image.create(
            prompt= image_prompt,
            n=1,
            size="1024x1024"
        )
        response_obj = Image(**response)
        return response_obj
    
    async def edit_text(self, input, instruction):
        response = openai.Edit.create(
            model="text-davinci-edit-001",
            input=input,
            instruction=instruction
        )
        response_obj = Edit(**response)
        return response_obj
    
    async def audio_transcription(self, file):
        response = openai.Audio.transcribe("whisper-1", file)
        return response
    
    async def audio_translation(self, file):
        response = openai.Audio.translate("whisper-1", file)
        return response
