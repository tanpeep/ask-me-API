from fastapi import FastAPI

from routes import hello, ask

app = FastAPI()

@app.on_event("startup")
async def startup() -> None:
    pass

@app.on_event("shutdown")
async def shutdown() -> None:
    pass

@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(hello.router)
app.include_router(ask.router)