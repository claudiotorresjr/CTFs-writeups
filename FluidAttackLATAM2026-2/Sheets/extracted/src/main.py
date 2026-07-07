import re
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api import router as apiRouter
from utils import admin_session_id
from bot import visit

print(f"{admin_session_id = }")

app = FastAPI()

frontend_path = Path(__file__).parent.resolve() / "frontend/dist"


@app.middleware("http")
async def csp(request: Request, call_next):
    response: Response = await call_next(request)
    if (
        not re.search(r"^/(api|docs|redoc)", request.url.path)
        and not request.url.netloc == "hook.pwn:5000"
    ):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
        )
    return response


@app.get("/")
def index():
    return FileResponse(frontend_path / "index.html")


@app.get("/report")
def report(url: str):
    if not url:
        return {"error": "Invalid URL"}

    r = visit(url)
    return r


app.include_router(apiRouter)
app.mount("/", StaticFiles(directory=frontend_path), name="static")
