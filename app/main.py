from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routes import router

app = FastAPI(
    title="ComicCraft",
    description="AI Comic Story Creator using Gemini Models",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(router)


@app.get("/health")
async def health_check():
    return {
        "status": "success",
        "message": "ComicCraft server is running"
    }