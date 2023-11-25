from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import Response
from src.utils.alias_generators import to_snake, to_camel, to_pascal
from src.api.v1.api import api_router
from starlette.datastructures import MutableHeaders
import json


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

#async def catch_exceptions_middleware(request: Request, call_next):
#    try:
#        return await call_next(request)
#    except Exception:
#        raise Response("Internal Server Error", status_code=500)


#app.middleware('http')(catch_exceptions_middleware)

app.include_router(api_router)
