from fastapi import FastAPI, Depends
from db import get_async_conn, connect_to_db, close_db_connection

app = FastAPI()

@app.on_event("startup")
async def startup():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db_connection()

@app.get("/recommendations/top-tracks/{genre}")
async def get_top_tracks_by_genre(genre: str, conn=Depends(get_async_conn)):
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