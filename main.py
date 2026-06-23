import time
import psycopg

from fastapi import FastAPI, Depends
from db import get_async_conn, connect_to_db, close_db_connection

_cache: dict[str, tuple[float, list]] = {}
CACHE_TTL_SECONDS = 3600  # placeholder - decide your own value below

def get_cached(key: str):
    entry = _cache.get(key)
    if entry is None:
        return None  # cache miss
    stored_at, value = entry
    if time.time() - stored_at > CACHE_TTL_SECONDS:
        return None  # expired - treat as a miss
    return value  # cache hit




def set_cached(key: str, value: list):
    _cache[key] = (time.time(), value)

app = FastAPI()











# @router.get("top-tracks/{genre}")
# async def get_top_tracks_by_genre(genre: str):
#     cached_tracks = get_cached(genre)

#     if cached_tracks is not None:
#         print ("cache hit")
#         return cached_tracks
    
#     else:
#         print("cache miss") 
        
#     tracks = []
#     set_cached(genre, tracks)

#     return tracks

@app.on_event("startup")
async def startup():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db_connection()

@app.get("/recommendations/top-tracks/{genre}")
async def get_top_tracks_by_genre(genre: str, conn=Depends(get_async_conn)):
    cached_tracks = get_cached(genre)

    if cached_tracks is not None:
        print("Cache hit")
        return cached_tracks

    print("Cache miss")

    async with conn.transaction():
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT t.track_id, t.title, a.name AS artist, t.play_count
                FROM tracks t
                JOIN artists a ON t.artist_id = a.artist_id
                WHERE a.genre = %s
                ORDER BY t.play_count DESC
                LIMIT 20
                """,
                (genre,),
            )
            rows = await cur.fetchall()

    set_cached(genre, rows)
    return rows

@app.get("/recommendations/{user_id}")
async def get_recommendations_for_user(user_id: int, conn=Depends(get_async_conn)):
    async with conn.cursor() as cur:
        await cur.execute(
            """
            WITH top_genre AS (
                SELECT a.genre
                FROM listening_events le
                JOIN tracks t ON le.track_id = t.track_id
                JOIN artists a ON t.artist_id = a.artist_id
                WHERE le.user_id = %s
                GROUP BY a.genre
                ORDER BY COUNT(*) DESC
                LIMIT 1
            )
            SELECT t.track_id, t.title, a.name AS artist, t.play_count
            FROM tracks t
            JOIN artists a ON t.artist_id = a.artist_id
            WHERE a.genre = (SELECT genre FROM top_genre)
              AND t.track_id NOT IN (
                  SELECT track_id FROM listening_events WHERE user_id = %s
              )
            ORDER BY t.play_count DESC
            LIMIT 10
            """,
            (user_id, user_id),
        )
        rows = await cur.fetchall()
    return rows




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=4444, reload=True)


