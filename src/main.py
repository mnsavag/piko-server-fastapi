from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from src.api.v1.api import api_router


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        raise Response("Internal Server Error", status_code=500)


app.middleware('http')(catch_exceptions_middleware)

app.include_router(api_router)
