from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Test"], prefix="/test")

@router.get("/", response_class=JSONResponse)
async def hello_world():
    response = jsonable_encoder({'msg' : "Hello world"})
    return response