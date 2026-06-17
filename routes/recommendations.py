# routes/recommendations.py
# Both endpoints below are already async and already use asyncpg -
# the conversion work is done. Your mini-sprint task is to add either
# a cache (top-tracks) or rate limiting (the per-user feed) - see the
# lesson instructions, not this file, for what to build.

from fastapi import APIRouter, Depends

from db import get_async_conn

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/top-tracks/{genre}")
async def get_top_tracks_by_genre(genre: str, conn=Depends(get_async_conn)):
    rows = await conn.fetch(
        """
        SELECT t.track_id, t.title, a.name AS artist, t.play_count
        FROM tracks t
        JOIN artists a ON t.artist_id = a.artist_id
        WHERE a.genre = $1
        ORDER BY t.play_count DESC
        LIMIT 20
        """,
        genre,
    )
    return [dict(row) for row in rows]


@router.get("/{user_id}")
async def get_recommendations_for_user(user_id: int, conn=Depends(get_async_conn)):
    rows = await conn.fetch(
        """
        WITH top_genre AS (
            SELECT a.genre
            FROM listening_events le
            JOIN tracks t ON le.track_id = t.track_id
            JOIN artists a ON t.artist_id = a.artist_id
            WHERE le.user_id = $1
            GROUP BY a.genre
            ORDER BY COUNT(*) DESC
            LIMIT 1
        )
        SELECT t.track_id, t.title, a.name AS artist, t.play_count
        FROM tracks t
        JOIN artists a ON t.artist_id = a.artist_id
        WHERE a.genre = (SELECT genre FROM top_genre)
          AND t.track_id NOT IN (
              SELECT track_id FROM listening_events WHERE user_id = $1
          )
        ORDER BY t.play_count DESC
        LIMIT 10
        """,
        user_id,
    )
    return [dict(row) for row in rows]
