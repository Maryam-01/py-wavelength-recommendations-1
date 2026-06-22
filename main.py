from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import close_db_connection, connect_to_db
from routes.recommendations import router as recommendations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db()
    yield
    await close_db_connection()


app = FastAPI(title="Wavelength Recommendations", lifespan=lifespan)
app.include_router(recommendations_router)
