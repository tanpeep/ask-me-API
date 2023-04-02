from fastapi import APIRouter, Body, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.gpt_service import GPTService
import io

router = APIRouter(tags=["Ask"], prefix="/ask")

gpt = GPTService()

@router.post("/", response_class=JSONResponse)
async def ask_prompt(prompt: str = Form(...)):
    query_result = await gpt.chat_completion(prompt)
    msg = {'prompt' : prompt, 'result': query_result.choices[0].message.content}
    response = jsonable_encoder(msg)
    return response

@router.post("/image", response_class=JSONResponse)
async def image_prompt(prompt: str = Form(...)):
    query_result = await gpt.image_generation(prompt)
    msg = {'prompt' : prompt, 'result': query_result.data[0].url}
    response = jsonable_encoder(msg)
    return response

@router.post("/edit", response_class=JSONResponse)
async def edit_text(input: str = Form(...), instruction: str = Form(...)):
    query_result = await gpt.edit_text(input, instruction)
    msg = {'input' : input, 'instruction': instruction, 'result': query_result.choices[0].text}
    response = jsonable_encoder(msg)
    return response

@router.post("/audio/{type}", response_class=JSONResponse)
async def audio_generation(type, file: UploadFile = File(...)):
    file_obj = io.BytesIO(file.file.read())
    file_obj.name = file.filename
    if type == "transcript" :
        query_result = await gpt.audio_transcription(file_obj)
    elif type == "translate" :
        query_result = await gpt.audio_translation(file_obj)
    else :
        raise HTTPException(status_code=400, detail="Type mismatch")
    
    msg = {'file' : file.filename, 'text': query_result["text"]}
    response = jsonable_encoder(msg)
    return response