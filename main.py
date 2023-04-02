from fastapi import FastAPI
from routes import hello, ask
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware

import time

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    pass

@app.on_event("shutdown")
async def shutdown() -> None:
    pass

@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.process_time())
    return response

app.include_router(hello.router)
app.include_router(ask.router)