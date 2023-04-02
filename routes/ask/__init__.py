from fastapi import APIRouter, Body, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.gpt_service import GPTService

router = APIRouter(tags=["Ask"], prefix="/ask")

gpt = GPTService()

@router.post("/", response_class=JSONResponse)
async def ask_prompt(prompt: str = Form(...)):
    query_result = gpt.chat_completion(prompt)
    msg = {'prompt' : prompt, 'result': query_result.choices[0].message.content}
    response = jsonable_encoder(msg)
    return response

@router.post("/image", response_class=JSONResponse)
async def image_prompt(prompt: str = Form(...)):
    query_result = gpt.image_generation(prompt)
    msg = {'prompt' : prompt, 'result': query_result.data[0].url}
    response = jsonable_encoder(msg)
    return response