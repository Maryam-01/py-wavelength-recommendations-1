# db.py
# asyncpg connection pool and the FastAPI dependency that hands a
# pooled connection to a route handler.

import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

pool: asyncpg.Pool | None = None


async def connect_to_db():
    global pool
    pool = await asyncpg.create_pool(dsn=DATABASE_URL)


async def close_db_connection():
    await pool.close()


async def get_async_conn():
    async with pool.acquire() as connection:
        yield connection
