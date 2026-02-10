from fastapi import FastAPI
from src.backend.routes import routers
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    for router in routers:
        app.include_router(router)
    yield


app = FastAPI(title="EffectiveMobile Backend", lifespan=lifespan)

if __name__ == '__main__':
    uvicorn.run("uvi", reload=True)
