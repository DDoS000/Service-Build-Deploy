from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from build.api import build_router

app = FastAPI(
    docs_url='/docs',
    redoc_url='/redocs',
    title='Service-Deploy',
    version='1.0',
    openapi_url='/openapi.json'
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Add routers
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(build_router, tags=["Auth"])
app.include_router(v1_router)


# @app.on_event('startup')
# async def startup():
#     await database.connect()
#     print('DB is Connect!')


# @app.on_event('shutdown')
# async def shutdown():
#     await database.disconnect()
#     print('DB is Disconnect!')


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=5, log_level="info")
